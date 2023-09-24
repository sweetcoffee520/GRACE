'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2021-10-30 17:17:57
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-07-29 23:43:29
FilePath: /ocean_change_python/GRACE_py/legendre.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
from scipy.special import lpmv,factorial

# 循环求所有纬度的正则化勒让德函数
def normalized_legendre(Lmax,lat):
    # 余纬
    lat = np.atleast_1d(lat)
    radlat = np.deg2rad(lat)
    latlen = len(lat)
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

def assoc_legendre(degree, x):
    """
    计算关联勒让德多项式。
    参数：
        degree: 整数，表示勒让德多项式的阶数
        x: 数字或数字的 numpy 数组，表示要在其上计算勒让德多项式的点
        normalize: 布尔值，表示是否进行正则化，默认为 False
    返回：
        关联勒让德多项式在点 x 上的值
    """

    x = np.atleast_1d(x)
    m = np.arange(degree+1)[:,None]
    n = np.arange(degree+1)[None,:]
    result = np.zeros((degree+1,degree+1, len(x)))
    # 计算勒让德多项式的系数
    for i in range(len(x)):
        result[...,i] = lpmv(m, n, x[i])

    return result

def legendre(l, x, NORMALIZE=False):
    """
    Computes associated Legendre functions for a particular degree
    following [Abramowitz1965]_ and [Jacobs1987]_

    Parameters
    ----------
    l: int
        degree of Legrendre polynomials
    x: np.ndarray
        elements ranging from -1 to 1

        Typically ``cos(theta)``, where ``theta`` is the colatitude in radians
    NORMALIZE: bool, default False
        Fully-normalize the Legendre Functions

    Returns
    -------
    Pl: np.ndarray
        legendre polynomials of degree ``l``

    References
    ----------
    .. [Abramowitz1965] M. Abramowitz and I. A. Stegun,
        *Handbook of Mathematical Functions*, 1046 pp., (1965).

    .. [Jacobs1987] J. A. Jacobs, *Geomagnetism*,
        Volume 1, 1st Edition, 832 pp., (1987).
    """
    # verify integer
    l = np.int64(l)
    # verify dimensions
    x = np.atleast_1d(x).flatten()
    # size of the x array
    nx = len(x)

    # for the l = 0 case
    if (l == 0):
        Pl = np.ones((1,nx), dtype=np.float64)
        return Pl

    # for all other degrees greater than 0
    rootl = np.sqrt(np.arange(0,2*l+1))# +1 to include 2*l
    # s is sine of colatitude (cosine of latitude) so that 0 <= s <= 1
    s = np.sqrt(1.0 - x**2)# for x=cos(th): s=sin(th)
    P = np.zeros((l+3,nx), dtype=np.float64)

    # Find values of x,s for which there will be underflow
    sn = (-s)**l
    tol = np.sqrt(np.finfo(np.float64).tiny)
    count = np.count_nonzero((s > 0) & (np.abs(sn) <= tol))
    if (count > 0):
        ind, = np.nonzero((s > 0) & (np.abs(sn) <= tol))
        # Approximate solution of x*ln(x) = Pl
        v = 9.2 - np.log(tol)/(l*s[ind])
        w = 1.0/np.log(v)
        m1 = 1+l*s[ind]*v*w*(1.0058+ w*(3.819 - w*12.173))
        m1 = np.where(l < np.floor(m1), l, np.floor(m1)).astype(np.int64)
        # Column-by-column recursion
        for k,mm1 in enumerate(m1):
            col = ind[k]
            # Calculate twocot for underflow case
            twocot = -2.0*x[col]/s[col]
            P[mm1-1:l+1,col] = 0.0
            # Start recursion with proper sign
            tstart = np.finfo(np.float64).eps
            P[mm1-1,col] = np.sign(np.fmod(mm1,2)-0.5)*tstart
            if (x[col] < 0):
                P[mm1-1,col] = np.sign(np.fmod(l+1,2)-0.5)*tstart
            # Recur from m1 to m = 0, accumulating normalizing factor.
            sumsq = tol.copy()
            for m in range(mm1-2,-1,-1):
                P[m,col] = ((m+1)*twocot*P[m+1,col] - \
                    rootl[l+m+2]*rootl[l-m-1]*P[m+2,col]) / \
                    (rootl[l+m+1]*rootl[l-m])
                sumsq += P[m,col]**2
            # calculate scale
            scale = 1.0/np.sqrt(2.0*sumsq - P[0,col]**2)
            P[0:mm1+1,col] = scale*P[0:mm1+1,col]

    # Find the values of x,s for which there is no underflow, and (x != +/-1)
    count = np.count_nonzero((x != 1) & (np.abs(sn) >= tol))
    if (count > 0):
        nind, = np.nonzero((x != 1) & (np.abs(sn) >= tol))
        # Calculate twocot for normal case
        twocot = -2.0*x[nind]/s[nind]
        # Produce normalization constant for the m = l function
        d = np.arange(2,2*l+2,2)
        c = np.prod(1.0 - 1.0/d)
        # Use sn = (-s)**l (written above) to write the m = l function
        P[l,nind] = np.sqrt(c)*sn[nind]
        P[l-1,nind] = P[l,nind]*twocot*l/rootl[-1]

        # Recur downwards to m = 0
        for m in range(l-2,-1,-1):
            P[m,nind] = (P[m+1,nind]*twocot*(m+1) - \
                P[m+2,nind]*rootl[l+m+2]*rootl[l-m-1]) / \
                (rootl[l+m+1]*rootl[l-m])

    # calculate Pl from P
    Pl = np.copy(P[0:l+1,:])

    # Polar argument (x == +/-1)
    count = np.count_nonzero(s == 0)
    if (count > 0):
        s0, = np.nonzero(s == 0)
        Pl[0,s0] = x[s0]**l

    # calculate Fully Normalized Associated Legendre functions
    if NORMALIZE:
        norm = np.zeros((l+1))
        norm[0] = np.sqrt(2.0*l+1)
        m = np.arange(1,l+1)
        norm[1:] = (-1)**m*np.sqrt(2.0*(2.0*l+1.0))
        Pl *= np.kron(np.ones((1,nx)), norm[:,np.newaxis])
    else:
        # Calculate the unnormalized Legendre functions by multiplying each row
        # by: sqrt((l+m)!/(l-m)!) == sqrt(prod(n-m+1:n+m))
        # following Abramowitz and Stegun
        for m in range(1,l):
            Pl[m,:] *= np.prod(rootl[l-m+1:l+m+1])
        # sectoral case (l = m) should be done separately to handle 0!
        Pl[l,:] *= np.prod(rootl[1:])

    return Pl