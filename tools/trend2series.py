import numpy as np
import pandas as pd
from tools import time_transfer as tt
def spatial_trend2series(date,trend,constant=None):
    """
    Args:
        lat (_type_): _description_
        lon (_type_): _description_
        date (_type_): _description_
        trend (_type_): _description_
        constant (int, optional): _description_. Defaults to 0.
    """
    if isinstance(date, pd.DatetimeIndex):
        time = tt.dateseries_to_timeseries(date)
    else:
        date = pd.DatetimeIndex(date)
        time = tt.dateseries_to_timeseries(date)
    if constant is None:
        constant = time[0]*trend
    else:
        pass
    spatial_series = trend[:,:,None] * time[None,None,:] - constant[:,:,None]
    return spatial_series
