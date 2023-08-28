'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-06-11 11:15:32
FilePath: /ocean_change_python/tools/fit_function.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2023 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
import pandas as pd
from . import time_transfer as tt

def annual_seasonal_trend(t, *p):
    """带有周年项和半周年项的拟合函数

    Args:
        t (numpy.dtype(float)): 时间数组
    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass
    return p[0]+p[1]*t+p[2]*np.sin(2*np.pi*t)+p[3]*np.cos(2*np.pi*t)+p[4]*np.sin(4*np.pi*t)+p[5]*np.cos(4*np.pi*t)

def seasonal_trend(t, *p):
    """带有周年项的拟合函数

    Args:
        t (numpy.dtype(float)): 时间数组
    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass
    return p[0]+p[1]*t+p[2]*np.sin(2*np.pi*t)+p[3]*np.cos(2*np.pi*t)

def line_trend(t, *p):
    """只有线性项的拟合函数

    Args:
        t (numpy.dtype(float)): 时间数组
    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass
    return p[0]+p[1]*t

def seasonal_cycle(t, *p):
    """只有周年和半周年项的拟合函数

    Args:
        t (_type_): _description_
    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass
    return p[0]*np.sin(2*np.pi*t)+p[1]*np.cos(2*np.pi*t)+p[2]*np.sin(4*np.pi*t)+p[3]*np.cos(4*np.pi*t)

def acceleration(t, *p):
    """带有线性项和加速度项的拟合函数

    Args:
        t (numpy.dtype(float)): 时间数组
    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    return p[0]+p[1]*t+p[2]*t**2

def polynomial(t, *coefficients):
    '''
    多项式拟合函数。
    '''
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass
    degree = len(coefficients)-1
    y = 0
    for i in range(degree):
        y += coefficients[i] * t**(degree-i)
    y += coefficients[-1]
    return y

def harmonic(t, *coefficients):
    '''
    谐波拟合函数。
    '''
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass
    n_harmonics = len(coefficients) // 2
    y = 0
    for i in range(n_harmonics):
        y += coefficients[2*i] * np.sin((i+1)*np.pi*t) + coefficients[2*i+1] * np.cos((i+1)*np.pi*t)
    return y