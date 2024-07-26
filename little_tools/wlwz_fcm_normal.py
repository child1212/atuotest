#%%
from adbutils import adb
import os

d = adb.device(adb.device_list()[0].serial)
operate = input("拖入配置文件")
with open(operate,"r") as f:
    for line in f:
        line = line.replace("\n",'')
        if "screencap" in line:
            print("这里截图一张")
        elif "stop" in line:
            os._exit()
        elif "pass" in line:
            pass
        else:
            input("")
            print(line)
            d.shell(line)
























# %%
