'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-09-24 16:33:38
FilePath: /ocean_change_python/tools/fit_result_error.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
from . import fit_function as ff
from . import time_transfer as tt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def line_fit(t,y,t0=None):
    """计算趋势项拟合的结果及其误差

    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass
    if t0 is None:
        t = t-int(t[0])
    else:
        t = t-t0
    p = [1,1]
    popt,pcov = curve_fit(ff.line_trend,t,y,p0=p)
    # 1 sigma: 68.3% ; 2 sigma: 95.4%; 3 sigma: 99.7%，此处取2sigma，即95.4%的置信水平
    trend = popt[1]
    trend_std = 2*np.sqrt(pcov[1,1])

    return trend,trend_std

def annual_season_fit(t,y,t0=None,std=None):
    """计算带有周年和半周年项拟合的结果及其误差

    Returns:
        para(trend,Amplitudel,Amplitude2,Phase1,Phase2);Amplitude1:周年振幅,Amplitude22:半周年振幅,Phase1:周年相位,Phase2:半周年相位
        para_error(trend_std,Amplitudel_std,Amplitude2_std,Phase1_std,Phase2_std);Amplitude1_std:周年振幅误差,Amplitude2_std:半周年振幅误差,Phase1_std:周年相位误差,Phase2_std:半周年相位误差

    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass
    if t0 is None:
        t = t-int(t[0])
    else:
        t = t-t0

    if std is None:
        p = [1,1,1,1,1,1]
        popt,pcov = curve_fit(ff.annual_seasonal_trend,t,y,p0=p)

    else:
        P = np.diag(1/std[0]) #设置权阵，对角阵，为1/std
        A = np.zeros((len(y),6))
        A[:,0] = np.ones((len(y)))
        A[:,1] = t
        A[:,2] = np.sin(2*np.pi*t)
        A[:,3] = np.cos(2*np.pi*t)
        A[:,4] = np.sin(4*np.pi*t)
        A[:,5] = np.cos(4*np.pi*t)
        # NBB^-1的逆为QXX
        popt=np.linalg.inv(A.T@P@A)@A.T@P@y #(B^TPB)^-1*B^TPl
        fit_result = np.dot(A,para)
        residual =sum((y-fit_result)**2)/(len(y)-6)
        Qxx = np.linalg.inv(A.T@P@A)
        pcov = np.dot(residual,Qxx)

    # 1 sigma: 68.3% ; 2 sigma: 95.4%; 3 sigma: 99.7%，此处取2sigma，即95.4%的置信水平
    trend = popt[1]
    trend_std = 2*np.sqrt(pcov[1,1])
    Amplitudel = np.sqrt(popt[2]**2+popt[3]**2)
    Amplitudel_std = 2*np.sqrt((popt[2]**2*pcov[2,2]+popt[3]**2*pcov[3,3])/Amplitudel**2)
    if popt[2]>0: # 周年sin(phase)>0,相位phase in [0,pi]
        # 在极坐标系中，cos(phase) = x/r, sin(phase) = y/r, r = sqrt(x^2+y^2)
        Phase1 = np.arccos(popt[3]/Amplitudel)
    elif popt[2]<0:
        Phase1 = 2*np.pi-np.arccos(popt[3]/Amplitudel)
    elif popt[2]==0 and popt[3]==1:
        Phase1=0
    elif popt[2]==0 and popt[3]==-1:
        Phase1 = np.pi
    elif popt[2]==0 and popt[3]==0:
        Phase1=0
    Phase1 = np.rad2deg(Phase1)

    Amplitude2 = np.sqrt(popt[4]**2+popt[5]**2)
    Amplitude2_std = 2*np.sqrt((popt[4]**2*pcov[4,4]+popt[5]**2*pcov[5,5])/Amplitude2**2)
    if popt[4]>0: #半周年sin(phase)>0,相位phase in [0,pi]
        Phase2 = np.arccos(popt[5]/Amplitude2)
    elif popt[4]<0:
        Phase2 = 2*np.pi-np.arccos(popt[5]/Amplitude2)
    elif popt[4]==0 and popt[5]==1:
        Phase2=0
    elif popt[4]==0 and popt[5]==-1:
        Phase2 = np.pi
    elif popt[4]==0 and popt[5]==0:
        Phase2=0
    Phase2 = np.rad2deg(Phase2)

    if abs(popt[2])>=abs(popt[3]): #周年sin>cos
        x_32 = popt[3]/popt[2]
        # arccos(x)的误差传播定律为：2*sqrt((1-x^2)*dx^2),1/x的误差传播定律
        Phase1_std = np.rad2deg(2*np.sqrt((x_32**2-x_32**4+x_32**6-x_32**8+x_32**10)**2*((popt[2]/popt[3]**2)**2*pcov[3,3]+(1/popt[3])**2*pcov[2,2])))
    else:
        x_23 = popt[2]/popt[3]
        Phase1_std = np.rad2deg(2*np.sqrt((1-x_23**2+x_23**4-x_23**6+x_23**8-x_23**10)**2*((popt[2]/popt[3]**2)**2*pcov[3,3]+(1/popt[3])**2*pcov[2,2])))
    #FIXME:半周年的相位误差计算有问题，待修正
    if abs(popt[4])>=abs(popt[5]): #半周年sin>cos
        x_54 = popt[5]/popt[4]
        Phase2_std = np.rad2deg(2*np.sqrt((x_54**2-x_54**4+x_54**6-x_54**8+x_54**10)**2*((popt[4]/popt[5]**2)**2*pcov[5,5]+(1/popt[5])**2*pcov[4,4])))
    else:
        x_45 = popt[4]/popt[5]
        Phase2_std = np.rad2deg(2*np.sqrt((1-x_45**2+x_45**4-x_45**6+x_45**8-x_45**10)**2*((popt[4]/popt[5]**2)**2*pcov[5,5]+(1/popt[5])**2*pcov[4,4])))

    para = (trend,Amplitudel,Amplitude2,Phase1,Phase2)
    para_error = (trend_std,Amplitudel_std,Amplitude2_std,Phase1_std,Phase2_std)

    return para,para_error

def polynomial_harmonic_fit(x, y, degree, n_harmonics):
    '''
    多项式和谐波拟合函数。
    '''
    if isinstance(x,pd.DatetimeIndex):
        x = tt.dateseries_to_timeseries(x)
    else:
        pass
    # 多项式拟合
    popt_poly,_ = curve_fit(ff.polynomial, x, y, p0=[0.0]*(degree+1))

    # 谐波拟合
    p0_harmonic = [y.mean()] + [0.0]*(2*n_harmonics)
    popt_harmonic, _ = curve_fit(ff.harmonic, x, y, p0=p0_harmonic)

    # 返回拟合结果
    return popt_poly,popt_harmonic