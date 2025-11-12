from adbutils import adb
import threading
from time import sleep




print(adb.device_list)
a = adb.device(adb.device_list()[0].serial)

def screen(x,y):
    a.screenshot().save("D:/screenshot/{x}{y}.jpg".format(x=x,y=y))
x = input("name:")
start = int(input("startNo:"))
for i in range(start,start+1000):
    print("{x}{y}.jpg".format(x=x,y=i))
    threading.Thread(target=screen,args=(x,i)).start()
    input("press enter to continue!")