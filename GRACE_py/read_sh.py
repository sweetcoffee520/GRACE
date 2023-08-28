import os

import numpy as np
import pandas as pd
from tools import time_transfer as tt

def sumN(N: int):
    result = 0
    for i in range(N+1):
        result += i
    return result


def read_sh(fold_path, file_flag, rankflag, institute_flag):
    """提取球谐系数文件

    Args:
    ----------
        fold_path (str or list):
            文件夹路径,或文件夹路径列表,当类型为列表是,GRACE路径放在前,GRACE-FO路径放在后
        file_flag (str):
            文件类型(GSM,GAA,GAC,GAD等)
        rankflag ([type]):
            文件阶数标志(A->60,B->90,C->180)
        institute_flag (str):
            文件来源(CSR,JPL,GFZ)
    Returns:
        Lmax, GC, GS, SC, date, file_num
    """

    flag_name_list = []
    file_name_list = []
    file_list = []
    date = []
    if type(fold_path) is list:
        # 循环文件夹，获取所有文件路径
        for fold_name in fold_path:
            flag_name_list.clear()
            file_list = os.listdir(fold_name)
            file_list.sort()
            for name in file_list:
                if name.startswith(file_flag) and name[-8] == rankflag:
                    flag_name_list.append(name)
            for name in flag_name_list:
                name_split = name.split('_')[1].split('-')
                startdate = name_split[0]
                enddate = name_split[1]
                startyear = int(startdate[0:4])
                endyear = int(enddate[0:4])
                # 跨越年份的情况
                if endyear - startyear == 1:
                    startday = int(startdate[4:7])
                    endday = int(enddate[4:7])
                    start_year_days = tt.year_days(startyear)
                    if start_year_days-startday > endday:
                        year = startyear
                        endday = start_year_days+endday
                    else:
                        year = endyear
                        startday = startday - start_year_days
                else:
                    startday = int(startdate[4:7])
                    endday = int(enddate[4:7])
                    year = startyear
                midday = (startday+endday-1)/2 #此处减1是因为GRACE的起始时间是从1月1日开始的，即2002001表示2002年1月1日
                date.append(tt.day2date(year, midday))
                file_name_list.append(os.path.join(fold_name,name))
    else:
        file_list = os.listdir(fold_path)
        file_list.sort()
        for name in file_list:
            if name.startswith(file_flag) and name[-8] == rankflag:
                flag_name_list.append(name)
        for name in flag_name_list:
            name_split = name.split('_')[1].split('-')
            startdate = name_split[0]
            enddate = name_split[1]
            startyear = int(startdate[0:4])
            endyear = int(enddate[0:4])
            if endyear - startyear == 1:
                startday = int(startdate[4:7])
                endday = int(enddate[4:7])
                start_year_days = tt.year_days(startyear)
                if start_year_days-startday > endday:
                    year = startyear
                    endday = start_year_days+endday
                else:
                    year = endyear
                    startday = startday - start_year_days
            else:
                startday = int(startdate[4:7])
                endday = int(enddate[4:7])
                year = startyear
            midday = (startday+endday-1)/2 #此处减1是因为GRACE的起始时间是从1月1日开始的，即2002001表示2002年1月1日
            date.append(tt.day2date(year, midday))
            file_name_list.append(os.path.join(fold_path,name))
    # 判断阶数
    if rankflag=='A':
        Lmax = 60
    elif rankflag=='B':
        Lmax = 96
    elif rankflag=='C':
        Lmax = 180
    file_num = len(file_name_list)
    linenum = sumN(Lmax+1)
    # 阶数
    l = np.zeros((linenum, file_num))
    # 次数
    m = np.zeros((linenum, file_num))
    GC = np.zeros((linenum, file_num))
    GS = np.zeros((linenum, file_num))
    SC = np.zeros((Lmax+1, 2*Lmax+1, file_num))
    date = pd.DatetimeIndex(date)

    if institute_flag == 'CSR' or institute_flag == 'GFZ':
        for file_name in file_name_list:
            with open(file_name, 'r') as p:
                allcontent = p.read()
            sp = allcontent.split('End of YAML header', 1)
            # headcontent.append(yaml.load(sp[0], Loader=yaml.BaseLoader))
            filedata = sp[1].strip().split()
            data_array = np.array(filedata).reshape(-1, 10)
            l[:, file_name_list.index(file_name)] = data_array[:, 1]
            m[:, file_name_list.index(file_name)] = data_array[:, 2]
            GC[:, file_name_list.index(file_name)] = data_array[:, 3]
            GS[:, file_name_list.index(file_name)] = data_array[:, 4]
    elif institute_flag == 'JPL':
        for file_name in file_name_list:
            with open(file_name, 'r') as p:
                allcontent = p.read()
            sp = allcontent.split('End of YAML header', 1)
            # headcontent.append(yaml.load(sp[0], Loader=yaml.BaseLoader))
            filedata = sp[1].strip().split()
            data_array = np.array(filedata).reshape(-1, 10)
            if file_flag == 'GSM':
                l[3:, file_name_list.index(file_name)] = data_array[:, 1]
                m[3:, file_name_list.index(file_name)] = data_array[:, 2]
                GC[3:, file_name_list.index(file_name)] = data_array[:, 3]
                GS[3:, file_name_list.index(file_name)] = data_array[:, 4]
            else:
                l[:, file_name_list.index(file_name)] = data_array[:, 1]
                m[:, file_name_list.index(file_name)] = data_array[:, 2]
                GC[:, file_name_list.index(file_name)] = data_array[:, 3]
                GS[:, file_name_list.index(file_name)] = data_array[:, 4]

    l = l.astype(np.int32)
    m = m.astype(np.int32)
    for i in range(file_num):
        for j in range(len(l[:, 1])):
            # DeltaC[l[j,i],m[j,i],i] = Dgc[j,i]
            # DeltaS[l[j,i],m[j,i],i] = Dgs[j,i]
            SC[l[j, i], Lmax-m[j, i], i] = GS[j, i]
            SC[l[j, i], Lmax+m[j, i], i] = GC[j, i]

    return Lmax, GC, GS, SC, date, file_num

def read_GIA_sh(file_path,flag):
    """读取GIA的球谐系数

    Args:
        fold_path (str): GIA球谐系数文件路径
        flag (str): GIA类型,Altimetry or GRACE
    """
    Lmax = 256
    linenum = sumN(Lmax+1)
    l = np.zeros(linenum)
    # 次数
    m = np.zeros(linenum)
    GC = np.zeros(linenum)
    GS = np.zeros(linenum)
    SC = np.zeros((Lmax+1, 2*Lmax+1))
    with open(file_path, 'r') as p:
        allcontent = p.read()
    filedata = allcontent.strip().split('\n')
    if flag == 'GRACE':
        degree2_data = np.array('\n'.join(filedata[1:7]).split()).reshape(-1,4)
        l[:6] = degree2_data[:,0]
        m[:6] = degree2_data[:,1]
        GC[:6] = degree2_data[:,2]
        GS[:6] = degree2_data[:,3]
    elif flag == 'Altimetry':
        degree2_data = np.array('\n'.join(filedata[9:15]).split()).reshape(-1,4)
        l[:6] = degree2_data[:,0]
        m[:6] = degree2_data[:,1]
        GC[:6] = degree2_data[:,2]
        GS[:6] = degree2_data[:,3]
    data = np.array('\n'.join(filedata[17:]).split()).reshape(-1,4)
    l[6:] = data[:,0]
    m[6:] = data[:,1]
    GC[6:] = data[:, 2]
    GS[6:] = data[:, 3]
    l = l.astype(np.int32)
    m = m.astype(np.int32)
    for j in range(linenum):
        # DeltaC[l[j,i],m[j,i],i] = Dgc[j,i]
        # DeltaS[l[j,i],m[j,i],i] = Dgs[j,i]
        SC[l[j], Lmax-m[j]] = GS[j]
        SC[l[j], Lmax+m[j]] = GC[j]

    return SC

def read_sh_swarm(fold_path):
    file_list = []
    file_name_list = []
    # 循环文件夹，获取所有文件路径
    file_list = os.listdir(fold_path)
    file_list.sort()
    for name in file_list:
        file_name_list.append(os.path.join(fold_path,name))
    Lmax = 40
    file_num = len(file_name_list)
    linenum = sumN(Lmax+1)
    # 阶数
    l = np.zeros((linenum, file_num))
    # 次数
    m = np.zeros((linenum, file_num))
    GC = np.zeros((linenum, file_num))
    GS = np.zeros((linenum, file_num))
    SC = np.zeros((Lmax+1, 2*Lmax+1, file_num))
    for file_name in file_name_list:
        with open(file_name, 'r') as p:
            allcontent = p.read()
        sp = allcontent.split('end_of_head ========================================', 1)
        # headcontent.append(yaml.load(sp[0], Loader=yaml.BaseLoader))
        filedata = sp[1].strip().split()
        data_array = np.array(filedata).reshape(-1, 5)
        l[:, file_name_list.index(file_name)] = data_array[:, 1].astype(np.int32)
        m[:, file_name_list.index(file_name)] = data_array[:, 2].astype(np.int32)
        GC[:, file_name_list.index(file_name)] = data_array[:, 3].astype(np.float32)
        GS[:, file_name_list.index(file_name)] = data_array[:, 4].astype(np.float32)
    l = l.astype(np.int32)
    m = m.astype(np.int32)
    for i in range(file_num):
        for j in range(len(l[:, 1])):
            # DeltaC[l[j,i],m[j,i],i] = Dgc[j,i]
            # DeltaS[l[j,i],m[j,i],i] = Dgs[j,i]
            SC[l[j, i], Lmax-m[j, i], i] = GS[j, i]
            SC[l[j, i], Lmax+m[j, i], i] = GC[j, i]
    return Lmax, GC, GS, SC, file_num