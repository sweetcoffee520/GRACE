import datetime
import numpy as np
import pandas as pd


def isLeap(year):
    '''
    判断是否为闰年
    '''
    flag = ((year % 4) == 0) and (
        not ((year % 100) == 0 and (year % 400) != 0))
    return(flag)


def delta2date(delta, startdate: np.datetime64) -> pd.DatetimeIndex:
    """把时间间隔序列转化为日期

    Args:
        delta (array): 时间间隔数组
        startdate (np.datetime64): 开始的日期

    Returns:
        list: 日期序列
    """
    time_schedule = []
    time_begin = np.datetime64(startdate,'D')
    for i in range(len(delta)):
        time_space_day =  np.timedelta64(int(delta[i]), 'D')
        time_space_hour = np.timedelta64(int((delta[i]-int(delta[i]))*24),'h')
        time_schedule.append(time_begin + time_space_day + time_space_hour)

    return pd.to_datetime(time_schedule)

def delta2date_unit(delta, unit: str, startdate: np.datetime64, delta_day) -> list:
    """把时间间隔序列转化为日期，指定时间单位和某月开始的天数

    Args:
        delta (array): 时间间隔数组
        unit (str): 时间单位('Y','M','W','D','h','m','s','ms')
        startdate (np.datetime64): 开始日期
        delta_day (int): 距一号的天数

    Returns:
        DatetimeIndex: 日期序列
    """
    time_begin = np.datetime64(startdate,unit)
    time_schedule = []

    for i in range(len(delta)):
        time_space = np.timedelta64(int(delta[i]), unit)
        # time_space = delta.astype(unit)
        time_schedule.append(time_begin + time_space +
                             np.timedelta64(delta_day, 'D'))
    time_schedule = pd.to_datetime(time_schedule)
    # time_list = time_schedule.tolist()

    return time_schedule


def day2date(year, day):
    '''
    把指定的天数转换为year年的年月日，起始时间为每年的1月1日00:00:00
    '''
    # first_day = datetime.date(year, 1, 1)
    # add_day = datetime.timedelta(days = int(day-1))
    # add_hour = datetime.timedelta(hours = int((day-int(day))*24))
    first_day = np.datetime64(str(year),'Y')
    add_day = np.timedelta64(int(day),'D')
    add_hour = np.timedelta64(int((day-int(day))*24),'h')
    # return datetime.datetime.strftime(first_day+add_day+add_hour,'%Y-%m-%d-%H-%M-%S')
    return pd.to_datetime(first_day+add_day+add_hour)


def date2day(date: datetime):
    '''
    将日期转换成在当年的天数
    '''
    year = date.year
    month = date.month
    day = date.day
    d = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]

    if 0 < month <= 12:
        sum_day = d[month-1]
    else:
        print('month error')

    sum_day += day

    # 判断闰年
    leap = isLeap(year)

    if(leap == 1 and month > 2):
        # 如果是闰年且月份大于2，则总天数加1
        sum_day += 1

    return sum_day


def str2date(timestr):
    """字符串转时间

    Args:
        timestr (str): 时间类型字符在，形式为"2000-01-01 01:01:01"

    Returns:
        datetime
    """

    date_time = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
    return date_time

def year_days(year):
    '''
    计算本年一共有多少天
    '''
    begin = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)

    return (end-begin).days+1


def date2fraction_year(date: datetime):
    '''
    把日期转换成当天所占当年的比例
    '''
    days = date2day(date)
    time_proportion = days/year_days(date.year)

    return time_proportion


def fracion_of_year2date(fraction_year):
    '''
    把比例时间转换为日期
    '''
    fraction_days = fraction_year - int(fraction_year)
    date = day2date(int(fraction_year), fraction_days*year_days(int(fraction_year)))
    return date


def dateseries_to_timeseries(dateseries: pd.DatetimeIndex) -> list:
    '''
    把日期序列转换为时间序列
    '''
    timeseries = []
    for date in dateseries:
        timeseries.append(date.year + date2fraction_year(date))
    return np.array(timeseries)

def timeseries_to_dateseries(timeseries: list) -> pd.DatetimeIndex:
    '''
    把时间序列转换为日期序列
    '''
    dateseries = []
    for time in timeseries:
        dateseries.append(fracion_of_year2date(time))
    return pd.to_datetime(dateseries)

def strtime_to_dateseries(strtimelist:list) -> pd.DatetimeIndex:
    '''
    字符串时间序列转为日期序列
    '''
    dateseries = []
    for strtime in strtimelist:
        year = int(strtime[0:4])
        day = int(strtime[4:7])
        dateseries.append(day2date(year, day))
    return pd.to_datetime(dateseries)

def date2middle_month(date:np.datetime64):
    '''
    把日期转换成当月的中间日期
    '''
    dateseries = []
    for time in date:
        time = pd.Timestamp(datetime.datetime(time.year,time.month,1))+pd.Timedelta(time.daysinmonth-1,unit='D')
        day = int(time.daysinmonth/2)
        dateseries.append(time-np.timedelta64(day, 'D'))
    return pd.to_datetime(dateseries)