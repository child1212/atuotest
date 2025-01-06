#%%
import pyautogui
from ctypes import *
import time
import os

def get_color(x,y):
    gdi32 = windll.gdi32
    user32 = windll.user32
    hdc = user32.GetDC(None)
    pixel = gdi32.GetPixel(hdc,x,y)
    r = pixel & 0x0000ff
    g = (pixel & 0x00ff00) >> 8
    b = pixel >> 16
    return [r,g,b]


try:
    run = 0
    while True:
        screenWidth, ScreenHeight = pyautogui.size()
        x,y = pyautogui.position()
        color = get_color(2620,670)
        if run == 0:
            if color == [252, 252, 251]:
                pyautogui.click()
                run = 1
        else:
            if color == [247,231,199]:
                run = 0
except:
    print("end")



# %%
