import os

import pandas as pd

from integrations.http import RetrySession

BASE_URL = "https://dmigw.govcloud.dk/v1/forecastdata"
MODEL_NAME = "harmonie_dini_sf"


class DMIOpenData:

    def __init__(self):
        self.api_key = os.environ["DMI_OPEN_DATA_API_KEY"]

    def get_collection(self) -> dict:
        session = RetrySession()

        response = session.get(
            url=f"{BASE_URL}/collections/{MODEL_NAME}/items",
            params={"api-key": self.api_key},
            timeout=5,
        )

        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(data["features"])

        df = pd.concat(
            objs=[
                df,
                pd.json_normalize(df["properties"]),
                pd.json_normalize(df["asset"]),
            ],
            axis="columns",
        )

        for col in ["modelRun", "datetime", "created"]:
            df[col] = df[col].str[:19]
            df[col] = pd.to_datetime(df[col])
            df[col] = df[col].dt.tz_localize(None)
            df[col] = df[col].astype("datetime64[us]")

        df = df.rename(
            columns={
                "id": "run_id",
                "datetime": "time_utc",
                "modelRun": "model_run_time_utc",
                "data.href": "content_url",
            }
        )

        df["horizon"] = df["time_utc"] - df["model_run_time_utc"]

        df = df.filter(
            [
                "run_id",
                "model_run_time_utc",
                "horizon",
                "time_utc",
                "content_url",
            ]
        )

        return df

    def download_run(self, content_url: str, file_path: str):
        session = RetrySession()

        with session.get(
            url=content_url,
            params={"api-key": self.api_key},
            stream=True,
        ) as response:

            response.raise_for_status()

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=5242880):
                    f.write(chunk)
