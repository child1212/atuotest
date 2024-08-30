from adbutils import adb
import threading

ds = adb.device_list()
print("检测到{n}台设备".format(n=len(ds)))
p = input("apkpath:\n")
name = p.split("\\")[-1]
pat = "/sdcard/Download/{name}".format(name=name)
for d in ds:
    r = adb.device(d.serial)
    threading.Thread(target=r.sync.push,args=(p,pat)).start()
