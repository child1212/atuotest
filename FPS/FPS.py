import adbutils
import threading
import copy
import time
import pathlib

class check_FPS():
    def __init__(self):
        self.devices = {}
        self.device_version = {}
        self.device_layer = {}
        self.adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        for info in self.adb.list():
            if info.state == "device":
                self.devices[info.serial] = self.adb.device(info.serial)
                self.device_version[info.serial] = self.devices[info.serial].shell("getprop ro.build.version.release")
            
    def get_layerName(self,adb_device,android_version):
        SurfaceInfo = adb_device.shell('dumpsys SurfaceFlinger')

        if android_version == "9":
            SurfaceInfo1 = SurfaceInfo[SurfaceInfo.find(" HWC layers"):]
            layerNameBreak = SurfaceInfo1[:SurfaceInfo1.find("h/w composer state:")].split("\n")[5][78:]
        else:
            if "[*]" in SurfaceInfo:
                layerNameBreak = SurfaceInfo[SurfaceInfo.find(" HWC layers"):SurfaceInfo.find("[*]")].split("\n")[-2][1:]
            else:
                SurfaceInfo1 = SurfaceInfo[SurfaceInfo.find(" HWC layers"):]
                layerNameBreak = SurfaceInfo1[:SurfaceInfo1.find("DEVICE")].split("\n")[-2][1:]
        if "[...]" in layerNameBreak:
                layerNameBreak2 = layerNameBreak.split("[...]")
                layerNameAll = adb_device.shell("dumpsys SurfaceFlinger --list").split("\n")
                for line in layerNameAll:
                    if layerNameBreak2[0] in line and line.find(layerNameBreak2[0])==0 and layerNameBreak2[1] in line:
                        return line
        else:
            print(layerNameBreak)
            return layerNameBreak

    def get_device_layer(self):
        for device in self.devices.keys():
            self.device_layer[device] = self.get_layerName(self.devices[device],self.device_version[device])

    def get_FPS(self,adb_device,layerName):
        command1 = adb_device.shell('dumpsys SurfaceFlinger --latency "{layerName}"'.format(layerName=layerName))
        Frames_temp = command1.split("\n")
        time_60 = int((Frames_temp[-5].split("\t"))[1])-int((Frames_temp[-65].split("\t"))[0])
        if time_60 == 0:
            return 1
        time_60 = time_60/1000000000
        fps = 60//time_60
        return fps

    def get_device_model(self,adb_device):
        return adb_device.shell('getprop ro.product.model')
    
    def screen_shot(self,adb_device,num):
        png_data = adb_device.shell("screencap -p", encoding=None)
        pathlib.Path("lowFPS{num}.png".format(num=num)).write_bytes(png_data)


    def main(self):
        start_time = int(time.time())
        device_FPS = {}
        device_model = {}
        old_FPS = {}
        for device in self.devices.keys():
            device_model[device] = self.get_device_model(self.devices[device])
            device_FPS[device] = []
            old_FPS[device] = 0
            with open("{device_model}.csv".format(device_model=device_model[device]), "w") as file_init:
                file_init.write("time,fps,screencap\n")
        print(self.device_layer)
        run = 0
        self.get_device_layer()
        while True:
            for device in self.devices.keys():
                if len(device_FPS[device]) == 10:
                    print(device_model[device])
                    print(device_FPS[device])
                    with open("{device_model}.csv".format(device_model=device_model[device]),"a") as f:
                        for line in device_FPS[device]:
                            f.write(",".join(line))
                            f.write("\n")
                    device_FPS[device] = []
                new_fps = self.get_FPS(self.devices[device],self.device_layer[device])
                now = int(time.time())
                if new_fps < 25 and old_FPS[device] >= 25:
                    t = threading.Thread(target=self.screen_shot,args=(self.devices[device],run,))
                    t.start()
                    print("检测到帧率低于25,截图lowFPS{num}.png,设备：{device_model}".format(num=run,device_model=device_model[device]))
                    run += 1
                    device_FPS[device].append([str(now-start_time),str(new_fps),"lowFPS{num}.png".format(num=run)])
                else:
                    device_FPS[device].append([str(now-start_time),str(new_fps)])
                old_FPS[device] = copy.deepcopy(new_fps)


if __name__ == "__main__":
    FPS = check_FPS()
    if FPS.devices =={}:
        input("no devices")
        exit()
    FPS.main()



