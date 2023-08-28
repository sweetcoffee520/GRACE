import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import ArrowStyle
import numpy as np

plt.rcParams.update({
    'font.family': 'Arial',
})
def plot_line(*arg,title=None,xtitle=None,ytitle=None,color=None,ticktype = 'date'):
    """折线图

    Args:
        arg 画图,参数为二维元组,一对(x1,y1,dash_type1,name1),一个元组,长度可变
        title (_type_, optional): _description_. Defaults to None.
        xtitle (_type_, optional): _description_. Defaults to None.
        ytitle (_type_, optional): _description_. Defaults to None.
        color (_type_, optional): _description_. Defaults to None.
        ticktype (str, optional): 'date' or 'linear'. Defaults to 'date'.

    Returns:
        _type_: _description_
    """
    # 创建画布
    fig, ax = plt.subplots()
    fig.set_facecolor('#ffffff')
    fig.set_size_inches(24,16)
    ax.set_facecolor('white')
    # 绘制线条
    for i in range(len(arg)):
        if color is None:
            if arg[i][2] == '':
                if arg[i][3] == '':
                    ax.plot(arg[i][0],arg[i][1], label='',marker='o',linewidth=3)
                else:
                    ax.plot(arg[i][0],arg[i][1], label=arg[i][3],marker='o',linewidth=3)
            else:
                if arg[i][3] == '':
                    ax.plot(arg[i][0],arg[i][1], label='',marker='o',linestyle=arg[i][2],linewidth=3)
                else:
                    ax.plot(arg[i][0],arg[i][1], label=arg[i][3],marker='o',linestyle=arg[i][2],linewidth=3)
        else:
            if arg[i][2] == '':
                if arg[i][3] == '':
                    ax.plot(arg[i][0],arg[i][1], label='',color=color[i],marker='o',linewidth=3)
                else:
                    ax.plot(arg[i][0],arg[i][1], label=arg[i][3],color=color[i],marker='o',linewidth=3)
            else:
                if arg[i][3] == '':
                    ax.plot(arg[i][0],arg[i][1], label='',marker='o',color=color[i],linestyle=arg[i][2],linewidth=3)
                else:
                    ax.plot(arg[i][0],arg[i][1], label=arg[i][3],marker='o',color=color[i],linestyle=arg[i][2],linewidth=3)

    # 设置x轴
    ax.set_xlabel(xlabel=xtitle, fontsize=40, color='black',labelpad=20)
    if ticktype == 'date':
        ax.xaxis.set_major_locator(mdates.YearLocator(base=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=1))

    elif ticktype == 'linear':
        pass
    ax.tick_params(axis='x', labelsize=30, pad=20)
    ax.grid(axis='x', linewidth=1, linestyle='-', color='#e0e0e0',which='both')
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.tick_params(axis='x', which='major',length=10, width=2, colors='black',top=True)
    ax.tick_params(axis='x', which='minor',length=5, width=1, colors='black',top=True)
    ax.tick_params(axis='x', which='both', direction='out')
    ax.tick_params(axis='x', which='major', pad=10)

    # 设置y轴
    ax.set_ylabel(ylabel=ytitle, fontsize=40, color='black',labelpad=20)
    ax.tick_params(axis='y', labelsize=30, pad=20)
    ax.grid(axis='y', linewidth=1, linestyle='-', color='#e0e0e0')
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.tick_params(axis='y', length=8, width=2, colors='black',right=True)
    ax.tick_params(axis='y', which='both', direction='out')
    ax.tick_params(axis='y', which='major', pad=10)

    # 设置标题和图例
    ax.set_title(label=title,fontdict={'size':40,'color':'k'})
    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98),fancybox=False,fontsize=30, edgecolor='black', borderpad=0.4, labelspacing=0.5, handlelength=1, handletextpad=0.5,facecolor='white',labelcolor='black')

    return fig,ax

class subplot(object):
    fig = None
    ax = None
    def __init__(self,rows,cols,title=None,xtitle=None,ytitle=None,color=None,sub_titles=None,sharex=False,sharey=False,tick_type='date') -> None:
        self.rows = rows
        self.cols = cols
        self.title = title
        self.xtitle = xtitle
        self.ytitle = ytitle
        self.color = color
        self.sharex = sharex
        self.sharey = sharey
        self.sub_titles = sub_titles
        self.tick_type = tick_type

    def sub_plots(self,*arg):
        """画图,参数为二维元组,一对((x1,y1,dash_type1,name1),(x2,y2,dash_type2,name2),xlabel,ylable),一个元组,长度可变"""
        self.fig, self.ax = plt.subplots(nrows=self.rows,ncols=self.cols,sharex=self.sharex,sharey=self.sharey)
        if self.rows == 1:
            self.ax = self.ax[None,:]
        else:
            pass
        if self.cols == 1:
            self.ax = self.ax[:,None]
        else:
            pass
        self.fig.set_facecolor('#ffffff')
        self.fig.set_size_inches(24,16)
        for r in range(self.rows):
            for c in range(self.cols):
                self.ax[r,c].set_facecolor('white')
                subplot_num = r*self.cols+c
                plot_line_num = len(arg[subplot_num])-2
                for i in range(plot_line_num):
                    if self.color is None:
                        if arg[subplot_num][i][2] == '':
                            if arg[subplot_num][i][3] == '':
                                self.ax[r,c].plot(arg[subplot_num][i][0],arg[subplot_num][i][1], label='',marker='o',linewidth=3)
                            else:
                                self.ax[r,c].plot(arg[subplot_num][i][0],arg[subplot_num][i][1], label=arg[subplot_num][i][3],marker='o',linewidth=3)
                        else:
                            if arg[subplot_num][i][3] == '':
                                self.ax[r,c].plot(arg[subplot_num][i][0],arg[subplot_num][i][1], label='',marker='o',linestyle=arg[subplot_num][i][2],linewidth=3)
                            else:
                                self.ax[r,c].plot(arg[subplot_num][i][0],arg[subplot_num][i][1], label=arg[subplot_num][i][3],marker='o',linestyle=arg[subplot_num][i][2],linewidth=3)
                    else:
                        if arg[subplot_num][i][2] == '':
                            if arg[subplot_num][i][3] == '':
                                self.ax[r,c].plot(arg[subplot_num][i][0],arg[subplot_num][i][1], label='',color=self.color[i],marker='o',linewidth=3)
                            else:
                                self.ax[r,c].plot(arg[subplot_num][i][0],arg[subplot_num][i][1], label=arg[subplot_num][i][3],color=self.color[i],marker='o',linewidth=3)
                        else:
                            if arg[subplot_num][i][3] == '':
                                self.ax[r,c].plot(arg[subplot_num][i][0],arg[subplot_num][i][1], label='',marker='o',color=self.color[i],linestyle=arg[subplot_num][i][2],linewidth=3)
                            else:
                                self.ax[r,c].plot(arg[subplot_num][i][0],arg[subplot_num][i][1], label=arg[subplot_num][i][3],marker='o',color=self.color[i],linestyle=arg[subplot_num][i][2],linewidth=3)    # 设置x轴

                if self.sub_titles is not None:
                    self.ax[r,c].set_title(self.sub_titles[subplot_num],fontsize=40,color='black',pad=30)

                self.ax[r,c].set_xlabel(xlabel=arg[subplot_num][-2], fontsize=40, color='black')
                if self.tick_type == 'date':
                    self.ax[r,c].xaxis.set_major_locator(mdates.YearLocator(base=2))
                    self.ax[r,c].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
                    self.ax[r,c].xaxis.set_minor_locator(mdates.YearLocator(base=1))
                    # self.ax[r,c].xaxis.set_minor_formatter(mdates.DateFormatter('%Y'))
                elif self.tick_type == 'linear':
                    pass
                self.ax[r,c].tick_params(axis='x', labelsize=30, pad=20)
                self.ax[r,c].grid(axis='x', linewidth=1, linestyle='-', color='#e0e0e0',which='both')
                self.ax[r,c].spines['bottom'].set_linewidth(2)
                self.ax[r,c].spines['top'].set_linewidth(2)
                self.ax[r,c].spines['bottom'].set_color('black')
                self.ax[r,c].spines['top'].set_color('black')
                self.ax[r,c].tick_params(axis='x', which='major',length=10, width=2, colors='black',top=True)
                self.ax[r,c].tick_params(axis='x', which='minor',length=5, width=1, colors='black',top=True)
                self.ax[r,c].tick_params(axis='x', which='both', direction='out')
                self.ax[r,c].tick_params(axis='x', which='major', pad=10)

                # 设置y轴
                self.ax[r,c].set_ylabel(ylabel=arg[subplot_num][-1], fontsize=40, color='black')
                self.ax[r,c].tick_params(axis='y', labelsize=30, pad=20)
                self.ax[r,c].grid(axis='y', linewidth=1, linestyle='-', color='#e0e0e0')
                self.ax[r,c].spines['left'].set_linewidth(2)
                self.ax[r,c].spines['right'].set_linewidth(2)
                self.ax[r,c].spines['left'].set_color('black')
                self.ax[r,c].spines['right'].set_color('black')
                self.ax[r,c].tick_params(axis='y', length=8, width=2, colors='black',right=True)
                self.ax[r,c].tick_params(axis='y', which='both', direction='out')
                self.ax[r,c].tick_params(axis='y', which='major', pad=10)

                # 设置标题和图例
                self.ax[r,c].legend(loc='upper left', bbox_to_anchor=(0.02, 0.98),fancybox=False,fontsize=30, edgecolor='black', borderpad=0.4, labelspacing=0.5, handlelength=1, handletextpad=0.5,facecolor='white',labelcolor='black')
            plt.suptitle(self.title,fontsize=40,color='k')
            self.fig.text(0.5, 0.04, self.xtitle, ha='center')
            self.fig.text(0.04, 0.5, self.ytitle, va='center', rotation='vertical')

    def remove_sub_legend(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.ax[r,c] is not None:
                    self.ax[r,c].legend().remove()

    def date_format(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.ax[r,c] is not None:
                    self.ax[r,c].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

#TODO 未完成
def pha_vector_plot(pha_array,amp_array,linelabel,color,origin_coor=None):
    """

    Args:
        pha_array (array): 角度数组，非弧度
        linelabel (tuple or list): 线条标签
        color (_type_): _description_
        origin_coor (tuple): 起点坐标
    """

    my_arrow_style = ArrowStyle('-|>',head_length=2,head_width=0.6)
    pha_rad = np.radians(pha_array)
    fig, ax = plt.subplots()
    fig.set_facecolor('#ffffff')
    fig.set_size_inches(24,16)
    ax.set_facecolor('white')
    if origin_coor:
        for i in range(len(pha_array)):
            ax.plot([0,amp_array[i]*np.sin(pha_rad[i])],[0,amp_array[i]*np.cos(pha_rad[i])],linewidth=3,color=color[i],label=linelabel[i])
            ax.annotate('',xy=(1.01*amp_array[i]*np.sin(pha_rad[i]),1.01*amp_array[i]*np.cos(pha_rad[i])),xytext=(0,0),arrowprops=dict(arrowstyle=my_arrow_style,color=color[i],lw=3))
    ax.set_xlabel(xlabel='Sine(mm)', fontsize=40, color='black',labelpad=20)
    ax.tick_params(axis='x', labelsize=30, pad=20)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.tick_params(axis='x', which='major',length=10, width=2, colors='black',top=True)
    ax.tick_params(axis='x', which='minor',length=5, width=1, colors='black',top=True)
    ax.tick_params(axis='x', which='both', direction='out')
    ax.tick_params(axis='x', which='major', pad=10)

    # 设置y轴
    ax.set_ylabel(ylabel='Cosine(mm)', fontsize=40, color='black',labelpad=20)
    ax.tick_params(axis='y', labelsize=30, pad=20)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.tick_params(axis='y', length=8, width=2, colors='black',right=True)
    ax.tick_params(axis='y', which='both', direction='out')
    ax.tick_params(axis='y', which='major', pad=10)

    # 设置标题和图例
    ax.set_title(label='',fontdict={'size':40,'color':'k'})
    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98),fancybox=False,fontsize=30, edgecolor='black', borderpad=0.4, labelspacing=0.5, handlelength=1, handletextpad=0.5,facecolor='white',labelcolor='black')