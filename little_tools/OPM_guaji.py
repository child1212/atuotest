#%%
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import threading
import time
def test(value1, value2,value3):
    # print("{a} threading is printed {b}, {c}".format(a=threading.current_thread().name, b=value1, c=value2))
    print(sum((value1, value2,value3)))
    time.sleep(2)
    return 'finished'
 
def test_result(future):
    print(future.result())

threadPool = ThreadPoolExecutor(max_workers=3, thread_name_prefix="test_")
for i in range(0,10):
    future = threadPool.submit(test, i,i+1,i+2)
threadPool.shutdown(wait=True)





# %%
# from queue import Queue
# import time,threading
# q = Queue(maxsize=0)

# def product():
#     while True:
#         x =input("输入：")
#         q.put("气球"+x)

# def consume(name):
#     while True:
#         print("{} use {}".format(name,q.get()))
#         q.task_done()
# t1 = threading.Thread(target=product)
# t2 = threading.Thread(target=consume,args=("ypp",))
# t3 = threading.Thread(target=consume,args=("others",))

# t1.start()
# t2.start()
# t3.start()
# %% 
# 录入device id


# from adbutils import adb
# import json
# deviceId = open("deviceId.json","r")
# device = json.load(deviceId)
# deviceId.close()
# ser = adb.device_list()[0].serial
# x = "A-{n}".format(n=input("输入设备编号："))
# if device.get(x) != None:
#     input("设备已录入！")
# device[x] = ser
# data = json.dumps(device)
# deviceId = open("deviceId.json","w")
# deviceId.write(data)
# deviceId.close()


#%%
# import json
# deviceId = open("deviceId.json","r")
# device = json.load(deviceId)
# aaa = ["030","046","066","067","229","246"]
# for i in aaa:
#     nums = device.keys()
#     if "A-{n}".format(n=i) not in nums:
#         print(i,end=",")



# %%
from adbutils import adb
import json
deviceId = open("deviceId.json","r")
device = json.load(deviceId)
deviceId.close()
deviceName = {}
for key in device.keys():
    deviceName[device[key]] = key
data = json.dumps(deviceName)
deviceId = open("deviceName.json","w")
deviceId.write(data)
deviceId.close()
