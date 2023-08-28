'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-06-03 12:57:12
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-08-07 23:57:24
FilePath: /ocean_change_python/GRACE_py/sc_action_set.py
Description: sc action set

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np

def sc2cs(sc,Lmax):
    file_num = np.size(sc,2)
    cs = np.zeros((Lmax+1,Lmax+1,file_num))
    for i in range(file_num):
        cs[:,:,i] = sc[:,Lmax:,i] + np.rot90(np.hstack((np.zeros((Lmax+1,1)),sc[:,0:Lmax,i])),1)

    return cs

def cs2sc(cs,Lmax):
    file_num = np.size(cs,2)
    sc = np.zeros((Lmax+1,2*Lmax+1,file_num))
    for i in range(file_num):

        sc[:,:,i] = np.hstack((np.rot90(np.triu(cs[:,:,i],1),-1)[:,1:],np.tril(cs[:,:,i])))

    return sc


def sc2singlesc(SC,Lmax):

    file_num = np.size(SC,axis=2)
    single_S = np.zeros((Lmax+1,Lmax+1,file_num))
    single_C = SC[:,Lmax:,:].copy()
    for i in range(file_num):
        single_S[:,:,i] = np.fliplr(np.append(SC[:,:Lmax,i],np.zeros((Lmax+1,1)),axis=1))

    return single_C,single_S

def sc2singlesc(SC,Lmax):

    file_num = np.size(SC,axis=2)
    single_S = np.zeros((Lmax+1,Lmax+1,file_num))
    single_C = SC[:,Lmax:,:].copy()
    for i in range(file_num):
        single_S[:,:,i] = np.fliplr(np.append(SC[:,:Lmax,i],np.zeros((Lmax+1,1)),axis=1))

    return single_C,single_S

def sc2Deltasc(SC):
    file_num = np.size(SC,axis=2)
    SC_sum = SC.sum(axis=2)
    SC_ave = SC_sum/file_num
    Delta_SC = SC - SC_ave[:,:,None]

    return Delta_SC

def sc2Deltasc_ocean(SC):
    """与GAD等产品做差数据保持一致

    Args:
        SC (_type_): _description_
        Lmax (_type_): _description_

    Returns:
        _type_: _description_
    """
    SC_ave = np.sum(SC[:,:,8:141],axis=2)/133

    Delta_SC = SC - SC_ave[:,:,None]
    return Delta_SC

def sc2Deltasc_mascon(SC):
    """与mascon数据时变数据一致，即减去2004.1-2009.12的平均值

    Args:
        SC (array): sc格式球谐系数
        Lmax (int): 最大阶数

    Returns:
        array: sc格式球谐系数
    """
    SC_ave = np.sum(SC[:,:,18:90],axis=2)/72

    Delta_SC = SC - SC_ave[:,:,None]
    return Delta_SC

def singlesc2sc(C, S, Lmax):
    """把C,S合并成SC形式
    Args:
        C (array): Clm的球谐系数阵
        S (array): Slm的球谐系数阵
        Lmax (int): 最大阶数
    Returns:
        array: SC数组
    """
    file_num = np.size(C,2)
    SC = np.zeros((Lmax+1,2*Lmax+1,file_num))
    SC[:,0:Lmax+1,:] = np.fliplr(S)
    SC[:,Lmax:,:] = C

    return SC