#%%

from adbutils import adb
import re
import threading

# adb = adbutils.AdbClient(host="127.0.0.1",port=5037)

class DeviceAndroid():
    def __init__(self,deviceId) -> None:
        self.deviceId = deviceId
        self.adb_d = adb.device(deviceId)
        self.max_x = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0035 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.max_y = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0036 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.direction = self.adb_d.rotation()

    def check_direction(self):
        self.direction = self.adb_d.rotation()
        return self.direction
    
    def out_relative_position_x(self,x_p):
        x_i = int(x_p,16)
        return x_i/self.max_x

    def out_relative_position_y(self,y_p):
        y_i = int(y_p,16)
        return y_i/self.max_y
    
    def refrash(self):
        self.max_x = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0035 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.max_y = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0036 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])

    def tap(self,positionx,positiony):
        if self.direction==0:
            print(positionx,positiony)
            self.adb_d.click(positionx,positiony)
        else:
            print(positiony,1-positionx)
            self.adb_d.click(positiony,1-positionx)


    def swipe(self,position_x,position_y,position_x1,position_y1):
        if self.direction == 0:
            self.adb_d.swipe(position_x,position_y,position_x1,position_y1,0.2)
        else:
            self.adb_d.swipe(position_y,1-position_x,position_y1,1-position_x1,0.2)


while True:
    device_list = adb.list()
    devices = adb.device_list()
    #可以手动填写
    MainDeviceId = input("主控设备id:")
    # MainDeviceId = ""#input("主控设备id:")
    if MainDeviceId == "":
        MainDeviceId = devices[0].serial
    print("主控设备id：",MainDeviceId,"\n脚本初始化,请稍候")
    #-------------
    MainDevice = DeviceAndroid(MainDeviceId)
    temp = MainDevice.adb_d.shell("getevent -p")
    print(MainDevice.max_x,MainDevice.max_y)
    devices_set = set()
    for dev in adb.device_list():
        if dev.serial != MainDeviceId:
            d = DeviceAndroid(dev.serial)
            print(d.deviceId,d.adb_d.window_size())
            devices_set.add(d)
        
    stream = MainDevice.adb_d.shell("getevent -l", stream=True)
    running = 0
    distance = 0.05
    with stream:
        f = stream.conn.makefile()
        position = []
        posx_temp = 0
        print("初始化完成，可以开始操作了！")
        while True:
            if device_list != adb.list():
                f.close()
                break
            line = f.readline()
            info_serch = re.search(r'ABS_MT_POSITION_X +[0-9a-f]{8}|ABS_MT_POSITION_Y +[0-9a-f]{8}|BTN_TOUCH +DOWN|BTN_TOUCH +UP',line)
            if info_serch != None:
                search_result = re.split(r' +',info_serch.group(0))
                if search_result[0] == "ABS_MT_POSITION_X":
                    temp_x = MainDevice.out_relative_position_x(search_result[1])
                    if len(position) < 2:
                        position.append([temp_x,0])
                    else:
                        position[1][0] = temp_x

                elif search_result[0] == "ABS_MT_POSITION_Y":
                    temp_y = MainDevice.out_relative_position_y(search_result[1])
                    if len(position) == 0:
                        position.append([temp_x,temp_y])
                    else:
                        position[-1][1] = temp_y


                elif search_result[0] == "BTN_TOUCH":
                    # if search_result[1] == "DOWN":

                    if search_result[1] == "UP":
                        if len(position) == 1:
                            for shouji in devices_set:
                                threading.Thread(target=shouji.tap,args=(position[0][0],position[0][1])).start()
                        elif len(position) == 2:
                            if abs(position[0][0]-position[1][0])>distance or abs(position[0][1]-position[1][1])>distance:
                                for shouji in devices_set:
                                    threading.Thread(target=shouji.swipe,args=(position[0][0],position[0][1],position[1][0],position[1][1])).start()
                            else:
                                for shouji in devices_set:
                                    threading.Thread(target=shouji.tap,args=(position[0][0],position[0][1])).start()
                        position=[]





#%%


























        if running == 0:
            start_signal = re.search(r'BTN_TOUCH +DOWN',line)
            if start_signal != None:
                running = 1
        elif running == 1:
            end_signal = re.search(r'BTN_TOUCH +UP',line)
            if end_signal != None:
                direction = MainDevice.check_direction()
                running = 0
                if len(position)==1:
                    for shouji in devices_set:
                        threading.Thread(target=shouji.tap,args=(position[0][0],position[0][1])).start()
                    position =[]
                elif len(position) == 2:
                    for shouji in devices_set:
                        if abs(position[0][0]-position[1][0])>0.05 or abs(position[0][1]-position[1][1])>0.05:
                            threading.Thread(target=shouji.swipe,args=(position[0][0],position[0][1],position[1][0],position[1][1])).start()
                        else:
                            threading.Thread(target=shouji.tap,args=(position[0][0],position[0][1])).start()
                    position =[]          
            posx_16 = re.search(r'ABS_MT_POSITION_X +[0-9a-f]{8}',line)
            if posx_16!= None:
                posx = int(re.split(r' +',posx_16.group(0))[1],16)
                if len(position) != 2:
                    position.append([posx/MainDevice.max_x,0])
                    posx_temp = position[0][0]
                else:
                    position[1][0] = posx/MainDevice.max_x
            posy_16 = re.search(r'ABS_MT_POSITION_Y +[0-9a-f]{8}',line)
            if posy_16 != None:
                posy = int(re.split(r' +',posy_16.group(0))[1],16)
                if len(position) == 0:
                    position.append([posx_temp,posy/MainDevice.max_y])
                else:
                    position[-1][1] = posy/MainDevice.max_y






























            # resx = res.group(0)
            # sc = re.split(r' +',resx)
            # if sc[1] == "ffffffff":
            #     running = 0
            # else:
            #     running = 1


            # print(sc)
            # print(resx)
    f.close()

