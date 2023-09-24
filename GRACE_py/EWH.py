'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-07-29 18:49:31
FilePath: /ocean_change_python/GRACE_py/EWH.py
Description: calculate equivalent water height from GRACE data

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
from GRACE_py.mass import mass
from GRACE_py import read_sh as rsh
from GRACE_py import region_grid as rgd
from GRACE_py import sc_action_set
from GRACE_py import replace_action_set
from GRACE_py import destriping
from GRACE_py import filter
from GRACE_py import vertical_deformation as vd
import numpy as np


def GLOBAL_EWH(GSM_fold_path, institute_flag, res_lonlat, love_path, degree1_path, c20_path):
    """利用SH系数计算全球质量变化(等效水高表示)

    Args:
        GSM_fold_path (str): GSM文件路径
        rankflag (str): 文件等级(A->60,B->90,C->180)
        institute_flag (str): 数据机构(CSR,GFZ,JPL)
        res_lonlat (float): 分辨率大小
        love_path (str): 勒夫数文件路径
        degree1_path (str): 一阶项替换文件路径
        c20_path (_type_): c20项替换文件路径

    Returns:
        lat,lon (array): 经纬度数组
        EWH (array): 全球等效水高
    """
    Lmax, _, _, SC, _, file_num = rsh.read_sh(
        GSM_fold_path, 'GSM', 'A', institute_flag)
    if res_lonlat == 0.25:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.875,
                                           89.875, 0.125, 359.875, res_lonlat)
    elif res_lonlat == 0.5:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.75,
                                           89.75, 0.25, 359.75, res_lonlat)
    elif res_lonlat == 1:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.5, 89.5, 0.5, 359.5, res_lonlat)

    # 替换项
    SC = replace_action_set.replace_degree1(SC, Lmax, degree1_path)
    SC = replace_action_set.replace_c20_c30(SC, Lmax, c20_path)
    # 去条带处理
    SC_new = destriping.chen_destriping(SC, 20, 50, 5, Lmax)
    # 高斯滤波处理,先进行较小的高斯平滑
    DeltaSC = sc_action_set.sc2Deltasc_mascon(SC_new)
    DeltaSC_filter = filter.gaussian_filter(DeltaSC, 300, Lmax)
    DeltaC, DeltaS = sc_action_set.sc2singlesc(DeltaSC_filter, Lmax)

    EWH = mass(Lmax, file_num, DeltaC, DeltaS, lat, lon, love_path, 1000)

    return lat,lon,EWH


def vertical_deformation_EWH(GSM_fold_path, institute_flag, res_lonlat, love_path, degree1_path, c20_path):

    Lmax, _, _, SC, _, file_num = rsh.read_sh(GSM_fold_path, 'GSM', 'A', institute_flag)
    if res_lonlat == 0.25:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.875,
                                           89.875, 0.125, 359.875, res_lonlat)
    elif res_lonlat == 0.5:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.75,
                                           89.75, 0.25, 359.75, res_lonlat)
    elif res_lonlat == 1:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.5, 89.5, 0.5, 359.5, res_lonlat)

    # 替换项
    SC = replace_action_set.replace_degree1(SC, Lmax, degree1_path)
    SC = replace_action_set.replace_c20_c30(SC, Lmax, c20_path)
    # 去条带处理
    # SC_new = destriping.chen_destriping(SC, 20, 50, 5, Lmax)
    # 高斯滤波处理,先进行较小的高斯平滑
    DeltaSC = sc_action_set.sc2Deltasc_mascon(SC)
    DeltaSC_filter = filter.gaussian_filter(DeltaSC, 300, Lmax)
    DeltaC, DeltaS = sc_action_set.sc2singlesc(DeltaSC_filter, Lmax)

    vertical_def = vd.vertical_deformation(Lmax,file_num,DeltaC,DeltaS,lat,lon,love_path)

    return lat,lon,vertical_def