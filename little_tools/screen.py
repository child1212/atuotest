from adbutils import adb
import threading
from time import sleep




print(adb.device_list)
a = adb.device(adb.device_list()[0].serial)

def screen(x,y):
    a.screenshot().save("D:/screenshot/imag{x}{y}.jpg".format(x=x,y=y))

for i in range(0,1000):
    input("press enter to continue!")
    threading.Thread(target=screen,args=(i,"")).start()