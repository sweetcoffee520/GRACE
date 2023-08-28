'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2023-08-24 17:16:21
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-08-25 10:14:00
FilePath: /GRACE_code/plot_map.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import numpy as np
from tools import plot_gmt as pg
xyz = np.loadtxt('result/spatial_trend.txt')
trend_fig = pg.plot_X(xyz[:,:,None], '1/1', 'd0.5/359.5/-89.5/89.5', '-10/10/5','jet', True, title='' ,xtitle='', ytitle='',unit='mm/yr', rows = 1,cols = 1)
trend_fig.savefig('result/spatial_trend.png')