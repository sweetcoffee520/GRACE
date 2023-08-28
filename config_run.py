import yaml
import xarray as xr
import pandas as pd
import numpy as np
from GRACE_py import read_sh as rsh
from GRACE_py import mass
from GRACE_py import sc_action_set as sac
from GRACE_py import region_grid as rgd
from GRACE_py import filter as flt
from GRACE_py import destriping as dsp
from GRACE_py import replace_action_set
from tools import spatial_distribution as sd
from tools import time_series as ts
from tools import time_transfer as tt
from tools import matplot
from tools import fit_result_error as fre
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
fold_path = config['PATH'][0]['GRACE_SH_FOLDER']
Institute = config['PATH'][1]['Institute']
love_path = config['PATH'][2]['love_path']
mask_path = config['PATH'][3]['mask_path']

C00_replace = config['Replace'][0]['C00']
degree1_replace = config['Replace'][1]['degree1']
C20C30_replace = config['Replace'][2]['C20C30']

destripe_filter = config['Filter'][0]['destripe']
gaussian_filter_radius = config['Filter'][1]['gaussian_filter_radius']

resolution = config['Resolution']

# 创建网格
lat, lon, _, _, _, _ = rgd.region_grid(-89.5, 89.5, 0.5, 359.5, resolution)
# 读取GRACE SH数据，返回Lmax, GC, GS, SC, date, file_num
Lmax, GC, GS, SC, date, file_num =  rsh.read_sh(fold_path,file_flag='GSM',rankflag='A',institute_flag=Institute)
# 替换一阶项
if degree1_replace is True:
    SC = replace_action_set.replace_degree1(SC, Lmax, f'data/TN-13_GEOC_CSR_RL06.txt')
# 替换C20 C30
if C20C30_replace is True:
    SC = replace_action_set.replace_c20_c30(SC, Lmax, 'data/TN-14_C30_C20_GSFC_SLR.txt')
# 去条带
if destripe_filter == 'chen':
    SC_new = dsp.chen_destriping(SC,20,50,5,Lmax)
elif destripe_filter == 'sweason':
    SC_new = dsp.swenson_destriping(SC,5,60,5,52,2,Lmax)
elif destripe_filter == 'chamber':
    SC_new = dsp.chambers_destriping(SC,12,40,5,Lmax)
# 高斯滤波
SC_new = flt.gaussian_filter(SC_new,gaussian_filter_radius,Lmax)
# 减去与mascon数据相同时间段的平均值
DeltaSC = sac.sc2Deltasc_mascon(SC_new)
# 计算DeltaC,DeltaS
DeltaC,DeltaS = sac.sc2singlesc(DeltaSC,Lmax)
# 计算质量变化
area_mass = mass.mass(Lmax,file_num,DeltaC,DeltaS,lat,lon,love_path,1000)
area_mask = xr.open_dataset(mask_path).z.values
area_ts = ts.series_latitudinal(area_mass,area_mask,lat)
area_para,area_para_error = fre.annual_season_fit(date,area_ts)
sp_trend,sp_amp,sp_semiamp,sp_pha,sp_semipha = sd.spatial_trend_amp(date,area_mass)
latm = np.repeat(lat, len(lon))[:,None]
lonm = np.tile(lon, len(lat))[:,None]
# 组建lon,lat,value格式的array数组
lonlat = np.c_[lonm,latm]
value = np.reshape(sp_trend*10,(-1,1),'C')
xyz = np.reshape(np.hstack((lonlat, value)),(-1,3))
np.savetxt('result/spatial_trend.txt',xyz,fmt='%7f %7f %.3f')
area_dataframe = pd.DataFrame({'area_para':area_para,'area_para_error':area_para_error},index=['trend','annual_amp','semiannual_amp','annual_pha','semiannual_pha'])
area_dataframe.to_csv('area_para.csv')
fig,ax = matplot.plot_line((date,area_ts,'',''),xtitle='Time',ytitle='EWH(cm)')
fig.savefig('area_ts.png',dpi=300,bbox_inches='tight',facecolor='white',pad_inches=0.1)