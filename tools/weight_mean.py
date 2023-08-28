'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-04-16 14:30:44
FilePath: /ocean_change_python/tools/weight_mean.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np

def latitudinal_weight(grd,lat,grd_mask=None):
    """纬度加权

    Args:
        grd (array): 被加权格网
        lat (array): 纬度数组
        grd_mask (array): 掩膜格网

    Returns:
        array: 加权后的值
    """

    lat_mask = np.cos(np.deg2rad(lat))
    if grd_mask is None:
        ave_result = np.sum(grd*lat_mask[:,None,None],(0,1))/np.sum(np.repeat(lat_mask,np.size(grd,1)))
    else:
        ave_result = np.sum(grd*lat_mask[:,None,None]*grd_mask[...,None],(0,1))/np.sum(lat_mask[:,None]*grd_mask)

    return ave_result

def latitudinal_weight_mask(grd,lat,grd_mask):
    """变化mask的纬度加权

    Args:
        grd (array): 被加权格网
        lat (array): 纬度数组,与grd大小相同
        grd_mask (array): 掩膜格网（每个月的mask不一样）

    Returns:
        array: 加权后的值
    """

    lat_mask = np.cos(np.deg2rad(lat))
    ave_result = np.sum(grd*lat_mask[:,None,None]*grd_mask,(0,1))/np.sum(lat_mask[:,None,None]*grd_mask,(0,1))

    return ave_result