'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-05-31 17:21:09
LastEditors: sweetcoffee qq791227132@gmail.com
FilePath: /ocean_change_python/GRACE_py/gravity.py
Description: calculate gravity form SH coefficients

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
from . import legendre as lgd

def gravity(Lmax, file_num, DeltaC, DeltaS, lat, lon):
    """通过DelatC, DelatS计算等效水高

    Args:
        Lmax (int): 最大阶数
        file_num (int): 文件数
        Deltac,DeltaS (array): 球谐系数
        lat (array): 纬度数组
        lon (array): 经度矩阵
        love_path (str): Love数文件路径
        rho_water (float): 水密度

    Returns:
    """
    a = 6371004  # 地球平均半径：单位米
    GM = 3.986004418e14  # 地球质量
    legendre = lgd.legendre(Lmax,90-lat,len(lat))

    cosmf = np.cos(np.deg2rad(np.arange(Lmax+1)[:,None])*lon[None,:])
    sinmf = np.sin(np.deg2rad(np.arange(Lmax+1)[:,None])*lon[None,:])

    gravity = np.zeros((len(lat), len(lon), file_num))

    for k in range(file_num):
        for i in range(len(lat)):
            gravity[i, :, k] = GM/a**2*(np.arange(Lmax+1)-1)@(legendre[:, :, i]*DeltaC[:, :, k]@cosmf+legendre[:, :, i]*DeltaS[:, :, k]@sinmf)



    return gravity