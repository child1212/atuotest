# -- coding: UTF-8 --
from win32gui import *
from PIL import ImageGrab
import win32con
import time
import win32com.client
import pyautogui
import threading
import sys
import numpy
import tkinter
import cv2 as cv
import ctypes
import random

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
if is_admin():
    pass
else:
    ctypes.windll.shell32.ShellExecuteW(None,"runas",sys.executable,__file__,None,1)
pyautogui.FAILSAFE = False


#鼠标点击函数
def mouse_click(box,position):
    if position[0]:
        pyautogui.click(box[0]+position[1],box[1]+position[2])
        pyautogui.moveTo(10,10,duration=0.2)
        print("mouse_click",position[1],position[2])
        return True
    else:
        return False
    

def get_window_title(window,names):
    '''
    获取窗口标题函数
    :param window: 窗口对象
    :param nouse:
    :return:
    '''
    if IsWindow(window) and IsWindowEnabled(window) and IsWindowVisible(window):
        names.add(GetWindowText(window))

#检测游戏开启
def check_window_zx():
    names = set()
    EnumWindows(get_window_title,names)
    list_ = [name for name in names if name]
    if '梦幻新诛仙 手游模拟器' in names:
        return True
    else: 
        return False

#游戏置顶
def zx_on_top():
    name = '梦幻新诛仙 手游模拟器'
    window = FindWindow(0,name)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')

    ShowWindow(window,win32con.SW_MAXIMIZE)
    SetForegroundWindow(window)

#截取整个游戏截图
def get_zx_screen(screen_name="template.png"):
    name = '梦幻新诛仙 手游模拟器'
    window = FindWindow(0,name)
    # shell = win32com.client.Dispatch("WScript.Shell")
    # shell.SendKeys('%')
    # ShowWindow(window,win32con.SW_MAXIMIZE)
    # SetForegroundWindow(window)
    x_start, y_start, x_end, y_end = GetWindowRect(window)
    box = (x_start, y_start, x_end, y_end)
    if abs(x_end-x_start-1920)>1 or abs(y_end-y_start-1080)>1:
        raise(TypeError)
        print("屏幕分辨率错误,请设置分辨率为1920x1080!")
        return box
    time.sleep(1)
    # image = ImageGrab.grab(box)
    image = pyautogui.screenshot(region=box)
    # image.save(screen_name)
    print("截图:",x_end-x_start,"x",y_end-y_start)
    return box,image
def get_screen_box(x_start, y_start, x_end, y_end,screen_name="box.png"):
    box = (x_start, y_start, x_end, y_end)
    image = pyautogui.screenshot(region=box)
    image.save(screen_name)
    return box,image

#查找目标icon，返回坐标，未找到返回False
def find_icon(icon,screencap,stand=0.99,position=5):
    '''
    screencap:屏幕截图路径
    icon:要寻找的目标
    stand:图像识别阈值
    '''
    img = cv.imread(icon)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    w,h = gray.shape[::-1]
    # img1 = cv.imread(screencap)
    gray1 = cv.cvtColor(numpy.array(screencap), cv.COLOR_BGR2GRAY)
    match = cv.matchTemplate(gray,gray1,cv.TM_CCORR_NORMED)
    # print(cv.minMaxLoc(match)[1])
    if cv.minMaxLoc(match)[1]>stand:
        min_val, max_val, min_loc, max_loc =cv.minMaxLoc(match)
        top_left = max_loc
        middle = (top_left[0] + w//2,top_left[1] + h//2)
        bottom_right = (top_left[0] + w,top_left[1] + h)
        print(middle[0],middle[1])
        if position==1:
            return True,top_left[0],top_left[1]
        elif position==2:
            return True,middle[0],top_left[1]
        elif position==3:
            return True,bottom_right[0],top_left[1]
        elif position ==4:
            return True,top_left[0],middle[1]
        elif position ==5:
            return True,middle[0],middle[1]
        elif position == 6:
            return True,bottom_right[0],middle[1]
        elif position == 7:
            return True,top_left[0],bottom_right[1]
        elif position == 8:
            return True,middle[0],bottom_right[1]
        elif position == 9:
            return True,bottom_right[0],bottom_right[1]
    else:
        return False,0,0

def find_icon_quick(gray,screencap,stand=0.99,position=5):
    '''
    screencap:屏幕截图路径
    icon:要寻找的目标
    stand:图像识别阈值
    '''
    w,h = gray.shape[::-1]
    # img1 = cv.imread(screencap)
    gray1 = cv.cvtColor(numpy.array(screencap), cv.COLOR_BGR2GRAY)

    match = cv.matchTemplate(gray,gray1,cv.TM_CCORR_NORMED)
    # print(cv.minMaxLoc(match)[1])
    if cv.minMaxLoc(match)[1]>stand:
        min_val, max_val, min_loc, max_loc =cv.minMaxLoc(match)
        top_left = max_loc
        middle = (top_left[0] + w//2,top_left[1] + h//2)
        bottom_right = (top_left[0] + w,top_left[1] + h)
        print(middle[0],middle[1])
        if position==1:
            return True,top_left[0],top_left[1]
        elif position==2:
            return True,middle[0],top_left[1]
        elif position==3:
            return True,bottom_right[0],top_left[1]
        elif position ==4:
            return True,top_left[0],middle[1]
        elif position ==5:
            return True,middle[0],middle[1]
        elif position == 6:
            return True,bottom_right[0],middle[1]
        elif position == 7:
            return True,top_left[0],bottom_right[1]
        elif position == 8:
            return True,middle[0],bottom_right[1]
        elif position == 9:
            return True,bottom_right[0],bottom_right[1]
    else:
        return False,0,0


def icon_exist(icon,screencap,stand=0.99):
    img = cv.imread(icon)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    w,h = gray.shape[::-1]
    # img1 = cv.imread(screencap)
    gray1 = cv.cvtColor(numpy.array(screencap), cv.COLOR_BGR2GRAY)
    match = cv.matchTemplate(gray,gray1,cv.TM_CCORR_NORMED)
    # print(cv.minMaxLoc(match)[1])
    if cv.minMaxLoc(match)[1]>stand:
        return True

def icon_exist_quick(gray,screencap,stand=0.98):
    w,h = gray.shape[::-1]
    # img1 = cv.imread(screencap)
    gray1 = cv.cvtColor(numpy.array(screencap), cv.COLOR_BGR2GRAY)

    match = cv.matchTemplate(gray,gray1,cv.TM_CCORR_NORMED)
    # print(cv.minMaxLoc(match)[1])
    if cv.minMaxLoc(match)[1]>stand:
        return True


def make_ans(icon,screencap,ans_l):
    if icon_exist(icon,screencap):
        ans_l.append(int(icon[1]))

# 
if __name__ == '__main__':
    zx_on_top()
    get_zx_screen()
    get_screen_box(1800,30,80,70)
    run = 0
    chat = 450
    mission = cv.imread("box.png")
    mission_gray = cv.cvtColor(mission,cv.COLOR_BGR2GRAY)
    while True:
        x,y = get_zx_screen()
        pos = find_icon_quick(mission_gray,y)
        if pos[0]:
            pyautogui.click(1550,180)
        else:
            if run == 0:
                if chat == 750:
                    chat = 450
                for i in range(10):
                    pyautogui.press("space")
                pyautogui.click(1500,820)
                time.sleep(0.5)
                pyautogui.click(965,1040)
                time.sleep(0.5)
                pyautogui.click(1500,970)
                time.sleep(0.5)
                pyautogui.click(1250,chat)
                run += 1
                chat += 100
                # pyautogui.click(1800,63)
            elif run == 1:
                for i in range(10):
                    pyautogui.click(968,982)      
                    time.sleep(0.2)
                pyautogui.click(1800,63)
                run += 1
            elif run == 2:
                pyautogui.press("esc")
                run = 0





