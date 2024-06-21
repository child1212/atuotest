#%%
from adbutils import adb
import threading
from time import sleep




print(adb.device_list)
a = adb.device(adb.device_list()[0].serial)

def screen(x,y):
    a.screenshot().save("D:/screenshot/temp{x}_{y}.jpg".format(x=x,y=y))


for i in range(10):
    a.shell("input tap 1366 597")
    sleep(1)
    threading.Thread(target=screen,args=(i,0)).start()
    a.shell("input tap 1793 828")
    sleep(1)
    threading.Thread(target=screen,args=(i,1)).start()
    a.shell("input tap 1430 939")
    sleep(1)
    threading.Thread(target=screen,args=(i,2)).start()
    a.shell("input tap 1587 926")
    sleep(1)
    threading.Thread(target=screen,args=(i,3)).start()
    a.shell("input tap 1747 933")
    sleep(1)
    threading.Thread(target=screen,args=(i,4)).start()
    a.shell("input tap 1884 935")
    sleep(1)
    threading.Thread(target=screen,args=(i,5)).start()
    a.shell("input tap 2047 921")
    sleep(1)
    threading.Thread(target=screen,args=(i,6)).start()
    a.shell("input tap 2305 206")
    sleep(1)
    threading.Thread(target=screen,args=(i,7)).start()
