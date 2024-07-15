#%%

import adbutils
import re
adb = adbutils.AdbClient(host="127.0.0.1",port=5037)

class DeviceAndroid():
    def __init__(self,deviceId) -> None:
        self.deviceId = deviceId
        self.adbdevice = adb.device(deviceId)
        self.max_x = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0035 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adbdevice.shell("getevent -p"))[-1]).group(0))[1])
        self.max_y = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0036 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adbdevice.shell("getevent -p"))[-1]).group(0))[1])
        # display = self.adbdevice.shell("dumpsys window displays")
        # cur = re.search(r'cur=[1-9][0-9]+x[1-9][0-9]+',display).group(0)
        # cursize = re.findall(r'[1-9][0-9]+',cur)
        self.size_x = int(re.findall(r'[1-9][0-9]+',re.search(r'cur=[1-9][0-9]+x[1-9][0-9]+',self.adbdevice.shell("dumpsys window displays")).group(0))[0])
        self.size_y = int(re.findall(r'[1-9][0-9]+',re.search(r'cur=[1-9][0-9]+x[1-9][0-9]+',self.adbdevice.shell("dumpsys window displays")).group(0))[1])
        self.direction = re.split(r'=',re.search(r'orientation=[0-4]',self.adbdevice.shell("dumpsys input|grep orientation=")).group(0))[1]

    def check_direction(self):
        self.direction = re.split(r'=',re.search(r'orientation=[0-4]',self.adbdevice.shell("dumpsys input|grep orientation=")).group(0))[1]
        return self.direction



    
devices = adb.device_list()
#可以手动填写
xiaomidev = devices[0].serial
# xiaomidev = "2f20296"
print(xiaomidev)
#-------------

xiaomi = DeviceAndroid(xiaomidev)
temp = xiaomi.adbdevice.shell("getevent -p")
adbDevices = set()
for dev in adb.device_list():
    if dev.serial != xiaomidev:
        adbDevices.add(DeviceAndroid(dev.serial))
    
stream = xiaomi.adbdevice.shell("getevent -l", stream=True)
running = 0
with stream:
    f = stream.conn.makefile()
    # while True: 
    position = []
    posx_temp = 0
    for i in range(1000):# read 100 lines

        line = f.readline()
        # print(line)

        if running == 0:
            start_signal = re.search(r'BTN_TOOL_FINGER +DOWN',line)
            if start_signal != None:
                running = 1
                position =[]
        elif running == 1:
            end_signal = re.search(r'BTN_TOOL_FINGER +UP',line)
            if end_signal != None:
                direction = xiaomi.check_direction()
                running = 0
                if len(position)==1:
                    for shouji in adbDevices:
                        if direction == "0":
                            # print(shouji.deviceId,shouji.size_x,shouji.size_y)
                            # print("input tap {x} {y}".format(x=position[0][0]*shouji.size_x//100000,y=position[0][1]*shouji.size_y//100000))
                            shouji.adbdevice.shell("input tap {x} {y}".format(x=position[0][0]*shouji.size_x//100000,y=position[0][1]*shouji.size_y//100000))
                        else:
                            shouji.adbdevice.shell("input tap {y} {x}".format(y=position[0][1]*shouji.size_y//100000,x=shouji.size_x-position[0][0]*shouji.size_x//100000))
                elif len(position) == 2:
                    for shouji in adbDevices:
                        if direction == "0":
                            # print(shouji.deviceId,shouji.size_x,shouji.size_y)
                            # print("input swipe {a} {b} {c} {d} ".format(a=position[0][0]*shouji.size_x//100000,b=position[0][1]*shouji.size_y//100000,c=position[1][0]*shouji.size_x//100000,d=position[1][1]*shouji.size_y//100000))
                            shouji.adbdevice.shell("input swipe {a} {b} {c} {d} ".format(a=position[0][0]*shouji.size_x//100000,b=position[0][1]*shouji.size_y//100000,c=position[1][0]*shouji.size_x//100000,d=position[1][1]*shouji.size_y//100000))
                        else:
                            shouji.adbdevice.shell("input swipe {b} {a} {d} {c} ".format(a=shouji.size_x-position[0][0]*shouji.size_x//100000,b=position[0][1]*shouji.size_y//100000,c=shouji.size_x-position[1][0]*shouji.size_x//100000,d=position[1][1]*shouji.size_y//100000))
            posx_16 = re.search(r'ABS_MT_POSITION_X +[0-9a-f]{8}',line)
            if posx_16!= None:
                posx = int(re.split(r' +',posx_16.group(0))[1],16)
                if len(position) != 2:
                    position.append([posx*100000//xiaomi.max_x,0])
                    posx_temp = position[0][0]
                else:
                    position[1][0] = posx*100000//xiaomi.max_x
            posy_16 = re.search(r'ABS_MT_POSITION_Y +[0-9a-f]{8}',line)
            if posy_16 != None:
                posy = int(re.split(r' +',posy_16.group(0))[1],16)
                if len(position) == 0:
                    position.append([posx_temp,posy*100000//xiaomi.max_y])
                else:
                    position[-1][1] = posy*100000//xiaomi.max_y






























            # resx = res.group(0)
            # sc = re.split(r' +',resx)
            # if sc[1] == "ffffffff":
            #     running = 0
            # else:
            #     running = 1


            # print(sc)
            # print(resx)
    f.close()

