#%%
from adbutils import adb
import threading
from time import sleep

print(adb.device_list)
a = adb.device(adb.device_list()[0].serial)
#%%
for i in range(150):
    a.shell("input tap 2309 1078")
    sleep(0.2)
    # a.shell("input tap 1793 828")
    # sleep(1)
    # a.shell("input tap 1430 939")
    # sleep(1)
    # a.shell("input tap 1587 926")
    # sleep(1)
    # a.shell("input tap 1747 933")
    # sleep(1)
    # a.shell("input tap 1884 935")
    # sleep(1)
    # a.shell("input tap 2047 921")
    # sleep(1)
    # a.shell("input tap 2305 206")
    # sleep(1)


#%%
p=300033
# p=100069
h = 20402


a.shell("input text 'addhero {h}'\n".format(h=h))
a.shell("input keyevent 66")
a.shell("input text 'additem {p} 100'".format(p = p))
a.shell("input keyevent 66")


