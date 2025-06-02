import pandas as pd

import logs
from integrations.dataset import Dataset
from integrations.eds import EDS
from integrations.log import Log
from jobs.spot_prices import transformations

logger = logs.get_logger(__name__)


class SpotPricesETL:

    def __init__(self):
        # source
        self.eds = EDS()
        # destiation
        self.spot_prices_dataset = Dataset("spot_prices")
        self.spot_prices_log = Log.create(
            name="log_spot_prices",
            schema={
                "date": "datetime64[us]",
            },
        )

    def get_new_dates(self) -> pd.DataFrame:
        df = self.spot_prices_log.read()
        latest_date = pd.to_datetime(df["date"]).max()
        if pd.isna(latest_date):
            latest_date = pd.Timestamp("2023-12-31T00:00:00")

        new_dates = pd.date_range(
            start=latest_date + pd.Timedelta(days=1),
            end=pd.Timestamp.now().floor("D"),
        )

        logger.info(
            f"{len(new_dates)} new dates. {len(new_dates) - len(df)} existing dates."
        )

        return new_dates

    def run(self):
        new_dates = self.get_new_dates()

        for date in new_dates:
            logger.info(f"Running ETL for date {date}")

            start_date = date
            end_date = date + pd.Timedelta(days=1)

            df = self.eds.download_period(start_date, end_date)

            ds = transformations.transform(df)

            # write to datalake
            self.spot_prices_dataset.write(ds)

            # log run
            entry = pd.DataFrame({"date": [date.strftime("%Y-%m-%d")]})
            self.spot_prices_log.write(entry)

        logger.info(f"Downloaded {date}")
