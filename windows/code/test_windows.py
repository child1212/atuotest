

from win32gui import *
from PIL import ImageGrab
import win32con
import time
import cv2 as cv
import win32com.client
import pyautogui
import threading
import sys

import tkinter

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
    if '诛仙手游 官方桌面版' in names:
        return True
    else: 
        return False

#游戏置顶
def zx_on_top():
    name = '诛仙手游 官方桌面版'
    window = FindWindow(0,name)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')

    ShowWindow(window,win32con.SW_MAXIMIZE)
    SetForegroundWindow(window)

#截取整个游戏截图
def get_zx_screen(screen_name):
    name = '诛仙手游 官方桌面版'
    window = FindWindow(0,name)
    # shell = win32com.client.Dispatch("WScript.Shell")
    # shell.SendKeys('%')
    # ShowWindow(window,win32con.SW_MAXIMIZE)
    # SetForegroundWindow(window)
    x_start, y_start, x_end, y_end = GetWindowRect(window)
    box = (x_start, y_start, x_end, y_end)
    if abs(x_end-x_start-1920)>1 or abs(y_end-y_start-1080)>1:
        print("屏幕分辨率错误,请设置分辨率为1920x1080!")
        return box
    time.sleep(1)
    # image = ImageGrab.grab(box)
    image = pyautogui.screenshot(region=box)
    image.save(screen_name)
    print("截图:",x_end-x_start,"x",y_end-y_start)
    return box

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
    img1 = cv.imread(screencap)
    gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
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
    img1 = cv.imread(screencap)
    gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    match = cv.matchTemplate(gray,gray1,cv.TM_CCORR_NORMED)
    # print(cv.minMaxLoc(match)[1])
    if cv.minMaxLoc(match)[1]>stand:
        return True

def make_ans(icon,screencap,ans_l):
    if icon_exist(icon,screencap):
        ans_l.append(int(icon[1]))

def hand_loop(template,jldw):
    #点击酒令，寻找酒令一
    print("点击酒令，寻找酒令")
    jiuling_title_path = "jiuling_title.png"
    jiuling_path = "jiuling{i}.png".format(i=jldw)
    box = get_zx_screen(template)
    jiuling = find_icon(jiuling_path,template)
    if jiuling[0] == False:
        mouse_click(box,find_icon(jiuling_title_path,template))
    #点击酒令一
    print("点击酒令一子菜单")
    box = get_zx_screen(template)
    mouse_click(box,find_icon(jiuling_path,template))
    box = get_zx_screen(template)
    #点击前往
    print("点击前往")
    go_path = "go.png"
    mouse_click(box,find_icon(go_path,template))
    box=get_zx_screen(template)
    mouse_click(box,find_icon(go_path,template))
    time.sleep(1)
    box=get_zx_screen(template)

    #检测行酒令条目并点击
    print("检测行酒令条目并点击")
    jiuling_button_path = "jiuling_button.png"
    mouse_click(box,find_icon(jiuling_button_path,template,0.99))

    #检测活动说明界面
    # box=get_zx_screen(template)
    # print("检测活动说明界面")
    # introduction_path = "introduction.png"
    # mouse_click(box,find_icon(introduction_path,template,0.99,position=3))
    #循环执行划拳脚本、划拳脚本中，检测任务成功、任务失败
    time.sleep(3.5)
    print("循环执行划拳脚本、划拳脚本中，检测任务成功、任务失败")
    hand_set = {"l0.png","l1.png","l2.png","l3.png","l4.png","l5.png","r1.png","r2.png","r3.png","r4.png","r5.png"}
    running = 0
    while running<3:
        print("running",running)
        ans_l = []
        box=get_zx_screen(template)
        for icon in hand_set:
            if icon_exist(icon,template):
                ans_l.append(int(icon[1]))
        ans = sum(ans_l)
        print("划拳结果为：",ans)
        print("寻找点击位置...")
        ans_path = "ans{ans}.png".format(ans=ans)
        result = mouse_click(box,find_icon(ans_path,template,0.99))
        if result == False:
            running += 1


    #任务失败，直接点击再次挑战
    print("点击再次挑战")            
    mission_fail_path = "mission_fail.png"
    mouse_click(box,find_icon(mission_fail_path,template,0.99,position=7))
    #任务成功，点击完成
    print("任务成功，点击完成")
    mission_succeed_path = "complete.png"
    mouse_click(box,find_icon(mission_succeed_path,template,0.99,position=8))
    box=get_zx_screen(template)
    #领奖
    print("领奖")
    ok_path = "ok.png"
    mouse_click(box,find_icon(ok_path,template,0.99,position=8))
    mouse_click(box,find_icon(ok_path,template,0.99,position=8))

def whole_loop(x=1,y="y",i=1,nouse=False):
    a = 0
    template = "template.png"
    # if i not in (1,2,3) or y not in ('n', 'y'):
    #     raise ValueError("invalid input")


    # #检测进入游戏
    # # zx_on_top()
    # run = check_window_zx()
    # if run == False:
    #     print("未检测到客户端，请检查游戏是否开启!")
    #     input("press enter to exit...")
    # else:
    #点击头像、点击帮派、点击帮派筹建
    # headicon_path = "headicon.png"
    gang_path = "gang.png"
    preparation_path = "preparation.png"
    box=get_zx_screen(template)
    # mouse_click(box,find_icon(headicon_path,template,stand=0.95))
    box=get_zx_screen(template)
    mouse_click(box,find_icon(gang_path,template,stand=0.987))
    box=get_zx_screen(template)
    mouse_click(box,find_icon(preparation_path,template,stand=0.987))

    #点击寻奇，检测寻奇条目关闭
    xunqi_path = "xunqi.png"
    xunqi_title_path = "xunqi_title.png"
    box=get_zx_screen(template)
    xunqi = find_icon(xunqi_path,template)
    if xunqi[0] == True:
        mouse_click(box,find_icon(xunqi_title_path,template))


    while(a<x):
        hand_loop(template,i)
        if y == "n":
            input("press 'Enter' to continue!")
        a += 1    
    return 1


def start_command():
    def run_command():
        window_running = tkinter.Tk()
        window_running.title("点击器")
        window_running.geometry("100x100")
        lable_running = tkinter.Label(window_running,text = "脚本执行完毕")
        lable_running.pack()
        # def exit_tk():
        #     exit()
        btnStop = tkinter.Button(window_running,height=1,text="exit",command=sys.exit)
        btnStop.pack()
        # try:
        x = int(text_times.get("1.0","end"))
        y = text_loop.get("1.0","end")
        y = y.replace("\n","")
        i = int(text_level.get("1.0","end"))
        # except:
        #     print("输入的参数-错误！")
        #     input("press enter to exit...")
        #     window_running.mainloop()

        window.destroy()
        if i not in (1,2,3) or y not in ('n', 'y'):
            print("输入的参数错误！")
            input("press enter to exit...")
            window_running.mainloop()

        # #检测进入游戏
        # # zx_on_top()
        run = check_window_zx()
        if run == False:
            print("未检测到客户端，请检查游戏是否开启!")
            input("press enter to exit...")
            window_running.mainloop()
        whole_loop(x=x,y=y,i=i)
        window_running.mainloop()
    window = tkinter.Tk()
    
    window.title("诛仙-行酒令")

    window.geometry("200x200")

    label_times = tkinter.Label(window,text="请在下方输入循环次数：",height=1)
    label_times.pack()
    text_times = tkinter.Text(window,height=1)
    text_times.insert(tkinter.END,3)
    text_times.pack()

    label_loop = tkinter.Label(window,text="请在下方输入是否连续执行(n/y)",height=1)
    label_loop.pack()
    text_loop = tkinter.Text(window,height=1)
    text_loop.insert(tkinter.END,'y')
    text_loop.pack()

    label_level = tkinter.Label(window,text="请在下方输入行酒令等级(1/2/3)",height=1)
    label_level.pack()
    text_level = tkinter.Text(window,height=1) 
    text_level.insert(tkinter.END,1)
    text_level.pack()

    btnRun = tkinter.Button(window,height=1,text="RUN",command=run_command)
    btnRun.pack()
    # main()

    window.mainloop()

if __name__ == '__main__':
    start_command()


