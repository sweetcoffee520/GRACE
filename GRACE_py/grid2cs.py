'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2022-11-20 15:40:27
FilePath: /ocean_change_python/GRACE_py/grid2cs.py
Description: mass to SH

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
from . import legendre as lgd

def grid2cs(grd, lat, lon, res_lonlat, love_path, Lmax, rho_water):
    """将格网值转化为C和S

    Args:
        grd (array): 格网矩阵,单位cm
        lat (array): 纬度矩阵
        lon (array): 经度矩阵
        res_lonlat (float): 经纬度分辨率
        love_path (str): Love数文件路径
        Lmax (int): 最大阶数
        rho_water (float): 水密度

    Returns:
        C,S (array): C和S矩阵
    """
    rhoE = 5507.85  # 地球密度
    a = 6371004  # 地球平均半径
    file_num = np.size(grd, 2)
    C = np.zeros((Lmax+1, Lmax+1, file_num))
    S = np.zeros((Lmax+1, Lmax+1, file_num))
    loveN_k = np.loadtxt(love_path)
    loveN_k[1] = 0.026
    kl_s = loveN_k[0:Lmax+1]
    legendre= lgd.normalized_legendre(Lmax,90-lat)

    constant_array = np.reshape(np.repeat(
        3*(1+kl_s)/(4*np.pi*a*rhoE*(2*np.arange(0, Lmax+1)+1)), Lmax+1), (Lmax+1, Lmax+1))
    '''
    行为l,列为m
    [[1,1,1]
     [2,2,2]
     [3,3,3]]
    '''
    # 循环月份
    for k in range(file_num):
        # 循环纬度
        for i in range(len(lat)):
            # cosm = np.cos(np.reshape(np.repeat(np.arange(0, Lmax+1), len(lon)), (len(lon), Lmax+1), order='F') *
            #               np.reshape(np.repeat(np.deg2rad(lon), Lmax+1), (len(lon), Lmax+1)))
            # cosm = np.cos(np.reshape(np.repeat(np.arange(Lmax+1), len(lon)),(len(lon),Lmax+1),order='F') * np.deg2rad(lon[:,None]))
            cosm = np.cos(np.arange(Lmax+1)[None,:] * np.deg2rad(lon[:,None]))


            C[:, :, k] += constant_array * (grd[i, :, k]*rho_water/100@cosm) * legendre[:, :, i] * \
                np.sin(np.deg2rad(90-lat[i]))*(np.deg2rad(res_lonlat))**2

            # sin(m*lambda)
            # sinm = np.sin(np.reshape(np.repeat(np.arange(0, Lmax+1), len(lon)), (len(lon), Lmax+1), order='F') *
            #               np.reshape(np.repeat(np.deg2rad(lon), Lmax+1), (len(lon), Lmax+1)))
            # sinm = np.sin(np.reshape(np.repeat(np.arange(Lmax+1), len(lon)),(len(lon),Lmax+1),order='F')*np.deg2rad(lon[:,None]))
            sinm = np.sin(np.arange(Lmax+1)[None,:]*np.deg2rad(lon[:,None]))

            S[:, :, k] += constant_array * (grd[i,:,k]*rho_water/100@sinm) * legendre[:, :, i] * \
                np.sin(np.deg2rad(90-lat[i]))*(np.deg2rad(res_lonlat))**2

    return C, S
