#%%

from adbutils import adb
import re
import threading
#  962 1758
# adb = adbutils.AdbClient(host="127.0.0.1",port=5037)

class DeviceAndroid():
    def __init__(self,deviceId) -> None:
        self.deviceId = deviceId
        self.adb_d = adb.device(deviceId)
        self.max_x = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0035 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.max_y = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0036 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.size_x = int(re.findall(r'[1-9][0-9]+',re.search(r'cur=[1-9][0-9]+x[1-9][0-9]+',self.adb_d.shell("dumpsys window displays")).group(0))[0])
        self.size_y = int(re.findall(r'[1-9][0-9]+',re.search(r'cur=[1-9][0-9]+x[1-9][0-9]+',self.adb_d.shell("dumpsys window displays")).group(0))[1])
        self.direction = re.split(r'=',re.search(r'orientation=[0-4]',self.adb_d.shell("dumpsys input|grep orientation=")).group(0))[1]

    def check_direction(self):
        self.direction = re.split(r'=',re.search(r'orientation=[0-4]',self.adb_d.shell("dumpsys input|grep orientation=")).group(0))[1]
        return self.direction
    
    def refrash(self):
        self.max_x = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0035 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.max_y = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0036 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.size_x = int(re.findall(r'[1-9][0-9]+',re.search(r'cur=[1-9][0-9]+x[1-9][0-9]+',self.adb_d.shell("dumpsys window displays")).group(0))[0])
        self.size_y = int(re.findall(r'[1-9][0-9]+',re.search(r'cur=[1-9][0-9]+x[1-9][0-9]+',self.adb_d.shell("dumpsys window displays")).group(0))[1])

    def tap(self,position_x,position_y,direction):
        if direction == "0":
            print("input tap {x} {y}".format(x=position_x*self.size_x//100000,y=position_y*self.size_y//100000))        
        else:
            print("input tap {x} {y}".format(x=position_y*self.size_x//100000,y=self.size_y-position_x*self.size_y//100000))

    def swipe(self,position_x,position_y,position_x1,position_y1,direction):
        if direction == "0":
            print("input swipe {a} {b} {c} {d} ".format(a=position_x*self.size_x//100000,b=position_y*self.size_y//100000,c=position_x1*self.size_x//100000,d=position_y1*self.size_y//100000))
        else:
            print("input swipe {a} {b} {c} {d} ".format(a=position_y*self.size_x//100000,b=self.size_y-position_x*self.size_y//100000,c=position_y1*self.size_x//100000,d=self.size_y-position_x1*self.size_y//100000))

    def install(self,path):
        self.adb_d.install(path)
    
devices = adb.device_list()
#可以手动填写
MainDeviceId = input("主控设备id:")
if MainDeviceId == "":
    MainDeviceId = devices[0].serial
print("主控设备id：",MainDeviceId,"\n脚本初始化,请稍候")
#-------------

MainDevice = DeviceAndroid(MainDeviceId)
temp = MainDevice.adb_d.shell("getevent -p")
print(MainDevice.max_x,MainDevice.max_y)

    
stream = MainDevice.adb_d.shell("getevent -l", stream=True)
running = 0
with stream:
    f = stream.conn.makefile()
    # while True: 
    position = []
    posx_temp = 0
    print("初始化完成，可以开始操作了！")
    # for i in range(1000):# read 100 lines
    while True:

        line = f.readline()
        # print(line)

        if running == 0:
            start_signal = re.search(r'ABS_MT_TRACKING_ID',line)
            # start_signal = re.search(r'BTN_TOUCH +DOWN',line)
            if start_signal != None:
                running = 1
                position =[]
        elif running == 1:
            end_signal = re.search(r'BTN_TOUCH +UP',line)
            if end_signal != None:
                direction = MainDevice.check_direction()
                running = 0
                if len(position)==1:
                    MainDevice.tap(position[0][0],position[0][1],direction)
                elif len(position) == 2:
                    MainDevice.swipe(position[0][0],position[0][1],position[1][0],position[1][1],direction)
            posx_16 = re.search(r'ABS_MT_POSITION_X +[0-9a-f]{8}',line)
            if posx_16!= None:
                posx = int(re.split(r' +',posx_16.group(0))[1],16)
                if len(position) != 2:
                    position.append([posx*100000//MainDevice.max_x,0])
                    posx_temp = position[0][0]
                else:
                    position[1][0] = posx*100000//MainDevice.max_x
            posy_16 = re.search(r'ABS_MT_POSITION_Y +[0-9a-f]{8}',line)
            if posy_16 != None:
                posy = int(re.split(r' +',posy_16.group(0))[1],16)
                if len(position) == 0:
                    position.append([posx_temp,posy*100000//MainDevice.max_y])
                else:
                    position[-1][1] = posy*100000//MainDevice.max_y






























            # resx = res.group(0)
            # sc = re.split(r' +',resx)
            # if sc[1] == "ffffffff":
            #     running = 0
            # else:
            #     running = 1


            # print(sc)
            # print(resx)
    f.close()

