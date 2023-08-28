'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-10-15 20:49:09
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-04-24 20:55:36
FilePath: /ocean_change_python/GRACE_py/earth_function.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2023 by ${git_name_email}, All Rights Reserved.
'''
import re
import numpy as np
from GRACE_py import constant
def original_legendre(maxn,x):
    P = np.zeros((maxn+1,len(x)))
    P[0,:] = 1
    P[1,:] = x
    for i in range(2,maxn+1):
        P[i,:] = ((2*(i-1)+1)*x*P[i-1,:] - (i-1)*P[i-2,:])/i

    return P

def gamma(maxn,x,legd):
    F = np.zeros((maxn+1,len(x)))
    F[0,:] = (1-np.cos(x))/2
    for i in range(maxn+1):
        F[i,:] = ((legd[i-1,:]-legd[i+1,:]))/2

    return F

def Sup(Lmax,x,love_path):
    legd = original_legendre(Lmax+1,x)
    gam = gamma(Lmax,x)
    with open(love_path,'r') as f:
        all_content = f.read()
        data = np.array(re.split('#\n',all_content)[1].split()).reshape(-1,4).astype(np.float64)
    loveN_k = data[:,3]
    loveN_k[1] = 0.026
    loveN_h = data[:,1]
    Sup = (loveN_h[:Lmax+1]@gam*4*np.pi*constant.earth_constants.G*constant.earth_constants.a*legd)/(constant*constant.earth_constants.g*2*(np.arange(Lmax+1)[:,None]+1))

    return Sup