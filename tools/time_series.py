import numpy as np

from .polygon import inpolygon
from . import weight_mean
from . import fit_function as ff
from scipy.optimize import curve_fit
from . import extract_function
from . import time_transfer as tt
from scipy.fft import fft, ifft, fftfreq
from tools import longitude_range as lr
import pandas as pd


def grd_series_latitudinal(grd, nannum, lat, lat_range=None):
    """ 计算mask之后的时间序列,纬度加权

    Args:
        grd (array): 格网数组
        lat (array): 纬度数组
        lat_range (tuple): 纬度范围
        nannum (float or int): 无效值大小

    Returns:
        array: 时间序列
    """
    row,col,_ = np.shape(grd)
    mask = np.ones((row,col))
    mask[grd[...,0]==nannum] = 0
    if lat_range is None:
        weighted_ave = weight_mean.latitudinal_weight(grd, lat, mask)
    else:
        loc = (lat>=lat_range[0])&(lat<=lat_range[1])
        weighted_ave = weight_mean.latitudinal_weight(grd[loc,:,:], lat[loc], mask[loc,:])
    return weighted_ave

def series_latitudinal(grd, mask, lat, lat_range=None):
    """计算给定格网的时间序列，纬度加权

    Args:
        grd (array): 格网数组
        mask (array): 掩膜格网数组
        lat (array): 纬度数组
        lat_range (tuple): 纬度范围

    Returns:
        array: 时间序列
    """
    if lat_range is None:
        weighted_average = weight_mean.latitudinal_weight(grd, lat, mask)
    else:
        loc = (lat>=lat_range[0])&(lat<=lat_range[1])
        weighted_average = weight_mean.latitudinal_weight(grd[loc,:,:], lat[loc], mask[loc,:])

    return weighted_average

def series_latitudinal_mask(grd,mask,lat,lat_range=None):
    """计算变化mask（每个月的mask不一样）的时间序列,纬度加权

    Args:
        grd (array): 格网数组
        mask (array): 掩膜格网数组,与grd大小相同（每个月的mask不一样）
        lat (array): 纬度数组
        lat_range (tuple): 纬度范围
    """
    if lat_range is None:
        weighted_average = weight_mean.latitudinal_weight_mask(grd, lat, mask)
    else:
        loc = (lat>=lat_range[0])&(lat<=lat_range[1])
        weighted_average = weight_mean.latitudinal_weight_mask(grd[loc,:,:], lat[loc], mask[loc,:,:])

    return weighted_average

def series_latitudinal_box(grd,mask,lat,lat_range,lon,lon_range):
    """计算box的时间序列，box由lat_range和log_range给出,为矩形

    Args:
        grd (_type_): _description_
        mask (_type_): _description_
        lat (_type_): _description_
        lat_range (_type_, optional): _description_. Defaults to None.
        lon_range (_type_, optional): _description_. Defaults to None.
    """
    if isinstance(lat_range,tuple):
        latloc = (lat>=lat_range[0])&(lat<=lat_range[1])
    else:
        latloc = (lat == lat_range)
        if np.all(latloc == False):
            raise ValueError('lat_range is wrong')
    if isinstance(lon_range,tuple):
        lonloc = lr.longitude_range(lon,lon_range)
    else:
        lonloc = (lon == lon_range)
        if np.all(lonloc == False):
            raise ValueError('lon_range is wrong')
    if np.ndim(mask) == 2:
        weighted_average = weight_mean.latitudinal_weight(grd[latloc,:,:][:,lonloc,:], lat[latloc], mask[latloc,:][:,lonloc])
    if np.ndim(mask) == 3:
        weighted_average = weight_mean.latitudinal_weight_mask(grd[latloc,:,:][:,lonloc,:], lat[latloc], mask[latloc,:,:][:,lonloc,:])

    return weighted_average

def time_series_rolling_mean(y,window_size=30):
    """移动平均

    Args:
        y (array): y值
        window_size (int, optional): 滑动窗口大小. Defaults to 30.

    Returns:
        array: 去除趋势后的时间序列
    """
    y_detrended = y - pd.Series(y).rolling(window_size,center=True).mean().values

    return y_detrended

def time_series_low_pass_fft(y):
    """
    频率域的低通滤波

    Parameters:
    y (array-like): Input signal.

    Returns:
    array-like: Detrended signal.
    """
    y_fft = fft(y)
    freqs = fftfreq(len(y))
    mask = freqs > 0
    y_fft_detrended = y_fft.copy()
    y_fft_detrended[mask] = 0
    y_detrended = np.real(ifft(y_fft_detrended))

    return y_detrended

def time_series_remove_trend(t,y):
    """时间序列去除趋势

    Args:
        t (array): 时间数组
        y (array): y值

    Returns:
        array: 去除趋势后的时间序列
    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass

    popt,_= curve_fit(ff.line_trend,t,y,p0=[1,1])
    y_fit = y - ff.line_trend(t,*popt)

    return y_fit

def time_series_trend(t,y):
    """时间序列趋势

    Args:
        t (array): 时间数组
        y (array): y值
    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass

    popt,_= curve_fit(ff.line_trend,t,y,p0=[1,1])

    return ff.line_trend(t,*popt)

def time_series_remove_seasonal_cycle(t,y):
    """移除周期性的时间序列

    Args:
        t (array): 时间数组
        y (array): y值

    Returns:
        array: 移除周期性后的时间序列
    """

    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass

    popt,_= curve_fit(ff.annual_seasonal_trend,t,y,p0=[1,1,1,1,1,1])
    y_fit = y - (ff.annual_seasonal_trend(t,*popt)-ff.line_trend(t,*popt))

    return y_fit

def time_series_seasonal_cycle(t,y):
    """时间序列的周期性

    Args:
        t (array): 时间数组
        y (array): y值
    """

    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass

    popt,_= curve_fit(ff.annual_seasonal_trend,t,y,p0=[1,1,1,1,1,1])

    return ff.seasonal_cycle(t,*popt[2:])

def time_series_remove_trend_and_seasonal_cycle(t,y):
    """移除趋势和周期性的时间序列

    Args:
        t (_type_): _description_
        y (_type_): _description_
    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass

    popt,_= curve_fit(ff.annual_seasonal_trend,t,y,p0=[1,1,1,1,1,1])
    y_fit = y - ff.annual_seasonal_trend(t,*popt)

    return y_fit

def time_series_remove_acceleration(t,y):
    """移除加速度项(二次项)后的时间序列

    Args:
        t (array): 时间数组
        y (array): y值

    Returns:
        array: 移除加速度项后的时间序列
    """
    if isinstance(t,pd.DatetimeIndex):
        t = tt.dateseries_to_timeseries(t)
    else:
        pass

    popt,_= curve_fit(ff.acceleration,t,y,p0=[1,1,1])
    y_fit = y - (ff.acceleration(t,*popt)-ff.line_trend(t,*popt))

    return y_fit

def pd_Series_operation_set(series:pd.Series, type:'str'):
    """针对pd.Series的操作集合

    Args:
        series (_type_): _description_
        type (str): "remove_trend" or "remove_seasonal_cycle" or "remove_trend_and_seasonal_cycle" or "remove_acceleration"

    Returns:
        series (_type_): _description_
    """

    t = tt.dateseries_to_timeseries(series.index)
    y = series.values
    if np.any(np.isnan(y)):
        raise ValueError('y has nan')
    else:
        if type == 'remove_trend':
            y_fit = time_series_remove_trend(t,y)
        elif type == 'remove_seasonal_cycle':
            y_fit = time_series_remove_seasonal_cycle(t,y)
        elif type == 'remove_trend_and_seasonal_cycle':
            y_fit = time_series_remove_trend_and_seasonal_cycle(t,y)
        elif type == 'remove_acceleration':
            y_fit = time_series_remove_acceleration(t,y)

    return pd.Series(y_fit,index=series.index)