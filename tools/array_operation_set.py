'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-11-15 15:51:51
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2023-07-10 10:22:18
FilePath: /ocean_change_python/tools/array_operation_set.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np

def swaplr(array):
    """左右调换数组

    Args:
        array (array): 目标数组
    """

    array_shape = np.shape(array)
    # asser expresssion [,arguments],如果不符合条件则抛出异常
    assert array_shape[1]%2==0,'列长度不能为奇数'
    midloc = array_shape[1]//2
    array_temp = np.zeros_like(array)
    array_temp[:,:midloc] = array[:,midloc:]
    array_temp[:,midloc:] = array[:,:midloc]

    return array_temp

def swapud(array):
    """上下调换数组

    Args:
        array (array): 目标数组
    """

    array_shape = np.shape(array)
    # asser expresssion [,arguments],如果不符合条件则抛出异常
    assert array_shape[0]%2==0,'行长度不能为奇数'
    midloc = array_shape[0]//2
    array_temp = np.zeros_like(array)
    array_temp[:midloc,:] = array[midloc:,:]
    array_temp[midloc:,:] = array[:midloc,:]

    return array_temp

def swap1dimlr_by_specifycol(array,specifycol=None):
    """一维数组左右调换

    Args:
        array (_type_): _description_
        specifycol (_type_): _description_
    """
    if specifycol is None:
        specifycol = len(array)//2
    array_temp = np.zeros_like(array)
    array_temp[:-specifycol] = array[specifycol:]
    array_temp[-specifycol:] = array[:specifycol]

    return array_temp

def swaplr_by_specifycol(array,specifycol):
    """指定列左右调换数组

    Args:
        array (array): 目标数组
        specifycol (int): 指定列，为右边数组的开头列，从开始
    """

    array_temp = np.zeros_like(array)
    array_temp[:,:-specifycol] = array[:,specifycol:]
    array_temp[:,-specifycol:] = array[:,:specifycol]

    return array_temp

def swapud_by_specifyrow(array,specifyrow):
    """指定行上下调换数组

    Args:
        array (array): 目标数组
        specifyrow (int): 指定行，为下行数组的处理行，从处理行处理
    """

    array_temp = np.zeros_like(array)
    array_temp[:-specifyrow,:] = array[specifyrow:,:]
    array_temp[-specifyrow:,:] = array[:specifyrow,:]

    return array_temp

def append_npz_data(filepath, **new_data):
    """向npz文件中添加数据

    Args:
        filepath (str): _description_
        new_data (unlimited): key1=value1,key2=value2
    """
    dataset = np.load(filepath, allow_pickle=True)
    np.savez(filepath, **dataset, **new_data)

def del_npz_data(filepath, *del_data):
    """删除npz文件中的数据

    Args:
        filepath (str): _description_
        del_data (unlimited): key1,key2,key3
    """
    dataset = np.load(filepath, allow_pickle=True)
    for key in del_data:
        dataset.pop(key)
    np.savez(filepath, **dataset)

def modify_npz_data(filepath, **new_data):
    """修改npz文件中的数据

    Args:
        filepath (str): _description_
        new_data (unlimited): key1=value1,key2=value2
    """
    try:
        dataset = np.load(filepath, allow_pickle=False)
    except:
        dataset = np.load(filepath, allow_pickle=True)
    new_ds = {key: value for key, value in dataset.items()}
    for key in new_data:
        new_ds[key] = new_data[key]
    np.savez(filepath, **new_ds)

def arrminmax(arr, ymin=-1, ymax=1):
    """
    归一化数组到[ymin, ymax]范围。

    参数:
        arr (numpy.ndarray): 要归一化的数组。
        ymin (float): 归一化范围的最小值，默认为-1。
        ymax (float): 归一化范围的最大值，默认为1。

    返回:
        numpy.ndarray: 归一化后的数组。
    """
    arr_min = arr.min()
    arr_max = arr.max()

    # 归一化到[0, 1]范围
    arr_normalized_0_1 = (arr - arr_min) / (arr_max - arr_min)

    # 将值映射到[ymin, ymax]范围
    arr_normalized = ymin + arr_normalized_0_1 * (ymax - ymin)

    return arr_normalized