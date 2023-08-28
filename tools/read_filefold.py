'''
Author: sweetcoffee qq791227132@gmail.com
Date: 2022-04-28 22:20:46
LastEditors: sweetcoffee qq791227132@gmail.com
LastEditTime: 2023-06-03 20:13:34
FilePath: /ocean_change_python/tools/read_filefold.py
Github: https://github.com/sweetcoffee520
Description: 
Copyright (c) 2022 by sweetcoffee qq791227132@gmail.com, All Rights Reserved.
'''
import os

def read_filefold(foldpath,filetype:str):
    """遍历文件夹下指定类型的文件并添加至all_file_path列表

    Args:
        foldpath (str): 文件夹目录
        filetype (str): 文件类型
        all_file_path(list):

    Returns:
        list: 文件路径列表
    """
    all_file_path = []
    if os.path.isdir(foldpath):
        all_path = os.listdir(foldpath)
        for path in all_path:
            file_path = os.path.join(foldpath,path)
            # all_file_path.append(read_filefold(file_path,filetype))
            all_file_path += read_filefold(file_path,filetype)
    # 如果是文件则返回值
    elif os.path.isfile(foldpath) and os.path.splitext(foldpath)[1][1:] == filetype:
        all_file_path.append(foldpath)

    return all_file_path.sort()

def read_file_fold(foldpath,filetypes:str or list):
    """第二种方法遍历文件夹

    Args:
        foldpath (str): 文件夹目录
        filetype (str): 文件类型

    Returns:
        list: 文件路径列表
    """
    if isinstance(filetypes,str):
        filetypes = [filetypes]
    all_file_list = []
    for root,dirs,files in os.walk(foldpath):
        for filename in files:
            if os.path.splitext(filename)[1][1:] in filetypes:
                all_file_list.append(os.path.join(root,filename))
    all_file_list.sort()
    return all_file_list
