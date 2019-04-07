#!/usr/bin/env python3
#-*- coding:utf-8 -*-
'''
本地调试时，python3 main.py即可启动本程序
Created on 2019年3月3日
@author: bkd
'''
from tkinter import messagebox

if __name__ == '__main__':
    from kdPythonAPIViewer.kdPythonAPIViewer import main
    try:
        main()
    except Exception as e:
        messagebox.showerror("系统异常", str(e))