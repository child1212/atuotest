from adbutils import adb
import threading
from time import sleep
import uiautomator2 as u2





print(adb.device_list)
# a = adb.device(adb.device_list()[0].serial)
a = u2.connect()
def screen(x,y):
    # a.screenshot().save("D:/screenshot/{x}{y}.jpg".format(x=x,y=y))
    a.screenshot("D:/screenshot/{x}{y}.jpg".format(x=x,y=y))
x = input("name:")
start = int(input("startNo:"))
for i in range(start,start+10000):
    print("{x}{y}.jpg".format(x=x,y=i))
    screen(x,i)
    # threading.Thread(target=screen,args=(x,i)).start()
    # sleep(0.3)
    # input("press enter to continue!")