from tempfile import NamedTemporaryFile

import pandas as pd

import logs
from integrations.dataset import Dataset
from integrations.dmi import DMIOpenData
from integrations.log import Log
from jobs.versioned_nwp import transformations

logger = logs.get_logger(__name__)


class VersionedNwpETL:

    def __init__(self):
        # source
        self.dmi_open_data = DMIOpenData()
        # destination
        self.versioned_nwp_dataset = Dataset("versioned_nwp")
        self.versioned_nwp_log = Log.create(
            name="log_versioned_nwp",
            schema={
                "run_id": "string",
                "model_run_time_utc": "datetime64[us]",
                "horizon": "timedelta64[us]",
                "time_utc": "datetime64[us]",
                "forecast_url": "string",
            },
        )

    def get_available_forecasts(self) -> pd.DataFrame:
        forecasts = self.dmi_open_data.get_collection()

        forecasts = forecasts[
            forecasts["model_run_time_utc"]
            >= (pd.Timestamp.now() - pd.Timedelta("PT6H"))
        ]

        forecasts = forecasts[
            forecasts["model_run_time_utc"] == forecasts["model_run_time_utc"].min()
        ]

        return forecasts

    def get_downloaded_forecasts(self) -> pd.DataFrame:
        return self.versioned_nwp_log.read()

    def get_new_forecasts(self) -> pd.DataFrame:
        available_forecasts = self.get_available_forecasts()

        downloaded_forecasts = self.get_downloaded_forecasts()

        new_forecasts = available_forecasts[
            ~available_forecasts["run_id"].isin(downloaded_forecasts["run_id"])
        ]

        logger.info(
            f"{len(new_forecasts)} new forecasts. {len(available_forecasts)-len(new_forecasts)} existing forecasts."
        )

        return new_forecasts

    def run(self):
        new_forecasts = self.get_new_forecasts()

        for _, forecast in new_forecasts.iterrows():
            logger.info(f"Running ETL for run '{forecast['run_id']}'")

            with NamedTemporaryFile(suffix=".grib") as tmp_download_file:
                self.dmi_open_data.download_run(
                    content_url=forecast["content_url"],
                    file_path=tmp_download_file.name,
                )

                # read temporary file
                ds = transformations.read_grib(tmp_download_file.name)

                ds = transformations.transform(ds)

                # write to datalake
                self.versioned_nwp_dataset.write(ds)

                # log run
                self.versioned_nwp_log.write(df=forecast.to_frame().T)

            logger.info(f"Downloaded {forecast['run_id']}")
