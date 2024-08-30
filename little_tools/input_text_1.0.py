#%%
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
    cmd = input("输入文本：")
    if cmd == "exit":
        threadPool.shutdown(wait=True)
        break
    elif cmd == "":
        for d in ds:
            F = threadPool.submit(d.shell,"input keyevent KEYCODE_ENTER")
    elif cmd == "del":
        for d in ds:
            F = threadPool.submit(d.shell,"input keyevent KEYCODE_MOVE_END")
            F = threadPool.submit(clear_input,d)
    # elif ""
    else:    
        for d in ds:
            F = threadPool.submit(d.shell,['input', 'text', cmd])











# %%
