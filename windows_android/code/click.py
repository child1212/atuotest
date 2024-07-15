# --author--lienfeng --

from win32gui import *
from PIL import ImageGrab
import win32con
import time
import win32com.client

names = set()

def get_window_title(window,nouse):
    '''
    获取窗口标题函数
    :param window: 窗口对象
    :param nouse:
    :return:
    '''
    if IsWindow(window) and IsWindowEnabled(window) and IsWindowVisible(window):
        names.add(GetWindowText(window))

EnumWindows(get_window_title,0)

list_ = [name for name in names if name]

for n in list_:
    print("活动窗口：", n)


name = input('请输入需要截图的活动窗口名称: \n')
# name = input('诛仙手游 官方桌面版')

window = FindWindow(0,name)
shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')
ShowWindow(window,win32con.SW_MAXIMIZE)
SetForegroundWindow(window)

x_start, y_start, x_end, y_end = GetWindowRect(window)

box = (x_start, y_start, x_end, y_end)

time.sleep(1)

image = ImageGrab.grab(box)

image.save('target.png')

#%%
from win32gui import *
from PIL import ImageGrab
import win32con
import time
import win32com.client
import pyautogui
name = '雷电模拟器'

window = FindWindow(0,name)
# shell = win32com.client.Dispatch("WScript.Shell")
# shell.SendKeys('%')
# ShowWindow(window,win32con.SW_MAXIMIZE)
# SetForegroundWindow(window)

x_start, y_start, x_end, y_end = GetWindowRect(window)

box = (x_start, y_start, x_end, y_end)
print(box)
time.sleep(1)

image = pyautogui.screenshot(region=box)

image.show()
# image = ImageGrab.grab(box)

# image.save('target1.png')

# %%
