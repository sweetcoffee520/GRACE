'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-07-11 19:54:03
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2024-04-12 09:42:49
FilePath: /ocean_change_python/GRACE_py/GRACE_data_date.py
Github: https://github.com/sweetcoffee520
Description: GRACE数据缺失数据的年份，有效的年份
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import pandas as pd
from tools import time_transfer as tt
import datetime

miss_date = pd.DatetimeIndex(('2002-06','2002-07','2003-06','2011-01','2011-06','2012-05','2012-10','2013-03','2013-08','2013-09','2014-02','2014-07','2014-12','2015-06',
                 '2015-10','2015-11','2016-04','2016-09','2016-10','2017-02','2017-07','2017-08','2017-09','2017-10','2017-11','2017-12','2018-01','2018-02','2018-03',
                 '2018-04','2018-05','2018-08','2018-09',))
gap_date = tt.dateseries_to_middle_of_month(pd.date_range('2017-07','2018-06',freq='ME'))
full_date = tt.date2middle_month(pd.date_range('2002-04',datetime.date.today(),freq='ME'))
valid_date = full_date[~full_date.isin(miss_date)]