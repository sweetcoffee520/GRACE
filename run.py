'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2023-08-07 19:49:35
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-08-25 10:07:03
FilePath: /GRACE_code/run.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import argparse
import pathlib
import xarray as xr
import pandas as pd
import numpy as np
from GRACE_py import read_sh as rsh
from GRACE_py import mass
from GRACE_py import sc_action_set as sac
from GRACE_py import replace_action_set
from GRACE_py import region_grid as rgd
from GRACE_py import destriping
from GRACE_py import filter
from tools import spatial_distribution as sd
from tools import time_series as ts
from tools import time_transfer as tt
from tools import matplot
from tools import fit_result_error as fre
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path', type=pathlib.Path, required=True, help='SH file path',metavar='')
    parser.add_argument('-i','--institute', type=str, required=['-p'],default='CSR', help='institute',metavar='')
    parser.add_argument('-r','--resolution', type=float, default=1, help='resolution of grid(0.25|0.5|1)',metavar='')
    parser.add_argument('-lp','--love_path', type=pathlib.Path, default='data/loadLove.txt', help='love file path',metavar='')
    parser.add_argument('-mp','--mask_path', type=pathlib.Path, default='data/mask01d_300km.nc', help='mask file path',metavar='')
    parser.add_argument('-dp','--destrip', type=str, default='chen', help='destrip method',metavar='')
    parser.add_argument('-fr','--filter-radius', type=int, default=300, help='radius of filter(km)',metavar='')
    parser.add_argument('-d1','--degree1', default=True, help='replace degree1',action='store_true')
    parser.add_argument('-d23','--degree23', default=True, help='replace C20 C30',action='store_true')

    return parser

def main():
    parser = arguments()
    args,_ = parser.parse_known_args()
    lat, lon, _, _, _, _ = rgd.region_grid(-89.5, 89.5, 0.5, 359.5, args.resolution)
    Lmax, _, _, SC, date, file_num =  rsh.read_sh(args.path,file_flag='GSM',rankflag='A',institute_flag=args.institute)
    if args.degree1 is True:
        SC = replace_action_set.replace_degree1(SC, Lmax, f'data/TN-13_GEOC_{args.institute}_RL06.txt')
    if args.degree23 is True:
        SC = replace_action_set.replace_c20_c30(SC, Lmax, 'data/TN-14_C30_C20_GSFC_SLR.txt')
    if args.destrip == 'chen':
        SC_new = destriping.chen_destriping(SC, 20, 55, 5, Lmax)
    SC_new = filter.gaussian_filter(SC_new, args.filter_radius, Lmax)
    DeltaSC = sac.sc2Deltasc_mascon(SC_new)
    DeltaC,DeltaS = sac.sc2singlesc(DeltaSC,Lmax)
    area_mass = mass.mass(Lmax,file_num,DeltaC,DeltaS,lat,lon,args.love_path,1000)
    sp_trend,sp_amp,sp_semiamp,sp_pha,sp_semipha = sd.spatial_trend_amp(date,area_mass)
    latm = np.repeat(lat, len(lon))[:,None]
    lonm = np.tile(lon, len(lat))[:,None]
    # 组建lon,lat,value格式的array数组
    lonlat = np.c_[lonm,latm]
    value = np.reshape(sp_trend*10,(-1,1),'C')
    xyz = np.reshape(np.hstack((lonlat, value)),(-1,3))
    np.savetxt('result/spatial_trend.txt',xyz,fmt='%7f %7f %.3f')
    area_mask = xr.open_dataset(args.mask_path).z.values
    area_ts = ts.series_latitudinal(area_mass,area_mask,lat)
    area_para,area_para_error = fre.annual_season_fit(date,area_ts)
    area_dataframe = pd.DataFrame({'area_para':area_para,'area_para_error':area_para_error},index=['trend','annual_amp','semiannual_amp','annual_pha','semiannual_pha'])
    area_dataframe.to_csv('result/area_para.csv')
    fig,ax = matplot.plot_line((date,area_ts,'',''),xtitle='Time',ytitle='EWH(cm)')
    fig.savefig('result/area_ts.png',dpi=300,bbox_inches='tight',facecolor='white',pad_inches=0.1)

if __name__ == '__main__':
    main()