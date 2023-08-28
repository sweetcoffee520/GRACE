'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-07-11 09:40:57
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-03-06 10:21:23
FilePath: /ocean_change_python/GRACE_py/vertical_deformation.py
Github: https://github.com/sweetcoffee520
Description: calculate the vertical deformation of GRACE data
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
import re
from . import legendre as lgd
from GRACE_py import sc_action_set
from GRACE_py import region_grid as rgd
from GRACE_py import filter
def vertical_deformation(Lmax, file_num, DeltaC, DeltaS, lat, lon ,love_path):
    """通过DelatC, DelatS计算垂直形变

    Args:
        Lmax (int): 最大阶数
        file_num (int): 文件数
        Deltac,DeltaS (array): 球谐系数
        lat (array): 纬度数组
        lon (array): 经度矩阵
        love_path(str): 勒夫数集合路径
        rho_water (float): 水密度

    Returns:
    """
    a = 6371004  # 地球平均半径：单位米
    with open(love_path,'r') as f:
        all_content = f.read()
        data = np.array(re.split('#\n',all_content)[1].split()).reshape(-1,4).astype(np.float64)
    loveN_k = data[:,3]
    loveN_k[1] = 0.026
    loveN_h = data[:,1]
    legendre = lgd.normalized_legendre(Lmax,90-lat)

    loveN = ((loveN_h[0:Lmax+1])/(1+loveN_k[0:Lmax+1]))
    cosmf = np.cos(np.deg2rad(np.arange(Lmax+1)[:,None])*lon[None,:])
    sinmf = np.sin(np.deg2rad(np.arange(Lmax+1)[:,None])*lon[None,:])

    vertical_d = np.zeros((len(lat), len(lon), file_num))

    for k in range(file_num):
        for i in range(len(lat)):
            # 垂直水高，单位cm
            vertical_d[i, :, k] = a*loveN@(legendre[:, :, i]*DeltaC[:, :, k]@cosmf+legendre[:, :, i]*DeltaS[:, :, k]@sinmf)*100

    return vertical_d