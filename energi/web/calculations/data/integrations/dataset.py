import os

import fsspec
import numpy as np
import xarray as xr
from zarr.storage import FSStore


class Dataset:

    def __init__(
        self,
        name: str,
    ):
        self.name = name
        self.fs = fsspec.filesystem(
            protocol="az",
            connection_string=os.environ["DATA_STORAGE_ACCOUNT_CONNECTION_STRING"],
        )
        self.remote_store = FSStore(
            url=f"az://data/{name}",
            fs=self.fs,
        )
        self.dims = self._get_dims()

    def _get_dims(self):
        dataset = xr.open_zarr(
            store=self.remote_store,
        )
        dims = list(dataset.sizes.keys())
        return dims

    def write(self, dataset: xr.Dataset):
        # make appropiate encodings
        for name in dataset._coord_names:
            for key in ["chunks", "preferred_chunks"]:
                if key in dataset[name].encoding:
                    del dataset[name].encoding[key]
            if np.issubdtype(dataset[name].dtype, np.datetime64):
                dataset[name].encoding["units"] = "hours since 2023-01-01 00:00:00"
            if np.issubdtype(dataset[name].dtype, np.timedelta64):
                dataset[name].encoding["units"] = "hours"

        region = {dim: "auto" for dim in self.dims}

        dataset.to_zarr(
            store=self.remote_store,
            region=region,
            write_empty_chunks=False,
        )

    def read(self):
        return xr.open_zarr(
            store=self.remote_store,
        )
