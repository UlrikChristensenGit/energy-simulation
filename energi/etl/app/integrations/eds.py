import pandas as pd
from integrations.http import RetrySession

BASE_URL = "https://api.energidataservice.dk/dataset/Elspotprices"


class EDS:

    def download_period(
        self, start_date: pd.Timestamp, end_date: pd.Timestamp
    ) -> pd.DataFrame:
        session = RetrySession()

        response = session.get(
            url=BASE_URL,
            params={
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
            },
            timeout=5,
        )

        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(data["records"])

        for col in ["HourUTC", "HourDK"]:
            df[col] = df[col].str[:19]
            df[col] = pd.to_datetime(df[col])
            df[col] = df[col].dt.tz_localize(None)
            df[col] = df[col].astype("datetime64[us]")

        return df
