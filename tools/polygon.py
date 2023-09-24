'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-08-29 15:36:34
FilePath: /ocean_change_python/tools/polygon.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
import shapely.geometry
from matplotlib.path import Path
import re
from tools import array_operation_set as aos

# Points located inside or on edge of polygonal region
def inpolygon(xq, yq, xv, yv):
    shape = xq.shape
    xq = xq.reshape(-1)
    yq = yq.reshape(-1)
    xv = xv.reshape(-1)
    yv = yv.reshape(-1)
    q = [(xq[i], yq[i]) for i in range(xq.shape[0])]
    p = Path([(xv[i], yv[i]) for i in range(xv.shape[0])])
    return p.contains_points(q).reshape(shape)

def boundary2mask(boundarys, resolution, * ,is_file = True, data_type='lonlat', cross_meridian=False):
    """ 将边界转换为mask
    Args:
        boundary_file (str): 边界文件(区域边界的经纬度)
        resolution (int): 分辨率大小
        is_file (bool, optional): 是否为文件. Defaults to True.
        data_type (str, optional): 列顺序'latlon' or 'lonlat, Defaults is 'lonlat'
        cross_meridian (bool, optional): 是否穿过本初子午线. Defaults to False.

    Returns:
        _type_: _description_
    """

    if is_file == True:
        with open(boundarys,'r') as f:
            # _表示这个变量不需要
            boundary = np.reshape(np.array(f.read().split()),(-1,2))
    else:
        boundary = boundarys
    if data_type == 'lonlat':
        x = boundary[:,0].astype(np.float32)
        y = boundary[:,1].astype(np.float32)
    elif data_type == 'latlon':
        x = boundary[:,1].astype(np.float32)
        y = boundary[:,0].astype(np.float32)

    if resolution == 1:
        lat = np.arange(-89.5,89.6,resolution)
        lon = np.arange(0.5,359.6,resolution)
    elif resolution == 0.5:
        lat = np.arange(-89.75,89.76,resolution)
        lon = np.arange(0.25,359.76,resolution)
    elif resolution == 0.25:
        lat = np.arange(-89.875,89.876,resolution)
        lon = np.arange(0.125,359.876,resolution)

    lg_mask = np.zeros((len(lat),len(lon)))

    if cross_meridian == False:
        x[x<0] += 360
        lonmin = np.min(x)
        lonmax = np.max(x)
        latmin = np.min(y)
        latmax = np.max(y)
        for i in range(len(lat)):
            for j in range(len(lon)):
                if lat[i]>=latmin and lat[i]<=latmax and lon[j]>=lonmin and lon[j]<=lonmax:
                    in_ = inpolygon(lon[j],lat[i],x,y)
                    if in_ == True:
                        lg_mask[i,j] = 1
    elif cross_meridian == True:
        x[x>180]-=360
        lonm = lon-180
        lonmin = np.min(x)
        lonmax = np.max(x)
        latmin = np.min(y)
        latmax = np.max(y)
        for i in range(len(lat)):
            for j in range(len(lonm)):
                if lat[i]>=latmin and lat[i]<=latmax and lonm[j]>=lonmin and lonm[j]<=lonmax:
                    in_ = inpolygon(lonm[j],lat[i],x,y)
                    if in_ == True:
                        lg_mask[i,j] = 1
        lg_mask = aos.swaplr(lg_mask)

    return lat,lon,lg_mask

def boundary2mask_gmtdcw(file_path,resolution,Antarctica=False):
    """将gmt的dcw提取的边界文件转换为mask

    Args:
        file_path (str): 文件路径
        Antarctica (bool, optional): 是否为南极洲(dcw的南极洲边界线比较特殊，需要单独处理). Defaults to False.

    Returns:
        _type_: _description_
    """

    if resolution == 1:
        lat = np.arange(-89.5,89.6,resolution)
        lon = np.arange(0.5,359.6,resolution)
    elif resolution == 0.5:
        lat = np.arange(-89.75,89.76,resolution)
        lon = np.arange(0.25,359.76,resolution)
    elif resolution == 0.25:
        lat = np.arange(-89.875,89.876,resolution)
        lon = np.arange(0.125,359.876,resolution)

    mask = np.zeros((len(lat),len(lon)))
    with open(file_path,'r') as f:
        content = f.read()
        boundarys = list(filter(None,re.split(r">\s+\w+\s+\w+ \d+\n",content)))
    if Antarctica == True:
        boundary_part = np.array(boundarys[0].split(),dtype='float').reshape(-1,2)
        boundary_part[-2,0] = 0
        boundary_part[-2,1] = -90
        boundary_part[-1,0] = 360
        boundary_part[-1,1] = -90
        _,_,mask = boundary2mask(boundary_part,resolution,is_file=False)
    else:
        for boundary in boundarys:
            boundary_part = np.array(boundary.split(),dtype='float').reshape(-1,2)
            _,_,mask_part = boundary2mask(boundary_part,resolution,is_file=False)
            mask += mask_part
    mask[mask>1] = 1
    return lat,lon,mask

# Create buffer around points, lines, or polyshape objects
def polybuffer(P,d):
    if isinstance(P,shapely.geometry.Point):
        return P.buffer(d)
    elif isinstance(P,shapely.geometry.LineString):
        return P.buffer(d)
    elif isinstance(P,shapely.geometry.Polygon):
        return P.buffer(d)
    elif isinstance(P,np.ndarray):
        return shapely.geometry.MultiPolygon([polybuffer(shapely.geometry.Point(p),d) for p in P])
    elif isinstance(P,shapely.geometry.MultiPolygon):
        return shapely.geometry.MultiPolygon([polybuffer(shapely.geometry.Point(p),d) for p in P])
    else:
        raise TypeError('{} is not a valid type'.format(type(P)))

def equidistant_zoom_contour(contour, margin):
    """
    等距放大轮廓
    contour: 输入轮廓
    margin: 放大距离
    :return: 输出轮廓
    """
    # 轮廓长度
    length = contour.shape[0]
    # 轮廓中心坐标
    center = np.array([np.mean(contour[:, 0]), np.mean(contour[:, 1])])
    # 轮廓放大后的轮廓
    new_contour = np.zeros((length, 2))
    # 等距放大轮廓
    for i in range(length):
        if contour[i,0]>center[0]:
            new_contour[i,0] = contour[i,0] + margin
        elif contour[i,0]<center[0]:
            new_contour[i,0] = contour[i,0] - margin
        if contour[i,1]>center[1]:
            new_contour[i,1] = contour[i,1] + margin
        elif contour[i,1]<center[1]:
            new_contour[i,1] = contour[i,1] - margin
    return new_contour