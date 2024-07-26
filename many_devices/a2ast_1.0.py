#%%

from adbutils import adb
import re
import threading
from multiprocessing import Process

# adb = adbutils.AdbClient(host="127.0.0.1",port=5037)

class DeviceAndroid():
    def __init__(self,deviceId) -> None:
        self.deviceId = deviceId
        self.coefficient = 1000
        self.adb_d = adb.device(deviceId)
        self._size = self.adb_d.window_size()
        self.max_x = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0035 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.max_y = int(re.split(r' +',re.search(r'max +[0-9]+',re.findall(r' +0036 +: value +[0-9]+, +min +[0-9]+, +max +[0-9]+',self.adb_d.shell("getevent -p"))[-1]).group(0))[1])
        self.direction = re.split(r'=',re.search(r'orientation=[0-4]',self.adb_d.shell("dumpsys input|grep orientation=")).group(0))[1]
        self.size_x = min(self._size) if self.direction=="0" else max(self._size)
        self.size_y = max(self._size) if self.direction=="0" else min(self._size)

    def out_relative_position_x(self,x_p):
        x_i = int(x_p,16)
        return x_i*self.coefficient//self.max_x

    def out_relative_position_y(self,y_p):
        y_i = int(y_p,16)
        return y_i*self.coefficient//self.max_y
    
    def touch_relative_position(self,relative_x,relative_y,action=0):
        '''
        action==1:down
        action==2:up
        '''
        if self.direction == "0":
            pos_x = relative_x*self.size_x//self.coefficient
            pos_y = relative_y*self.size_y//self.coefficient
        else:
            pos_x = relative_y*self.size_x//self.coefficient
            pos_y = self.size_y-relative_x*self.size_y//self.coefficient
        if action==0:
            self.adb_d.shell("input motionevent MOVE {pos_x} {pos_y}".format(pos_x=pos_x,pos_y=pos_y))
        elif action == 1:
            print( "DOWN {pos_x} {pos_y}".format(pos_x=pos_x,pos_y=pos_y))
            self.adb_d.shell("input motionevent DOWN {pos_x} {pos_y}".format(pos_x=pos_x,pos_y=pos_y))
            self.adb_d.shell("input motionevent MOVE {pos_x} {pos_y}".format(pos_x=pos_x,pos_y=pos_y))
        elif action == 2:
            self.adb_d.shell("input motionevent MOVE {pos_x} {pos_y}".format(pos_x=pos_x,pos_y=pos_y))
            self.adb_d.shell("input motionevent UP {pos_x} {pos_y}".format(pos_x=pos_x,pos_y=pos_y))
            print( "UP {pos_x} {pos_y}".format(pos_x=pos_x,pos_y=pos_y))

def do_action(devices_list,position,action):
    for shouji in devices_list:
        threading.Thread(target=shouji.touch_relative_position,args=(position[0],position[1],action)).start()


while True:
    device_list = adb.list()
    devices = adb.device_list()
    #可以手动填写
    MainDeviceId = input("主控设备id:")
    # MainDeviceId = "A4RY023A17003122"#input("主控设备id:")
    if MainDeviceId == "":
        MainDeviceId = devices[0].serial
    print("主控设备id： ",MainDeviceId,"\n脚本正在初始化,请稍候！")
    #-------------
    MainDevice = DeviceAndroid(MainDeviceId)
    temp = MainDevice.adb_d.shell("getevent -p")
    print("主控设备分辨率：",MainDevice.size_x,MainDevice.size_y)
    devices_list = []
    for dev in adb.device_list():
        if dev.serial != MainDeviceId:
            d = DeviceAndroid(dev.serial)
            print(d.deviceId,":",d.size_x,d.size_y)
            devices_list.append(d)

    stream = MainDevice.adb_d.shell("getevent -l | grep -E 'ABS_MT_POSITION|BTN_TOUCH'", stream=True)
    running = 0
    action = 1
    run = 0
    distance_x = MainDevice.coefficient//40
    # distance_y = MainDevice.size_y//80
    with stream:
        f = stream.conn.makefile()
        # while True: 
        position = [0,0]
        posx_temp = 0
        print("初始化完成，可以开始操作了！")
        # for i in range(10000):# read 100 lines
        while True:
            if device_list != adb.list():
                f.close()
                break
            line = f.readline()
            info_serch = re.search(r'ABS_MT_POSITION_X +[0-9a-f]{8}|ABS_MT_POSITION_Y +[0-9a-f]{8}|BTN_TOUCH +DOWN|BTN_TOUCH +UP',line)
            if info_serch != None:
                # print(info_serch.group(0))
                search_result = re.split(r' +',info_serch.group(0))
                if search_result[0] == "ABS_MT_POSITION_X":
                    temp_x = MainDevice.out_relative_position_x(search_result[1])
                    if abs(temp_x-position[0])>distance_x or position[0]==0:
                        position[0] = temp_x
                        run += 1
                elif search_result[0] == "ABS_MT_POSITION_Y":
                    temp_y = MainDevice.out_relative_position_y(search_result[1])
                    if abs(temp_y-position[1])>distance_x or position[1]==0:
                        position[1] = temp_y

                        
                        run += 1

                elif search_result[0] == "BTN_TOUCH":
                    if search_result[1] == "DOWN":
                        run = 0
                        action = 1
                    elif search_result[1] == "UP":
                        threading.Thread(target=do_action,args=(devices_list,position,2)).start()
                        # for shouji in devices_list:
                            # threading.Thread(target=shouji.touch_relative_position,args=(position[0],position[1],2)).start()
                        position = [0,0]
                if run == 2 :
                    threading.Thread(target=do_action,args=(devices_list,position,action)).start()
                    # for shouji in devices_list:
                    #     threading.Thread(target=shouji.touch_relative_position,args=(position[0],position[1],action)).start()
                    action = 0
                    run=0
    



















































































# %%
