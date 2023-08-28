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


def ocean_EWH(GSM_fold_path,GAX_fold_path, GAX_rankflag, institute_flag, res_lonlat, mask, love_path, degree1_path, c20_path, GIA_correction,lat_range=None,replace_C00=False):
    """计算EWH

    Args:
        GSM_fold_path (str or list): GSM文件夹
        GAD_fold_path (str or list): GAD文件夹
        GAX_rankflag (str): 文件等级(A->60,B->90,C->180)
        institute_flag (str): 机构名(CSR,GFZ,JPL)
        res_lonlat (int): 分辨率大小
        mask (array): 海陆掩膜
        love_path (str): Love数文件路径
        degree1_path (str): 一阶项替换数据路径
        c20_path (str): c20项替换数据路径
        GIA_correction (array): GIA改正
        lat_range (tuple): 纬度范围
        replace_C00 (bool): 是否替换C00项

    Return:
        lat (array)
        lon (array)
        OcM (array)
    """

    Lmax, _, _, SC, _, file_num = rsh.read_sh(
        GSM_fold_path, 'GSM', 'A' , institute_flag)

    if res_lonlat == 0.25:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.875,
                                           89.875, 0.125, 359.875, res_lonlat)
    elif res_lonlat == 0.5:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.75,
                                           89.75, 0.25, 359.75, res_lonlat)
    elif res_lonlat == 1:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.5, 89.5, 0.5, 359.5, res_lonlat)

    lat_mask = np.cos(np.deg2rad(lat))
    # if institute_flag != 'CSR':
    #     _, _, GAA_EWH = GAX_EWH_Time_anomaly(GAX_fold_path,'GAA',GAX_rankflag,institute_flag,res_lonlat,love_path)
    #     GAA_mean = np.sum(GAA_EWH*lat_mask[:,None,None]*mask[...,None], axis=(0,1)) / np.sum(mask*lat_mask[:,None])
    # else:
    _, _, GAD_EWH = GAX_EWH_Time_anomaly(GAX_fold_path,'GAD',GAX_rankflag,institute_flag,res_lonlat,love_path)
    GAD_mean = np.sum(GAD_EWH*lat_mask[:,None,None]*mask[...,None], axis=(0,1)) / np.sum(mask*lat_mask[:,None])
    Lmax_GAC, _, _, SC_GAC, _, file_num = rsh.read_sh(GAX_fold_path,'GAC','C',institute_flag)
    # 替换项
    if replace_C00 == True:
        SC = replace_action_set.replace_c00(SC,SC_GAC,Lmax,Lmax_GAC)
    SC = replace_action_set.replace_degree1(SC, Lmax, degree1_path)
    SC = replace_action_set.replace_c20_c30(SC, Lmax, c20_path)
    # 去条带处理
    SC_new = destriping.chen_destriping(SC, 20, 55, 5, Lmax)
    # 高斯滤波处理,先进行较小的高斯平滑
    DeltaSC = sc_action_set.sc2Deltasc_mascon(SC_new)
    DeltaSC_filter = filter.gaussian_filter(DeltaSC, 300, Lmax)
    DeltaC, DeltaS = sc_action_set.sc2singlesc(DeltaSC_filter, Lmax)

    if lat_range is None:
        # if institute_flag != 'CSR':
            # OcM = mass(Lmax, file_num, DeltaC, DeltaS,lat, lon, love_path,1000) - GIA_correction[...,:file_num] + (GAD_EWH - GAA_mean[None,None,:])*mask[:,:,None]
        # else:
        OcM = mass(Lmax, file_num, DeltaC, DeltaS,lat, lon, love_path,1000) - GIA_correction[...,:file_num] + (GAD_EWH - GAD_mean[None,None,:])*mask[:,:,None]
    else:
        lat_loc = (lat>=lat_range[0]) & (lat<=lat_range[1])
        # if institute_flag != 'CSR':
        #     OcM = (mass(Lmax, file_num, DeltaC, DeltaS, lat, lon, love_path, 1000) -
        #         GIA_correction[..., :file_num] + GAD_EWH - GAA_mean[None, None, :]*mask[:,:,None])[lat_loc, ...]
        # else:
        OcM = (mass(Lmax, file_num, DeltaC, DeltaS, lat, lon, love_path, 1000) -
            GIA_correction[..., :file_num] + GAD_EWH - GAD_mean[None, None, :]*mask[:,:,None])[lat_loc, ...]

    return lat,lon,OcM

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


def GAX_EWH_Time_anomaly(GXX_fold_path, fileflag, rankflag, institute_flag, res_lonlat, love_path):
    """计算时间异常的GAX的全球等效水高

    Args:
        GXX_fold_path (str|list): GAX的文件路径
        fileflag (str): 文件标识(GAA,GAB,GAC,GAD)
        rankflag (str): 文件等级(A->60,B->90,C->180)
        institute_flag (str): 机构表示(CSR,GFZ,JPL)
        res_lonlat (float): 分辨率大小
        love_path (str): 勒夫数文件路径

    Returns:
        lat,lon (array): 经纬度数组
        EWH (array): 全球等效水高
    """
    Lmax, _, _, SC, _, file_num = rsh.read_sh(
    GXX_fold_path, fileflag, rankflag, institute_flag)
    if res_lonlat == 0.25:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.875,
                                           89.875, 0.125, 359.875, res_lonlat)
    elif res_lonlat == 0.5:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.75,
                                           89.75, 0.25, 359.75, res_lonlat)
    elif res_lonlat == 1:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.5, 89.5, 0.5, 359.5, res_lonlat)

    DeltaSC = sc_action_set.sc2Deltasc_mascon(SC)
    DeltaC, DeltaS = sc_action_set.sc2singlesc(DeltaSC, Lmax)

    EWH = mass(Lmax, file_num, DeltaC, DeltaS, lat, lon, love_path, 1000)

    return lat,lon,EWH

def GAX_EWH(GXX_fold_path, fileflag, rankflag, institute_flag, res_lonlat, love_path):
    """计算GAX的全球等效水高

    Args:
        GXX_fold_path (str|list): GAX的文件路径
        fileflag (str): 文件标识(GAA,GAB,GAC,GAD)
        rankflag (str): 文件等级(A->60,B->90,C->180)
        institute_flag (str): 机构表示(CSR,GFZ,JPL)
        res_lonlat (float): 分辨率大小
        love_path (str): 勒夫数文件路径

    Returns:
        lat,lon (array): 经纬度数组
        EWH (array): 全球等效水高
    """
    Lmax, _, _, SC, _, file_num = rsh.read_sh(
    GXX_fold_path, fileflag, rankflag, institute_flag)
    if res_lonlat == 0.25:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.875,
                                           89.875, 0.125, 359.875, res_lonlat)
    elif res_lonlat == 0.5:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.75,
                                           89.75, 0.25, 359.75, res_lonlat)
    elif res_lonlat == 1:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.5, 89.5, 0.5, 359.5, res_lonlat)

    DeltaC, DeltaS = sc_action_set.sc2singlesc(SC, Lmax)

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