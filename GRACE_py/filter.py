'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2022-06-28 19:37:03
FilePath: /ocean_change_python/GRACE_py/filter.py
Description: 计算高斯滤波

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np

def gaussian_filter(SC,radius,Lmax):
    """高斯滤波

    Args:
        SC (array): [description]
        radius (int): 滤波半径
        Lmax (int): 最大阶数

    Returns:
        array: 滤波后的sc
    """

    file_num = np.size(SC,2)
    SC_filter = np.zeros((Lmax+1,2*Lmax+1,file_num))
    w = np.zeros(Lmax+1)
    # b = np.log(2)/(1-np.cos(radius*1000/a))

    # john wahr 高斯滤波
    # w[0] = 1
    # w[1] = (1+np.e**(-2*b))/(1-np.e**(-2*b))-1/b
    # for i in range(2,len(w)):
    #     w[i] = -((2*(i-1)+1)/b*w[i-1])+w[i-2]

    # b = np.log(2)/(1-np.cos(radius*1000/a))
    # w[0] = 1/(2*np.pi)
    # w[1] = 1/(2*np.pi)*((1+np.e**(-2*b))/(1-np.e**(-2*b))-1/b)
    # for i in range(2,len(w)):
    #     w[i] = -((2*(i-1)+1)/b*w[i-1])+w[i-2]

    for i in range(Lmax+1):
        w[i] = np.exp(-(i*radius/6371)**2/(4*np.log(2)))


    SC_filter = SC*w[:,None,None]

    return SC_filter

def Fan_filter(SC, radius, Lmax):

    file_num = np.size(SC, 2)
    SC_filter = np.zeros((Lmax+1, 2*Lmax+1, file_num))
    wl = np.zeros(Lmax+1)
    wm = np.zeros(2*Lmax+1)

    for i in range(Lmax+1):
        wl[i] = np.exp(-(i*radius/6371)**2/(4*np.log(2)))
    wm = np.hstack((wl[::-1][1:],wl))
    # aa = np.reshape(np.repeat(w, Lmax+1), (Lmax+1, -1), order='F')
    # bb = np.hstack((np.fliplr(aa[:, 1:]), aa))
    # cc = np.reshape(np.repeat(bb, file_num, axis=1),
    #                 (Lmax+1, -1, file_num), order='C')

    SC_filter = SC*wm[None,:,None]*wl[:, None, None]

    return SC_filter