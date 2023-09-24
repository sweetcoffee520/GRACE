'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2021-12-08 17:04:10
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2022-10-18 22:49:12
FilePath: /ocean_change_python/GRACE_py/truncation.py
Description: truncate spherical harmonic coefficients

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
def truncation(sc,cut_num,Lmax):
    '''
    截断球谐系数
    '''
    sc_new = sc[0:cut_num+1,Lmax-cut_num:Lmax+cut_num+1,:].copy()
    return sc_new
