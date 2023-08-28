'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-07-16 21:07:23
FilePath: /ocean_change_python/GRACE_py/leakage_correction.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
from . import filter
from . import mass

from . import sc_action_set

def leakage_correction(DeltaSC_inverse, ocean_mask, filter_radius, Lmax, file_num, lat, lon, love_path):
    """泄露误差改正

    Args:
        DeltaSC_inverse (array): 区域内置零后反算的球谐系数SC形式
        ocean_mask (array): 海洋掩膜
        Lmax (int): 最大阶数
        file_num (int): 文件个数
        lat (array): 纬度数组
        lon (array): 经度数组
        love_path (array): Love数文件路径

    Returns:
        array: 泄漏的等效水高
    """

    DeltaSC_filter = filter.gaussian_filter(DeltaSC_inverse,filter_radius,Lmax)
    DeltaC,DeltaS = sc_action_set.sc2singlesc(DeltaSC_filter,Lmax)
    mass_water_leakage = mass.mass(Lmax,file_num,DeltaC,DeltaS,lat,lon,love_path,1000)
    # mass_water_leakage = mass_water_leakage*np.reshape(np.repeat(ocean_mask, file_num, axis=1), (latlen, lonlen, -1), order='C')
    mass_water_leakage = mass_water_leakage*ocean_mask[:,:,None]


    return mass_water_leakage