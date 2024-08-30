#%%
from adbutils import adb
import threading

ds = adb.device_list()
print("检测到{n}台设备".format(n=len(ds)))
p = input("apkpath:\n")
if p == "test":
    for d in ds:
        r = adb.device(d.serial)
        threading.Thread(target=r.shell,args=("input swipe 300 0 300 300",)).start()
else:
    for d in ds:
        r = adb.device(d.serial)
        threading.Thread(target=r.install,args=(p,)).start()











