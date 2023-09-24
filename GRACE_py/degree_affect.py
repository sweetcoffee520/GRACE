'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2023-06-14 19:07:01
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-07-30 17:51:29
FilePath: /ocean_change_python/GRACE_py/degree_affect.py
Description: 
'''
from GRACE_py.mass import mass,mass_degree
from GRACE_py import read_sh as rsh
from GRACE_py import region_grid as rgd
from GRACE_py import sc_action_set
from GRACE_py import replace_action_set
import numpy as np

def degree_affect(GAX_fold_path, file_flag, institute_flag, res_lonlat,love_path,degree_num):
    """计算SH数据不同阶的影响

    Args:
        GAX_fold_path (str): GAX数据的路径
        file_flag (str): 文件类型(GSM,GAA,GAC,GAD等)
        institute_flag (str): 机构名(CSR,GFZ,JPL)
        res_lonlat (float): 空间分辨率大小(0.25,0.5,1)
        love_path (str): love数路径
        degree_num (int): 阶数

    Returns:
        mass: 质量变化，等效水高形式，单位cm
    """

    if file_flag == 'GSM':
        Lmax, _, _, SC, _, file_num = rsh.read_sh(
            GAX_fold_path, 'GSM', 'A' , institute_flag)
    else:
        Lmax, _, _, SC, _, file_num = rsh.read_sh(
            GAX_fold_path, file_flag , 'C' , institute_flag)

    if res_lonlat == 0.25:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.875,
                                           89.875, 0.125, 359.875, res_lonlat)
    elif res_lonlat == 0.5:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.75,
                                           89.75, 0.25, 359.75, res_lonlat)
    elif res_lonlat == 1:
        lat, lon, _, _, _, _ = rgd.region_grid(-89.5, 89.5, 0.5, 359.5, res_lonlat)
    # SC_copy = np.zeros_like(SC)
    # SC_copy[degree_num,:] = SC[degree_num,:]
    DeltaSC = sc_action_set.sc2Deltasc_mascon(SC)
    DeltaC, DeltaS = sc_action_set.sc2singlesc(DeltaSC,Lmax)
    mass_copy = mass_degree(Lmax,file_num,DeltaC,DeltaS,lat,lon,love_path,1000,degree_num)

    return mass_copy

def degree1_diff(GSM_fold_path,degree1_path,institute_flag, res_lonlat, love_path):
    """_summary_

    Args:
        GSM_fold_path (_type_): _description_
        institute_flag (_type_): _description_
        res_lonlat (_type_): _description_
        love_path (_type_): _description_
        lat_range (_type_, optional): _description_. Defaults to None.
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

    SC_replace = replace_action_set.replace_degree1(SC, Lmax, degree1_path)
    DeltaSC_replace = sc_action_set.sc2Deltasc_mascon(SC_replace-SC)
    DeltaC, DeltaS = sc_action_set.sc2singlesc(DeltaSC_replace,Lmax)
    mass_replace = mass(1,file_num,DeltaC[:2,:2,:],DeltaS[:2,:2,:],lat,lon,love_path,1000)

    return mass_replace

def degree2_diff(GSM_fold_path,c20_path,institute_flag, res_lonlat, love_path):
    """_summary_

    Args:
        GSM_fold_path (_type_): _description_
        institute_flag (_type_): _description_
        res_lonlat (_type_): _description_
        love_path (_type_): _description_
        lat_range (_type_, optional): _description_. Defaults to None.
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

    SC_replace = replace_action_set.replace_c20_c30(SC, Lmax, c20_path)
    SC_replace[3,:] = SC[3,:]
    DeltaSC_replace = sc_action_set.sc2Deltasc_mascon(SC_replace-SC)
    DeltaC, DeltaS = sc_action_set.sc2singlesc(DeltaSC_replace,Lmax)
    mass_replace = mass(2,file_num,DeltaC[:3,:3,:],DeltaS[:3,:3,:],lat,lon,love_path,1000)

    return mass_replace