'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-05-31 15:46:15
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2022-11-13 17:39:27
FilePath: /ocean_change_python/GRACE_py/geoid.py
Description: calculate geoid form SH coefficients

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
from . import legendre as lgd

def geoid(Lmax, file_num, DeltaC, DeltaS, lat, lon):
    """通过DelatC, DelatS计算大地水准面

    Args:
        Lmax (int): 最大阶数
        file_num (int): 文件数
        Deltac,DeltaS (array): 球谐系数
        lat (array): 纬度数组
        lon (array): 经度矩阵

    Returns:
    """
    a = 6371004  # 地球平均半径：单位米
    legendre = lgd.normalized_legendre(Lmax,90-lat)

    cosmf = np.cos(np.deg2rad(np.arange(Lmax+1)[:,None])*lon[None,:])
    sinmf = np.sin(np.deg2rad(np.arange(Lmax+1)[:,None])*lon[None,:])

    geo = np.zeros((len(lat), len(lon), file_num))

    for k in range(file_num):
        for i in range(len(lat)):

            geo[i, :, k] = a*np.repeat(1,Lmax+1)@(legendre[:, :, i]*DeltaC[:, :, k]@cosmf+legendre[:, :, i]*DeltaS[:, :, k]@sinmf)*100

    return geo