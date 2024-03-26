'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2023-07-03 13:34:52
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2024-03-26 22:33:04
FilePath: /ocean_change_python/GRACE_py/destriping.py
Description: destriping from SC

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
import numpy as np

# 保持前start_ord次的不变，去除start_ord次后阶的相关性
def chen_destriping(SC, start_ord, end_ord, poly_ord, Lmax):
    '''
    startorder: 开始的次数
    endorder: 结束的次数
    poly_ord: 多项式阶数
    '''

    file_num = np.size(SC, axis=2)
    SC_d = np.zeros((Lmax+1, 2*Lmax+1, file_num))
    clm_result = np.zeros((Lmax+1))
    slm_result = np.zeros((Lmax+1))

    for i in range(file_num):
        # 循环次
        for j in range(start_ord, end_ord+1):

            clm_result[:] = 0
            slm_result[:] = 0
            n = np.arange(j, Lmax+1, 2)

            clm = SC[n, Lmax+j, i]
            slm = SC[n, Lmax-j, i]

            # 多线性估计，估计多项式前系数，返回系数矩阵。poly_ord为最高次，clm为每个点所对应的值，n为点的大小(位置)值
            poly_clm = np.polyfit(n, clm, poly_ord)
            poly_slm = np.polyfit(n, slm, poly_ord)

            # 多项式求值，用poly_clm为系数的多次多项式，求得n点的值
            clm_result[n] = np.polyval(poly_clm, n)
            slm_result[n] = np.polyval(poly_slm, n)

            n = np.arange(j+1, Lmax+1, 2)
            clm = SC[n, Lmax+j, i]
            slm = SC[n, Lmax-j, i]

            # 多线性估计，估计多项式前系数，返回系数矩阵。poly_ord为最高次，clm为每个点所对应的值，n为点的大小(位置)值
            poly_clm = np.polyfit(n, clm, poly_ord)
            poly_slm = np.polyfit(n, slm, poly_ord)

            # 多项式求值，用poly_clm为系数的多次多项式，求得n点的值
            clm_result[n] = np.polyval(poly_clm, n)
            slm_result[n] = np.polyval(poly_slm, n)

            SC_d[:, Lmax+j, i] = clm_result
            SC_d[:, Lmax-j, i] = slm_result

    SC_new = SC - SC_d

    # for i in range(endorder+1,Lmax+1):
    # SC_new[:, Lmax+end_ord+1:, :] = 0
    # SC_new[:, :Lmax-end_ord, :] = 0

    return SC_new


# 保持前start_deg阶的不变，只去除start_deg阶之后阶的相关性，从start_ord次开始
def chambers_destriping(SC, start_deg, end_ord, poly_ord, Lmax):
    """chambers方法的去相关滤波

    Args:
        SC (array): SC形状数组
        start_deg (int): 开始的阶数
        end_ord (int): 最大的次数
        poly_ord (int): 多项式阶数
        Lmax (int): 最大阶数

    Returns:
        array: 去条带滤波之后的SC形状数组
    """
    file_num = np.size(SC, axis=2)
    SC_d = np.zeros((Lmax+1, 2*Lmax+1, file_num))
    clm_result = np.zeros((Lmax+1))
    slm_result = np.zeros((Lmax+1))

    for i in range(file_num):
        # 循环次
        for j in range(0, end_ord+1):
            # 如果次大于start_deg的值，那么就从j次开始往下滤波，否则从start_deg大小的次往下滤波
            if j > start_deg:

                clm_result[:] = 0
                slm_result[:] = 0
                n = np.arange(j, Lmax+1, 2)

                clm = SC[n, Lmax+j, i]
                slm = SC[n, Lmax-j, i]

                # 多线性估计，估计多项式前系数，返回系数矩阵。poly_ord为最高次，clm为每个点所对应的值，n为点的大小(位置)值
                poly_clm = np.polyfit(n, clm, poly_ord)
                poly_slm = np.polyfit(n, slm, poly_ord)

                # 多项式求值，用poly_clm为系数的多次多项式，求得n点的值
                clm_result[n] = np.polyval(poly_clm, n)
                slm_result[n] = np.polyval(poly_slm, n)

                n = np.arange(j+1, Lmax+1, 2)
                clm = SC[n, Lmax+j, i]
                slm = SC[n, Lmax-j, i]

                # 多线性估计，估计多项式前系数，返回系数矩阵。poly_ord为最高次，clm为每个点所对应的值，n为点的大小(位置)值
                poly_clm = np.polyfit(n, clm, poly_ord)
                poly_slm = np.polyfit(n, slm, poly_ord)

                # 多项式求值，用poly_clm为系数的多次多项式，求得n点的值
                clm_result[n] = np.polyval(poly_clm, n)
                slm_result[n] = np.polyval(poly_slm, n)

                SC_d[:, Lmax+j, i] = clm_result
                SC_d[:, Lmax-j, i] = slm_result

            else:

                clm_result[:] = 0
                slm_result[:] = 0
                n = np.arange(start_deg, Lmax+1, 2)

                clm = SC[n, Lmax+j, i]
                slm = SC[n, Lmax-j, i]

                # 多线性估计，估计多项式前系数，返回系数矩阵。poly_ord为最高次，clm为每个点所对应的值，n为点的大小(位置)值
                poly_clm = np.polyfit(n, clm, poly_ord)
                poly_slm = np.polyfit(n, slm, poly_ord)

                # 多项式求值，用poly_clm为系数的多次多项式，求得n点的值
                clm_result[n] = np.polyval(poly_clm, n)
                slm_result[n] = np.polyval(poly_slm, n)

                n = np.arange(start_deg+1, Lmax+1, 2)
                clm = SC[n, Lmax+j, i]
                slm = SC[n, Lmax-j, i]

                # 多线性估计，估计多项式前系数，返回系数矩阵。poly_ord为最高次，clm为每个点所对应的值，n为点的大小(位置)值
                poly_clm = np.polyfit(n, clm, poly_ord)
                poly_slm = np.polyfit(n, slm, poly_ord)

                # 多项式求值，用poly_clm为系数的多次多项式，求得n点的值
                clm_result[n] = np.polyval(poly_clm, n)
                slm_result[n] = np.polyval(poly_slm, n)

                SC_d[:, Lmax+j, i] = clm_result
                SC_d[:, Lmax-j, i] = slm_result

        # for j in range(start_ord):

        #     clm_result[:] = 0
        #     slm_result[:] = 0
        #     n = np.arange(start_deg,end_deg+1,2)

        #     clm = SC[n,Lmax+1+j,i]
        #     slm = SC[n,Lmax+1-j,i]

        #     # 多线性估计，估计多项式前系数，返回系数矩阵。poly_ord为最高次，clm为每个点所对应的值，n为点的大小(位置)值
        #     poly_clm = np.polyfit(n,clm,poly_ord)
        #     poly_slm = np.polyfit(n,slm,poly_ord)

        #     # 多项式求值，用poly_clm为系数的多次多项式，求得n点的值
        #     clm_result[n] = np.polyval(poly_clm,n)
        #     slm_result[n] = np.polyval(poly_slm,n)

        #     n = np.arange(start_deg+1,end_deg+1,2)
        #     clm = SC[n,Lmax+1+j,i]
        #     slm = SC[n,Lmax+1-j,i]

        #     # 多线性估计，估计多项式前系数，返回系数矩阵。poly_ord为最高次，clm为每个点所对应的值，n为点的大小(位置)值
        #     poly_clm = np.polyfit(n,clm,poly_ord)
        #     poly_slm = np.polyfit(n,slm,poly_ord)

        #     # 多项式求值，用poly_clm为系数的多次多项式，求得n点的值
        #     clm_result[n] = np.polyval(poly_clm,n)
        #     slm_result[n] = np.polyval(poly_slm,n)

        #     SC_d[:,Lmax+1+j,i] = clm_result
        #     SC_d[:,Lmax+1-j,i] = slm_result

    SC_new = SC - SC_d

    # for i in range(end_ord+1, Lmax+1):
    #     SC_new[:, Lmax+i, :] = 0
    #     SC_new[:, Lmax-i, :] = 0

    return SC_new


def swenson_destriping(SC, start_deg, end_deg, start_ord, end_ord, poly_ord, Lmax):
    """去相关滤波swenson方法

    Args:
        SC (array): 球谐系数
        start_deg (int): 开始阶数
        end_deg (int): 结束阶数
        start_ord (int): 开始次数
        end_ord (int): 结束次数
        poly_ord (int): 平滑阶数
        Lmax (int): 最大阶数

    Returns:
        array: 去条带之后的SC形式球谐系数
    """
    file_num = np.size(SC,2)
    SC_s = np.zeros((Lmax+1, 2*Lmax+1, file_num))
    # 球谐系数不变的部分
    SC_s[end_ord:end_deg+1, :, :] = SC[end_ord:end_deg+1, :, :]
    for i in range(file_num):
        for m in range(start_ord-1, end_ord+1):
            clm_col_s = np.zeros(Lmax+1)
            slm_col_s = np.zeros(Lmax+1)

            # 如果值小于5，那么设置为5
            nsmooth = max(np.round(30*np.exp(-m/10)+1).astype(int), 5)
            # 如果次为end_ord，那么直接平滑之后所有的奇（偶）项
            if m == end_ord:
                llvec = np.arange(m, Lmax+1, 2)
            else:
                if m > start_deg:
                    llvec = np.arange(m, end_deg+1)
                else:
                    llvec = np.arange(start_deg, end_deg+1)
            # 对每一次中需要平滑的阶进行平滑
            for l in llvec:
                if l-(nsmooth-1) <= m:
                    # 偶数阶
                    if np.mod(l, 2) == 0:
                        if np.mod(m, 2) == 0:
                            n = np.arange(m, m+(nsmooth-1)*2+1, 2)
                        else:
                            n = np.arange(m+1,m+1+(nsmooth-1)*2+1,2)
                    # 奇数阶
                    else:
                        if np.mod(m, 2) == 0:
                            n = np.arange(m+1,m+1+(nsmooth-1)*2+1,2)
                        else:
                            n = np.arange(m, m+(nsmooth-1)*2+1, 2)
                else:
                    if np.mod(nsmooth,2)==0:
                        if l+nsmooth<=end_deg:
                            n = np.arange(l-nsmooth+2,l+nsmooth+1,2)
                        else:
                            if np.mod(l,2)==0:
                                n = np.arange(end_deg-(nsmooth-1)*2,end_deg+1,2)
                            else:
                                n = np.arange(end_deg-1-(nsmooth-1)*2,end_deg,2)
                    else:
                        if l+nsmooth-1<=end_deg:
                            n = np.arange(l-nsmooth+1,l+nsmooth,2)
                        else:
                            if np.mod(l,2)==0:
                                n = np.arange(end_deg-(nsmooth-1)*2,end_deg+1,2)
                            else:
                                n = np.arange(end_deg-1-(nsmooth-1)*2,end_deg,2)

                clm = SC[n, Lmax+m, i]
                slm = SC[n, Lmax-m, i]

                poly_clm = np.polyfit(n,clm,poly_ord)
                poly_slm = np.polyfit(n,slm,poly_ord)
                clm_col_s[l] = np.polyval(poly_clm,l)
                slm_col_s[l] = np.polyval(poly_slm,l)

            SC_s[:,Lmax+m,i] = clm_col_s
            SC_s[:,Lmax-m,i] = slm_col_s

        for m in range(0,start_ord):
            clm_col_s = np.zeros(Lmax+1)
            slm_col_s = np.zeros(Lmax+1)

            nsmooth = max(np.round(30*np.exp(-m/10)+1).astype(int), 5)

            llvec = np.arange(start_deg,end_deg+1)

            for l in llvec:
                if l-(nsmooth-1) <= start_deg:
                    # 偶数阶
                    if np.mod(l, 2) == 0:
                        if np.mod(start_deg, 2) == 0:
                            n = np.arange(start_deg, start_deg+(nsmooth-1)*2+1, 2)
                        else:
                            n = np.arange(start_deg+1,start_deg+1+(nsmooth-1)*2+1,2)
                    # 奇数阶
                    else:
                        if np.mod(start_deg, 2) == 0:
                            n = np.arange(start_deg+1,start_deg+1+(nsmooth-1)*2+1,2)
                        else:
                            n = np.arange(start_deg, start_deg+(nsmooth-1)*2+1, 2)
                else:
                    if np.mod(nsmooth,2)==0:
                        if l+nsmooth<=end_deg:
                            n = np.arange(l-nsmooth+2,l+nsmooth+1,2)
                        else:
                            if np.mod(l,2)==0:
                                n = np.arange(end_deg-(nsmooth-1)*2,end_deg+1,2)
                            else:
                                n = np.arange(end_deg-1-(nsmooth-1)*2,end_deg,2)
                    else:
                        if l+nsmooth-1<=end_deg:
                            n = np.arange(l-nsmooth+1,l+nsmooth,2)
                        else:
                            if np.mod(l,2)==0:
                                n = np.arange(end_deg-(nsmooth-1)*2,end_deg+1,2)
                            else:
                                n = np.arange(end_deg-1-(nsmooth-1)*2,end_deg,2)

                n_s = np.delete(n,np.where((n>Lmax)|(n<0)))

                clm = SC[n_s,Lmax+m,i]
                slm = SC[n_s,Lmax-m,i]

                poly_clm = np.polyfit(n_s,clm,poly_ord)
                poly_slm = np.polyfit(n_s,slm,poly_ord)
                clm_col_s[l] = np.polyval(poly_clm,l)
                slm_col_s[l] = np.polyval(poly_slm,l)

            SC_s[:,Lmax+m,i] = clm_col_s
            SC_s[:,Lmax-m,i] = slm_col_s

    SC_new = SC-SC_s

    return SC_new