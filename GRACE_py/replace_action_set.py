'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-06-03 13:23:19
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-07-29 18:41:22
FilePath: /ocean_change_python/GRACE_py/replace_action_set.py
Description: 

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
import re

def replace_c00(SC,SC_GAC,Lmax,Lmax_GAC):
    SC_new = SC.copy()
    SC_new[0,Lmax] = -SC_GAC[0,Lmax_GAC]

    return SC_new

def replace_degree1(sc,Lmax,degree1_path,*file_type):
    """替换一阶项

    Args:
        sc (array): sc形式数组
        Lmax (int): 最大阶数
        degree1_path (str): 一阶项替换文件路径
        file_type (替换的数据类型): GRACE,GRACE-FO,或者为空,表示两种数据联合

    Returns:
        [type]: [description]
    """
    with open(degree1_path,'r') as f:
        allcontent = f.read()

    sc_new = sc.copy()
    file_num = np.size(sc,2)
    #以两个及以上的=为分割符
    sp = re.split('={2,}',allcontent,1)

    filedata = re.split('\\s+',sp[1].strip())

    data_array = np.array(filedata).reshape(-1,9)
    line_len = np.size(data_array,0)
    #提出m=0和m=1的位置
    local_0 = np.arange(0,line_len,2)
    local_1 = np.arange(1,line_len,2)
    degree1_clm = np.zeros((len(local_0),2))
    degree1_slm = np.zeros((len(local_0),2))
    degree1_clm[:,0] = data_array[local_0,3]
    degree1_clm[:,1] = data_array[local_1,3]
    degree1_slm[:,0] = data_array[local_0,4]
    degree1_slm[:,1] = data_array[local_1,4]

    if not file_type or file_type[0] == '':
        sc_new[1, Lmax, :] = degree1_clm[0:file_num, 0]
        sc_new[1, Lmax+1,:] = degree1_clm[0:file_num, 1]
        sc_new[1, Lmax-1,:] = degree1_slm[0:file_num, 1]
    elif file_type[0] == 'GRACE':
        sc_new[1, Lmax, :] = degree1_clm[0:file_num, 0]
        sc_new[1, Lmax+1,:] = degree1_clm[0:file_num, 1]
        sc_new[1, Lmax-1,:] = degree1_slm[0:file_num, 1]
    elif file_type[0] == 'GRACE-FO':
        sc_new[1,Lmax, :] = degree1_clm[163:163+file_num, 0]
        sc_new[1, Lmax+1,:] = degree1_clm[163:163+file_num, 1]
        sc_new[1, Lmax-1,:] = degree1_slm[163:163+file_num, 1]

    return sc_new

def replace_c20_c30(sc,Lmax,c20_path,*file_type):
    """替换二阶项

    Args:
        sc (array): sc形式数组
        Lmax (int): 最大阶数
        c20_path (str): c20项替换文件路径
        file_type (替换的数据类型): GRACE,GRACE-FO,或者为空,表示两种数据联合

    Returns:
        [type]: [description]
    """
    with open(c20_path,'r') as p:
        allcontent = p.read()
        sp = allcontent.split('Product:',1)

    filedata = re.split('\\s+',sp[1].strip())
    file_num = np.size(sc,axis = 2)

    data_array = np.array(filedata,dtype=np.float64).reshape(-1,10)
    C20 = data_array[:,2]
    C30 = data_array[:,5]
    sc_new = sc.copy()

    if not file_type or file_type[0] == '':
        sc_new[2, Lmax,:] = C20[0:file_num]
        sc_new[3, Lmax,114:] = C30[114:file_num]
    elif 'GRACE' == file_type:
        sc_new[2, Lmax,:] = C20[0:file_num]
        sc_new[3, Lmax,114:] = C30[114:file_num]
    elif 'GRACE-FO' == file_type:
        sc_new[2, Lmax,:] = C20[163:163+file_num]
        # sc_new[3,:] = C30[163:163+file_num]
    return sc_new
