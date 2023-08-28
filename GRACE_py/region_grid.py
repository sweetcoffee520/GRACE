'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2022-10-01 15:58:27
FilePath: /ocean_change_python/GRACE_py/region_grid.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np

def region_grid(c1,c2,f1,f2,res_lonlat):
    """
    c1:起始纬度
    c2:结尾纬度
    f1:起始经度
    f2:末尾经度
    res_lonlat:经纬度分辨率
    return 格网
    """

    lat = np.arange(c1,c2+0.0001,res_lonlat)
    lon = np.arange(f1,f2+0.0001,res_lonlat)
    latlen = len(lat)
    lonlen = len(lon)
    # 维度列向量
    latm = np.repeat(lat,lonlen).reshape(-1,1)
    # 经度列向量，tile复制整个数组，repeat复制每个值，reshape参数order指定索引顺序，order='C'按行索引，order='F'按列索引，同时赋值先后顺序与索引顺序相同
    # 另外如果变成三维数组的话，当order='C'，是则是第一维为最外面的维度，即后两维里面是个二维数组；当order='F'时，第三维为最外面的维度，即前两维是二维数组
    lonm = np.tile(lon,latlen).reshape(-1,1)
    #实际返回的时元组
    return lat,lon,latlen,lonlen,latm,lonm
