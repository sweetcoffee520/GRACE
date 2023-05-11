'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2021-10-30 17:17:57
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2022-10-15 20:49:37
FilePath: /ocean_change_python/GRACE_py/legendre.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np

# 递归法求勒让德函数，以下代码一次实现一个值，而且每次都需要递归，浪费内存和时间
# def legendre(l,m):
#     mlegendre[0,0,i] = 1
#     mlegendre[1,0,i] = np.sqrt(3)*t[i]
#     mlegendre[1,1,i] = np.sqrt(3*(1-t[i]**2))
#     if l>1:
#         # 从阶数为2开始，阶数小于2已经有初始值
#         if m<l and m!=l-1:
#             result = a[l,m]*t[i]*legendre(l-1,m)-a[l,m]/a[l-1,m]*legendre(l-2,m)
#             # result = ((2*(l-1)+1)*t[i]*legendre(l-1,m)-(l-1+m)*legendre(l-2,m))/(l+m)
#         elif m==l:
#             result = b[l]*np.sqrt(1-t[i]**2)*legendre(l-1,l-1)
#         elif m==l-1:
#             result = t[i]*np.sqrt(2*(l+1)-1)*legendre(l-1,l-1)
#         else:
#             result = 0
#     else:
#         if l==1 and m==1:
#             result = mlegendre[1,1,i]
#         if l==1 and m==0:
#             result = mlegendre[1,0,i]
#         if l==0 and m==0:
#             result = mlegendre[0,0,i]
#             result = 0
#     mlegendre[l,m,i] = result
#     return result
# legendre(60,60)

# 循环求所有纬度的勒让德函数
def legendre(Lmax,lat,latlen):
    # 余纬
    radlat = np.deg2rad(lat)
    mlegendre = np.zeros((Lmax+1,Lmax+1,latlen))
    t = np.cos(radlat)

    a = np.zeros((Lmax+1,Lmax+1))
    b = np.zeros(Lmax+1)

    for n in range(1,Lmax+1):
        m = np.arange(0,n)
        a[n,0:len(m)] = np.sqrt((2*n+1)*(2*n-1)/((n+m)*(n-m)))

    n = np.arange(2,Lmax+1)
    b[2:] = np.sqrt((2*n+1)/(2*n))
    b[1] = np.sqrt(3)
    mlegendre[0,0,:] = 1
    mlegendre[1,0,:] = np.sqrt(3)*t
    mlegendre[1,1,:] = np.sqrt(3*(1-np.square(t)))
    for i in range(0,latlen):
        for j in range(2,Lmax+1):
            for k in range(j+1):
                # mlegendre[0,0,i] = 1
                # mlegendre[1,0,i] = np.sqrt(3)*t[i]
                # mlegendre[1,1,i] = np.sqrt(3*(1-t[i]**2))
                if k==j:
                    mlegendre[j,k,i] = b[j]*np.sqrt(1-t[i]**2)*mlegendre[j-1,j-1,i]
                elif k==j-1:
                    mlegendre[j,k,i] = t[i]*np.sqrt(2*(j+1)-1)*mlegendre[j-1,j-1,i]
                else:
                    mlegendre[j,k,i] = a[j,k]*t[i]*mlegendre[j-1,k,i]-a[j,k]/a[j-1,k]*mlegendre[j-2,k,i]
    return mlegendre