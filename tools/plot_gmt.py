'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-08-23 16:14:35
FilePath: /ocean_change_python/tools/plot_gmt.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import pygmt

pygmt.config(MAP_FRAME_WIDTH='2p', MAP_FRAME_TYPE='fancy', MAP_TITLE_OFFSET = '2p', COLOR_NAN = 'gray', 
            FORMAT_GEO_MAP='ddd:mm:ssF',MAP_ANNOT_MIN_SPACING='0.1c',FONT_TITLE = '12p,4,black',FONT_ANNOT_PRIMARY = '12p,4,black',FONT_LABEL = '12p,4,black')

def plot_K(xyz, spacing, region, color_scale, colorbar_type, title, xtitle, ytitle, unit, rows, cols) -> pygmt.Figure:
    fig = pygmt.Figure()
    with fig.subplot(nrows=rows, ncols=cols, subsize=('10c', '5c'), margins=['1c,0.5c']):
        for i in range(cols):
            for j in range(rows):
                with fig.set_panel([j, i]):
                    # coltypes='ig'表示此命令中输入数据的类型，fg表示地理坐标，projection后面加个d表示输入数据是地理坐标
                    fig.basemap(region=region, frame=[
                                'xa60f60','ya60f60',f'+t"{title}"'], projection='Ks10c')
                    # fig.coast(land="black", water="skyblue")
                    grd = pygmt.xyz2grd(
                        data=xyz[:, :, i*4+j], spacing=spacing, region=region, coltypes='ig')
                    # backgroud表示超过色标范围的值是否用底色表示
                    cpt = pygmt.makecpt(
                        cmap=colorbar_type, series=color_scale, continuous=True, reverse=True, background=True)
                    fig.grdimage(grd, cmap=cpt, nan_transparent=True)
                    # fig.coast(shorelines='1/0.1p',land = 'gray', lakes = 'gray', borders=1)
                    fig.coast(shorelines='1/0.1p', borders=1,frame = 'WSen')
                    # position中x10c/0c表示位置在(10c,0)的坐标位置，+m表示把标注放在色标的另一边，+w表示色标长宽，+h/v是绘制水平或垂直色标，+o是额外偏移量，+e表示是否为前景色和后景色加个三角形
                    fig.colorbar(position='jCB+m+w5c/-0.3c+h+o0c/-0.5c+e',frame=["y+lcm/s"])
                    fig.text(position='CM', text=xtitle,
                             offset='0c/3c', no_clip=True)
                    # justify表示锚点位置，意思是以文字的center和middle为原点控制文字的大小和便宜
                    fig.text(position='ML', justify='CM', text=ytitle,
                             offset='-1c/0c', no_clip=True, angle='90')
                    fig.text(position='BR', justify='ML', text=unit,
                             offset='-2.3c/-0.6c',no_clip=True)
    return fig

def plot_X(xyz, spacing, region, color_scale, colorbar_type, colorbar_is_continuous, title, xtitle, ytitle, unit, rows, cols) -> pygmt.Figure:
    fig = pygmt.Figure()
    with fig.subplot(nrows=rows, ncols=cols, subsize=('10c', '5c'), margins=['1c,0.5c']):
        for i in range(cols):
            for j in range(rows):
                with fig.set_panel([j, i]):
                    # coltypes='ig'表示此命令中输入数据的类型，fg表示地理坐标，projection后面加个d表示输入数据是地理坐标
                    fig.basemap(region=region, frame=[
                                'xa60f60','ya60f60',f'+t"{title}"'], projection='X10c/5c')
                    # fig.coast(land="black", water="skyblue")
                    grd = pygmt.xyz2grd(
                        data=xyz[:, :, i*4+j], spacing=spacing, region=region, coltypes='ig')
                    # backgroud表示超过色标范围的值是否用底色表示
                    cpt = pygmt.makecpt(
                        cmap=colorbar_type, series=color_scale, continuous=colorbar_is_continuous, reverse=False, background=True)
                    fig.grdimage(grd, cmap=cpt, nan_transparent=True)
                    # fig.coast(shorelines='1/0.1p',land = 'gray', lakes = 'gray', borders=1,frame = 'WSen')
                    fig.coast(shorelines='1/0.1p', borders=1,frame = 'WSen')
                    # position中x10c/0c表示位置在(10c,0)的坐标位置，+w表示色标长宽，+h/v是绘制水平或垂直色标，+o是额外偏移量，+e表示是否为前景色和后景色加个三角形
                    fig.colorbar(position='jMR+jCM+w5c/0.3c+o0.5c/0c+e')
                    fig.text(position='CM', text=xtitle,
                             offset='0c/3c', no_clip=True)
                    # justify表示锚点位置，意思是以文字的center和middle为原点控制文字的大小和偏移
                    fig.text(position='LM', justify='CM', text=ytitle,
                             offset='-1c/0c', no_clip=True, angle='90')
                    fig.text(position='RT', justify='CM', text=unit,
                             offset='0.5c/0.5c',no_clip=True)
    return fig

def plot_X_amp(xyz, spacing, region, color_scale, color_interval,title, xtitle, ytitle, unit, rows, cols) -> pygmt.Figure:
    fig = pygmt.Figure()
    with fig.subplot(nrows=rows, ncols=cols, subsize=('10c', '5c'), margins=['1c,0.5c']):
        for i in range(cols):
            for j in range(rows):
                with fig.set_panel([j, i]):
                    # coltypes='ig'表示此命令中输入数据的类型，fg表示地理坐标，projection后面加个d表示输入数据是地理坐标
                    fig.basemap(region=region, frame=[
                                'xa60f60','ya60f60',f'+t"{title}"'], projection='X10c/5c')
                    # fig.coast(land="black", water="skyblue")
                    grd = pygmt.xyz2grd(
                        data=xyz[:, :, i*4+j], spacing=spacing, region=region, coltypes='ig')
                    # backgroud表示超过色标范围的值是否用底色表示
                    cpt = pygmt.makecpt(
                        cmap='amp', series=color_scale, continuous=False, reverse=False, background=True)
                    fig.grdimage(grd, cmap=cpt, nan_transparent=True)
                    # fig.coast(shorelines='1/0.1p',land = 'gray', lakes = 'gray', borders=1,frame = 'WSen')
                    fig.coast(shorelines='1/0.1p', borders=1,frame = 'WSen')
                    # position中x10c/0c表示位置在(10c,0)的坐标位置，+w表示色标长宽，+h/v是绘制水平或垂直色标，+o是额外偏移量，+e表示是否为前景色和后景色加个三角形
                    fig.colorbar(position='jMR+jCM+w5c/0.3c+o0.5c/0c+e',frame = [f'x{color_interval}f{color_interval}'])
                    fig.text(position='CM', text=xtitle,
                             offset='0c/3c', no_clip=True)
                    # justify表示锚点位置，意思是以文字的center和middle为原点控制文字的大小和偏移
                    fig.text(position='LM', justify='CM', text=ytitle,
                             offset='-1c/0c', no_clip=True, angle='90')
                    fig.text(position='RT', justify='CM', text=unit,
                             offset='0.5c/0.5c',no_clip=True)
    return fig

def plot_X_pha(xyz, spacing, region, color_scale, color_interval, title, xtitle, ytitle, unit, rows, cols) -> pygmt.Figure:
    fig = pygmt.Figure()
    with fig.subplot(nrows=rows, ncols=cols, subsize=('10c', '5c'), margins=['1c,0.5c']):
        for i in range(cols):
            for j in range(rows):
                with fig.set_panel([j, i]):
                    # coltypes='ig'表示此命令中输入数据的类型，fg表示地理坐标，projection后面加个d表示输入数据是地理坐标
                    fig.basemap(region=region, frame=[
                                'xa60f60','ya60f60',f'+t"{title}"'], projection='X10c/5c')
                    # fig.coast(land="black", water="skyblue")
                    grd = pygmt.xyz2grd(
                        data=xyz[:, :, i*4+j], spacing=spacing, region=region, coltypes='ig')
                    # backgroud表示超过色标范围的值是否用底色表示
                    cpt = pygmt.makecpt(
                        cmap='cmocean/phase', series=color_scale, continuous=False, reverse=False, background=False)
                    fig.grdimage(grd, cmap=cpt, nan_transparent=True)
                    # fig.coast(shorelines='1/0.1p',land = 'gray', lakes = 'gray', borders=1,frame = 'WSen')
                    fig.coast(shorelines='1/0.1p', borders=1,frame = 'WSen')
                    # position中x10c/0c表示位置在(10c,0)的坐标位置，+w表示色标长宽，+h/v是绘制水平或垂直色标，+o是额外偏移量，+e表示是否为前景色和后景色加个三角形
                    fig.colorbar(position='jMR+jCM+w5c/0.3c+o0.5c/0c',frame = [f'xa{color_interval}f{color_interval}'])
                    fig.text(position='CM', text=xtitle,
                             offset='0c/3c', no_clip=True)
                    # justify表示锚点位置，意思是以文字的center和middle为原点控制文字的大小和偏移
                    fig.text(position='LM', justify='CM', text=ytitle,
                             offset='-1c/0c', no_clip=True, angle='90')
                    fig.text(position='RT', justify='CM', text=unit,
                             offset='0.5c/0.5c',no_clip=True)
    return fig