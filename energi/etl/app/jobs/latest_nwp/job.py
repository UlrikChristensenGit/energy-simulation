import pandas as pd

from integrations.dataset import Dataset
from integrations.log import Log
from jobs.latest_nwp import transformations
from logs import get_logger

logger = get_logger(__name__)


class LatestNwpETL:

    def __init__(self):
        # source
        self.versioned_nwp_dataset = Dataset("versioned_nwp")
        self.versioned_nwp_log = Log("log_versioned_nwp")
        # destination
        self.latest_nwp_dataset = Dataset("latest_nwp")
        self.latest_nwp_log = Log.create(
            name="log_latest_nwp",
            schema={
                "model_run_time_utc": "datetime64[us]",
            },
        )

    def get_available_batches(self) -> pd.DataFrame:
        df = self.versioned_nwp_log.read()
        #
        ## only consider batches that are complete
        # df = df.groupby("model_run_time_utc", as_index=False).count()
        #
        ##df = df[df["run_id"] == 61]
        #

        df = df[["model_run_time_utc"]].drop_duplicates()

        return df

    def get_transformed_batches(self) -> pd.DataFrame:
        return self.latest_nwp_log.read()

    def get_new_batches(self) -> pd.DataFrame:
        available_batches = self.get_available_batches()

        transformed_batches = self.get_transformed_batches()

        new_batches = available_batches[
            ~available_batches["model_run_time_utc"].isin(
                transformed_batches["model_run_time_utc"]
            )
        ]
        logger.info(
            f"{len(new_batches)} new batches. {len(available_batches)-len(new_batches)} existing batches."
        )

        return new_batches

    def run(self):
        new_batches = self.get_new_batches()

        for _, batch in new_batches.iterrows():

            logger.info(f"Running ETL for batch '{batch['model_run_time_utc']}'")

            ds = self.versioned_nwp_dataset.read()

            ds = ds.sel(model_run_time_utc=batch["model_run_time_utc"])

            ds = transformations.transform(ds)

            self.latest_nwp_dataset.write(ds)

            self.latest_nwp_log.write(df=batch.to_frame().T)

            logger.info(f"Transformed {batch['model_run_time_utc']}")
