import logging
import os

import fsspec
import pandas as pd


class Log:

    def __init__(
        self,
        name: str,
    ):
        self.name = name
        self.fs = fsspec.filesystem(
            protocol="az",
            connection_string=os.environ["DATA_STORAGE_ACCOUNT_CONNECTION_STRING"],
        )
        self.url = f"az://data/{name}/.csv"

    @classmethod
    def create(
        cls,
        name: str,
        schema: dict[str, str],
    ):
        log = cls(name)

        if log.fs.exists(log.url):
            logging.info("Log already exists. Returning existing object.")
            return log

        df = pd.DataFrame(data=[], columns=schema.keys())
        df = df.astype(schema)

        df.to_csv(
            path_or_buf=log.url,
            index=False,
            storage_options=log.fs.storage_options,
        )

        return log

    def write(self, df: pd.DataFrame):
        current_df = self.read()

        new_df = pd.concat([current_df, df], ignore_index=True)

        new_df.to_csv(
            path_or_buf=self.url,
            index=False,
            storage_options=self.fs.storage_options,
        )

    def read(self):
        return pd.read_csv(
            filepath_or_buffer=self.url,
            storage_options=self.fs.storage_options,
        )
