import dataclasses as dc

import numpy as np
import xarray as xr
from sklearn.neighbors import KDTree


class CoordinateKDTree:

    def __init__(self):
        self.dim_values = None
        self.coord_values = None
        self.kd_tree = None
        self.dim_names = None
        self.coord_names = None

    def fit(self, coords: xr.Coordinates):
        df = coords.to_dataset().to_dataframe()
        self.idx_values = df.index.to_frame().values
        self.coord_values = df.values
        self.kd_tree = KDTree(self.coord_values)
        self.dim_names = df.index.names
        self.coord_names = df.columns.tolist()

    def nearest_index(self, coord: dict | object):
        if dc.is_dataclass(coord):
            coord = dc.asdict(coord)

        X = np.array([[coord[key] for key in self.coord_names]])
        i = self.kd_tree.query(X, return_distance=False)[0][0]
        idx_value = self.idx_values[i]
        return {k: v for k, v in zip(self.dim_names, idx_value)}
