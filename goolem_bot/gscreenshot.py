#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#gbot ctypes from goolem

#notes: https://docs.microsoft.com/es-es/windows/win32/inputdev/virtual-key-codes?redirectedfrom=MSDN
#https://docs.microsoft.com/es-es/windows/win32/api/winuser/nf-winuser-getforegroundwindow?redirectedfrom=MSDN
#import opencv-python mss

####http://kbdlayout.info/kbdsp/virtualkeys


#pillow opencv-python numpy pip install numpy==1.19.3 pip install pywin32
import  ctypes
import os

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
import time # opcional
import datetime
import numpy
#import gaux.hexkeycodes
import win32api, win32con,win32ui,win32gui




class gScreenShot():
    def __init__(self):
        self.window_size=0



    def get(self):
        time.sleep(2)

        # Get the pixel 10 pixels along the top of the foreground window - this
        # will be a piece of the window border.

        foreground_window = ctypes.windll.user32.GetForegroundWindow()
        dc = ctypes.windll.user32.GetWindowDC(ctypes.windll.user32.GetForegroundWindow())
        print ("dc",dc)
        #rgb = ctypes.windll.gdi32.GetPixel(dc, 10, 0)
        ctypes.windll.user32.ReleaseDC(foreground_window, dc)

        # Windows returns colours as RGB values packed into three bytes of a word:
        r = rgb & 0xff
        g = (rgb >> 8) & 0xff
        b = (rgb >> 16) & 0xff
        print ("RGB(%d, %d, %d)" % (r, g, b))  # This prints RGB(0, 74, 216) on my XP machine


if __name__ == "__main__":

    gs=gScreenShot()
    gs.get()
