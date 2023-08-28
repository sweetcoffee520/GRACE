'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-07-24 16:41:44
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2022-11-05 12:27:30
FilePath: /ocean_change_python/GRACE_py/read_mascon.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''

import numpy as np
import xarray as xr
import pandas as pd
from tools import time_transfer as tt


def read_CSR_mascon(filepath, lat_min=None, lat_max=None):
    dataset = xr.open_dataset(filepath)
    lat = dataset['lat'].values
    lon = dataset['lon'].values
    lwe_thickness = dataset['lwe_thickness'].values.transpose(1, 2, 0)
    time = tt.delta2date(dataset['time'].values, '2002-01-01')
    if lat_min is not None and lat_max is not None:
        lat_loc = np.where((lat <= lat_max) & (lat >= lat_min))
        lat = lat[lat_loc[0]]
        lwe_thickness = lwe_thickness[lat_loc[0], ...]
    else:
        pass
    return lat, lon, lwe_thickness, time


def read_JPL_mascon(filepath, lat_min=None, lat_max=None):
    dataset = xr.open_dataset(filepath)
    lat = dataset['lat'].values
    lon = dataset['lon'].values
    lwe_thickness = dataset['lwe_thickness'].values.transpose(1, 2, 0)
    time = pd.DatetimeIndex(dataset['time'].values)
    if lat_min is not None and lat_max is not None:
        lat_loc = np.where((lat <= lat_max) & (lat >= lat_min))
        lat = lat[lat_loc[0]]
        lwe_thickness = lwe_thickness[lat_loc[0], ...]
    else:
        pass
    return lat, lon, lwe_thickness, time


def read_GSFC_mascon(filepath, lat_min=None, lat_max=None):
    dataset = xr.open_dataset(filepath)
    lat = dataset['lat'].values
    lon = dataset['lon'].values
    lwe_thickness = dataset['lwe_thickness'].values.transpose(1, 2, 0)
    time = pd.DatetimeIndex(dataset['time'].values)
    if lat_min is not None and lat_max is not None:
        lat_loc = np.where((lat <= lat_max) & (lat >= lat_min))
        lat = lat[lat_loc[0]]
        lwe_thickness = lwe_thickness[lat_loc[0], ...]
    else:
        pass
    return lat, lon, lwe_thickness, time
