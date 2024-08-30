from adbutils import adb
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

ds = adb.device_list()
device_set = set()
for de in ds:
    device_set.add(adb.device(de.serial))
print("检测到{t}台设备：".format(t=len(ds)))
threadPool = ThreadPoolExecutor(max_workers=len(ds),thread_name_prefix="test_")

def clear_input(device):
    for i in range(30):
        threading.Thread(target=device.shell,args=("input keyevent 67",)).start()

while True:
    cmd = input("输入key：")
    if cmd == "exit":
        threadPool.shutdown(wait=True)
        break
    elif cmd == "back":
        for d in ds:
            F = threadPool.submit(d.shell,"input keyevent KEYCODE_BACK")
    elif cmd == "home":
        for d in ds:
            F = threadPool.submit(d.shell,"input keyevent KEYCODE_HOME")
    elif cmd == "+":
        for d in ds:
            F = threadPool.submit(d.shell,"input keyevent KEYCODE_VOLUME_UP")
    elif cmd == "-":
        for d in ds:
            F = threadPool.submit(d.shell,"input keyevent KEYCODE_VOLUME_DOWN")
    elif cmd == "poweroff":
        for d in ds:
            F = threadPool.submit(d.shell,"reboot -p")
    else:    
        for d in ds:
            F = threadPool.submit(d.shell,['input', 'text', cmd])
