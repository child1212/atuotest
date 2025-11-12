import adbutils
import time
import subprocess
#%%
import uiautomator2 as u2

# 连接 Android 设备
d = u2.connect()
print(d.info)
# # 截图并保存到指定路径
# screenshot_path = "/sdcard/screenshot.png"
# d.screenshot(screenshot_path)

# # 将截图文件下载到本地
# d.pull(screenshot_path, "local_screenshot.png")


#%%
import adbutils
import re

adb = adbutils.AdbClient(host="127.0.0.1",port=5037)


device = adb.device()

text = device.shell('dumpsys SurfaceFlinger')
# a = re.search(r'TOTAL PSS: +([0-9]+) ',text)
# a = re.search(r'refresh-rate +: +([0-9]+)\.',text)

print(text)
# print(a.group(1))
#%%



print(time.ctime())
for i in range(10):
    # img = device.screenshot()
    # device.screenshot().save("D:/screenshot/skip{x}{y}.jpg".format(x=i,y=1))
    # subprocess.run("adb shell screencap -p /sdcard/screenshot.png")
    # subprocess.run("adb pull /sdcard/screenshot.png D:/screenshot/skip{x}{y}.jpg".format(x=i,y=1))
    # screenshot_path = "D:/screenshot/skip{x}{y}.jpg".format(x=i,y=1)
    d.screenshot()

    # d.pull(screenshot_path, "local_screenshot.jpg")

    # 将截图文件下载到本地
    # d.pull(screenshot_path, "D:/screenshot/skip{x}{y}.jpg".format(x=i,y=1))



print(time.ctime())



# import subprocess
# import cv2
# import numpy as np

# # 启动 scrcpy
# scrcpy_cmd = ["scrcpy"]
# subprocess.Popen(scrcpy_cmd)

# # 创建视频捕捉对象，使用 OpenCV 来捕获屏幕
# cap = cv2.VideoCapture("video=Screen Capture")  # Windows 环境

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("no screen")
#         break
    
#     # 处理图像，进行显示或保存
#     cv2.imshow("Screen Capture", frame)
    
#     # 按 'q' 键退出
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



# import cv2
# import pyautogui

# stream = cv2.VideoCapture('http://localhost:8888/stream.ffm')

# while True:
#     ret, frame = stream.read()
#     if not ret:
#         break

#     # 在这里进行进一步的处理
#     # ...

#     # 显示处理后的帧
#     cv2.imshow('Video Stream', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# stream.release()
# cv2.destroyAllWindows()
#%%
import re
text = '130 com.wanmei.zhuxian.laohu      3597 u0_a319      com.wanmei.zhuxian.laohu'
a = re.search(r'[0-9]+\.?[0-9]?',text)
# %%
