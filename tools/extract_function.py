'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-04-17 00:44:51
FilePath: /ocean_change_python/tools/extract_function.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
from tools import longitude_range as lr

def extract_range(grd,lat,lon,lat_range,lon_range=None):
    """截取格网数组

    Args:
        grd (array): 格网数组
        lat (array): 纬度数组
        lon (array): 经度数组
        lat_range (tuple): 纬度范围
        lon_range (tuple): 经度范围

    Returns:
        array: 截取之后的纬度数组，经度数组，格网数组
    """
    latm = (lat>=lat_range[0])&(lat<=lat_range[1])
    if lon_range is None:
        lonm = lon.copy()
        if np.ndim(grd) == 2:
            grdm = grd[latm,:].copy()
        elif np.ndim(grd) ==3:
            grdm = grd[latm,:,:].copy()
    else:
        lr.longitude_range(lon,lon_range)
        grd = grd[latm,:,:][:,lonm,:].copy()


    return latm,lonm,grdm

def extract_mask_from_global(res_lonlat,lat_range,lon_range=None):
    """对全球格网提取mask,有效值赋1

    Args:
        res_lonlat (float): 分辨率
        lat_range (tuple): 纬度范围
        lon_range (tuple): 经度范围

    Returns:
        array: 截取之后的纬度数组，经度数组，格网数组
    """
    if res_lonlat == 1:
        lat = np.arange(-89.5,89.6,res_lonlat)
        lon = np.arange(0.5,359.6,res_lonlat)
    elif res_lonlat == 0.5:
        lat = np.arange(-89.75,89.76,res_lonlat)
        lon = np.arange(0.25,359.76,res_lonlat)
    elif res_lonlat == 0.25:
        lat = np.arange(-89.875,89.876,res_lonlat)
        lon = np.arange(0.125,359.876,res_lonlat)
    grd = np.zeros((len(lat),len(lon)))

    lat_loc = np.where((lat>=lat_range[0])&(lat<=lat_range[1]))
    latmin = np.min(lat_loc[0])
    latmax = np.max(lat_loc[0])
    if lon_range is None:
        grd[latmin:latmax+1,:] = 1
    else:
        if lon_range[0]>lon_range[1]:
            lon_loc1 = np.where((lon>=lon_range[0]))[0]
            lon_loc2 = np.where((lon<=lon_range[1]))[0]
            grd[latmin:latmax+1,lon_loc1[0]:] = 1
            grd[latmin:latmax+1,:lon_loc2[-1]+1] = 1
        else:
            lon_loc = np.where((lon>=lon_range[0])&(lon<=lon_range[1]))
            lonmin = np.min(lon_loc[0])
            lonmax = np.max(lon_loc[0])
            grd[latmin:latmax+1,lonmin:lonmax+1] = 1


    return lat,lon,grd

def extract_mask_from_grd(grd,lat,lon,lat_range,lon_range=None):
    """对grd大小的格网提取mask,有效值赋1

    Args:
        grd (array): 需要mask的数组
        lat (array): 纬度数组
        lon (array): 经度数组
        lat_range (tuple): 纬度范围
        lon_range (tuple): 经度范围

    Returns:
        array: 截取之后的纬度数组，经度数组，格网数组
    """
    grdm = np.zeros_like(grd)
    lat_loc = np.where((lat>=lat_range[0])&(lat<=lat_range[1]))
    latmin = np.min(lat_loc[0])
    latmax = np.max(lat_loc[0])
    if lon_range is None:
        grdm[latmin:latmax+1,:] = 1
    else:
        if lon_range[0]>lon_range[1]:
            lon_loc1 = np.where((lon>=lon_range[0]))[0]
            lon_loc2 = np.where((lon<=lon_range[1]))[0]
            grdm[latmin:latmax+1,lon_loc1[0]:] = 1
            grdm[latmin:latmax+1,:lon_loc2[-1]+1] = 1
        else:
            lon_loc = np.where((lon>=lon_range[0])&(lon<=lon_range[1]))
            lonmin = np.min(lon_loc[0])
            lonmax = np.max(lon_loc[0])
            grdm[latmin:latmax+1,lonmin:lonmax+1] = 1

    return grdm

def set_mask(grd,lat,lon,values,lat_range,lon_range=None):
    """对指定范围内的值设为指定值

    Args:
        grd (array): _description_
        lat (array): _description_
        lon (array): _description_
        values (int): 指定mask的值
        lat_range (_type_): _description_
        lon_range (_type_, optional): _description_. Defaults to None.
    """
    grdm = grd.copy()
    lat_loc = np.where((lat>=lat_range[0])&(lat<=lat_range[1]))
    latmin = np.min(lat_loc[0])
    latmax = np.max(lat_loc[0])
    if lon_range is None:
        grdm[latmin:latmax+1,:] = values
    else:
        if lon_range[0]>lon_range[1]:
            lon_loc1 = np.where((lon>=lon_range[0]))[0]
            lon_loc2 = np.where((lon<=lon_range[1]))[0]
            grdm[latmin:latmax+1,lon_loc1[0]:] = values
            grdm[latmin:latmax+1,:lon_loc2[-1]+1] = values

        else:
            lon_loc = np.where((lon>=lon_range[0])&(lon<=lon_range[1]))
            lonmin = np.min(lon_loc[0])
            lonmax = np.max(lon_loc[0])
            grdm[latmin:latmax+1,lonmin:lonmax+1] = values

    return grdm