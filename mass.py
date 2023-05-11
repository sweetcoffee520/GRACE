'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2022-11-13 17:23:14
FilePath: /ocean_change_python/GRACE_py/mass.py
Description: calculate mass(equivalent water height) from SH coefficients

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
from . import legendre as lgd

def mass(Lmax, file_num, DeltaC, DeltaS, lat, lon, love_path, rho_water):
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
    pave = 5507.85  # 地球平均密度：单位kg/m3
    loveN_k = np.loadtxt(love_path)
    loveN_k[1] = 0.021
    legendre = lgd.legendre(Lmax,90-lat,len(lat))

    loveN = ((2*np.arange(Lmax+1)+1)/(1+loveN_k[0:Lmax+1]))
    cosmf = np.cos(np.deg2rad(np.arange(Lmax+1)[:,None])*lon[None,:])
    sinmf = np.sin(np.deg2rad(np.arange(Lmax+1)[:,None])*lon[None,:])

    mass = np.zeros((len(lat), len(lon), file_num))

    for k in range(file_num):
        for i in range(len(lat)):
            # for j in range(lonlen):
            #     grace_un[i,j,k] = a/3*pave*np.dot(loveN,np.dot(mlegendre[:,:,i]*DeltaC[:,:,k],cosmf[:,j])+np.dot(mlegendre[:,:,i]*DeltaS[:,:,k],sinmf[:,j]))
            # 等效水高，单位cm。 除以1000kg/m3的水密度时单位为m。
            mass[i, :, k] = a/3*pave*loveN@(legendre[:, :, i]*DeltaC[:, :, k]@cosmf+legendre[:, :, i]*DeltaS[:, :, k]@sinmf)/rho_water*100

    return mass