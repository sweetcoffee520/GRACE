'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-07-11 15:40:29
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2024-03-26 14:09:21
FilePath: /ocean_change_python/tools/interpolate_data.py
Github: https://github.com/sweetcoffee520
Description:
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import xarray as xr
import pandas as pd
import numpy as np
import warnings
from scipy.interpolate import griddata
from tools import time_transfer as tt

def interpolate_data(data, lat, lon, lat_interp, lon_interp, method='nearest'):
    """
    空间数据插值。

    参数:
    - data (array): 待插值的数据数组。
    - lat (array): 原始数据的纬度数组。
    - lon (array): 原始数据的经度数组。
    - lat_interp (array): 目标插值纬度数组。
    - lon_interp (array): 目标插值经度数组。
    - method (str): 插值方法，默认为'nearest'。

    返回:
    - array: 插值后的数据数组。
    """
    lon = np.where(lon < 0, lon + 360, lon)
    lon_interp = np.where(lon_interp < 0, lon_interp + 360, lon_interp)
    xv, yv = np.meshgrid(lon, lat)
    point = np.c_[xv.ravel(), yv.ravel()]
    interp_xv, interp_yv = np.meshgrid(lon_interp, lat_interp)
    interp_point = np.c_[interp_xv.ravel(), interp_yv.ravel()]

    if data.ndim == 2:
        data_interp = griddata(point, data.ravel(), interp_point, method=method).reshape(len(lat_interp), len(lon_interp))
    elif data.ndim == 3:
        data_interp = np.array([griddata(point, data[:, :, i].ravel(), interp_point, method=method).reshape(len(lat_interp), len(lon_interp)) for i in range(data.shape[2])]).transpose(1, 2, 0)

    return data_interp

def spatial_interpolate_to_specified_times(origin_data, origin_times, target_times, method='cubic'):
    """
    在空间上对数据进行时间序列插值，以适应指定的时间点。

    参数:
    - origin_data (array): 原始三维数据数组，其中第三维是时间维度。
    - origin_times (pd.DatatimeIndex): 原始数据对应的时间序列。
    - target_times (pd.DatatimeIndex): 目标时间序列，数据将被插值到这些时间点。
    - method (str): 插值方法，默认为 'linear'。

    返回:
    - array: 插值后的三维数据数组，第三维为目标时间维度。
    """
    # 验证数据维度
    if origin_data.ndim != 3:
        raise ValueError("origin_data 必须是三维数组。")

    # 初始化插值后的数据数组
    interpolated_data = np.zeros((origin_data.shape[0], origin_data.shape[1], len(target_times)))

    # 对每个空间点上的时间序列进行插值
    for i in range(origin_data.shape[0]):
        for j in range(origin_data.shape[1]):
            if np.any(origin_data[i, j, :]):  # 检查是否有有效数据
                ts = pd.Series(origin_data[i, j, :], index=origin_times)
                ts_interp = ts.reindex(target_times.union(origin_times)).interpolate(method=method)
                if np.isnan(ts_interp.iloc[0]):
                    ts_interp.iloc[0] = ts_interp.iloc[0]
                if np.isnan(ts_interp.iloc[-1]):
                    ts_interp.iloc[-1] = ts_interp.iloc[-2]
                interpolated_data[i, j, :] = ts_interp.reindex(target_times).values

    return interpolated_data

def interpolate_time_series(origin_date, origin_data, inter_date, method='cubic'):
    """
    时间序列数据插值。

    参数:
    - origin_date (array): 原始时间序列。
    - origin_data (array): 原始数据序列。
    - inter_date (array): 目标插值时间序列。
    - method (str): 插值方法，默认为'cubic'。

    返回:
    - Series: 插值后的时间序列数据。
    """
    origin_series = pd.Series(origin_data, index=origin_date,name='origin')
    specified_series = pd.Series(index=inter_date,name='specified')
    merge_series = pd.merge(origin_series, specified_series, how='outer', left_index=True, right_index=True)
    merge_series.iloc[:,0]=merge_series.iloc[:,0].interpolate(method=method)

    if np.isnan(merge_series.iloc[0,0]):
        merge_series.iloc[0,0] = merge_series.iloc[1,0]
    if np.isnan(merge_series.iloc[-1,0]):
        merge_series.iloc[-1,0] = merge_series.iloc[-2,0]

    return merge_series.loc[inter_date,'origin']

def interpolate_to_month_middle(origin_data, origin_date=None, method='cubic'):
    """
    将时间序列数据插值到每月中间。

    参数:
    - origin_data (array or pd.Series): 原始数据序列或 pandas Series 对象。
    - origin_date (pd.DatetimeIndex, optional): 若 origin_data 为数组，则需要提供对应的日期序列。
    - method (str): 插值方法，默认为 'cubic'。

    返回:
    - pd.Series: 插值到每月中间的时间序列数据。
    """
    if not isinstance(origin_data, pd.Series):
        if origin_date is None or not isinstance(origin_date, pd.DatetimeIndex):
            raise ValueError("必须提供有效的 pd.DatetimeIndex 类型的 origin_date.")
        origin_series = pd.Series(origin_data, index=origin_date,name='origin')
    else:
        origin_series = origin_data

    # 生成每月中间的日期
    inter_dates = tt.dateseries_to_middle_of_month(origin_series.index)

    return interpolate_time_series(origin_series.index, origin_series.values, inter_dates, method=method)

def data_interpolation_to_grace(data_series, grace_date):
    """
    将其他数据源（如argo或altimetry）插值到grace时间序列。

    参数:
    - data_series (Series): 原始数据时间序列。
    - grace_date (array): 目标插值时间序列（grace时间）。

    返回:
    - Series: 插值后的数据时间序列。
    """
    return interpolate_time_series(data_series.index, data_series.values, grace_date)