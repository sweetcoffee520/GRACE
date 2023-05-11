'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2022-11-01 00:27:59
FilePath: /ocean_change_python/GRACE_py/forward_model.py
Description: forward_model for solve leakage error

Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import numpy as np
from . import grid2cs
from . import mass
from . import filter
from . import sc_action_set


def forward_model(equivalent_water_height, lat, lon, res_lonlat, Lmax, filter_radius, rho_water, love_path ,alpha):
    """caculate forward_model for solve leakage error

    Args:
        equivalent_water_height (array): iteration initial value
        lat (array): latitude
        lon (array): longitude
        res_lonlat (float): resolution of lon and lat
        Lmax(int): max order
        filter_radius (float): filter radius
        rho_water (float): water density
        love_path (array): love number path
        alpha (float): acceleration factor
    """

    time_length = np.shape(equivalent_water_height)[2]
    prediction_model = np.empty(np.shape(equivalent_water_height))
    result_model = np.empty(np.shape(equivalent_water_height))
    error_model = np.empty(np.shape(equivalent_water_height))
    iteration = 50
    error = np.empty((iteration,time_length))
    lat_mask = np.cos(np.deg2rad(lat))

    for i in range(time_length):
        initial_model = equivalent_water_height[:,:,i].copy()
        origin_model = equivalent_water_height[:,:,i].copy()
        for j in range(iteration):
            C, S = grid2cs.grid2cs(initial_model[:,:,None], lat, lon, res_lonlat, love_path, Lmax, rho_water)
            # C[0, ...] = 0
            # S[0, ...] = 0
            # C[1, ...] = 0
            # S[1, ...] = 0
            SC = sc_action_set.singlesc2sc(C, S, Lmax)
            SC_filter = filter.gaussian_filter(SC, filter_radius, Lmax)
            C0, S0 = sc_action_set.sc2singlesc(SC_filter, Lmax)
            prediction_model[:,:,i] = np.squeeze(mass.mass(Lmax, 1, C0, S0, lat, lon, love_path, 1000))
            error[j,i] = np.sqrt(np.sum((prediction_model[:,:,i] - origin_model)**2*lat_mask[:,None])/np.sum(np.tile(lat_mask[:,None],(1,len(lon)))))
            error_model = prediction_model[:,:,i] - origin_model
            initial_model -= alpha * error_model
        result_model[:,:,i] = initial_model
    return result_model, prediction_model ,error