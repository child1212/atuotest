#%%
import adbutils
import threading
import copy
import time
import pathlib

class check_FPS():
    def __init__(self,serial):
        self.adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        self.serial = serial
        self.android = self.adb.device(serial)
        self.version = self.android.shell("getprop ro.build.version.release")
        self.layer = None
        self.FPS = []
        self.old_FPS = 0
        self.model = self.android.shell('getprop ro.product.model')
        self.start_time = int(time.time())
        with open("{model}.csv".format(model=self.model),"w") as f:
            f.write("time,fps,screencap\n")

    def get_layer(self):
        SurfaceInfo = self.android.shell('dumpsys SurfaceFlinger')
        if self.version == "9":
            SurfaceInfo1 = SurfaceInfo[SurfaceInfo.find(" HWC layers"):]
            layerNameBreak = SurfaceInfo1[:SurfaceInfo1.find("h/w composer state:")].split("\n")[5][78:]
        elif self.version == "10":
            SurfaceInfo1 = SurfaceInfo[SurfaceInfo.find(" HWC layers"):]
            layerNameBreak = SurfaceInfo1[:SurfaceInfo1.find("DEVICE")].split("\n")[-2][1:]
        elif self.version == "11":
            SurfaceInfo1 = SurfaceInfo[SurfaceInfo.find(" HWC layers"):]
            layerNameBreak = SurfaceInfo1[:SurfaceInfo1.find("DEVICE")].split("\n")[-2][1:]
        elif self.version == "12":
            layerNameBreak = SurfaceInfo[SurfaceInfo.find(" HWC layers"):SurfaceInfo.find("[*]")].split("\n")[-2][1:]
        elif self.version == "13":
            layerNameBreak = SurfaceInfo[SurfaceInfo.find(" HWC layers"):SurfaceInfo.find("[*]")].split("\n")[-2][1:]
        if "[...]" in layerNameBreak:
            layerNameBreak2 = layerNameBreak.split("[...]")
            layerNameAll = self.android.shell("dumpsys SurfaceFlinger --list").split("\n")
            for line in layerNameAll:
                if layerNameBreak2[0] in line and line.find(layerNameBreak2[0])==0 and layerNameBreak2[1] in line:
                    self.layer = line
        else:
            self.layer = layerNameBreak

    def get_fps(self):
        command1 = self.android.shell('dumpsys SurfaceFlinger --latency "{layerName}"'.format(layerName=self.layer))
        Frames_temp = command1.split("\n")
        if len(Frames_temp) < 80:
            return 0
        time_60 = int((Frames_temp[-5].split("\t"))[1])-int((Frames_temp[-65].split("\t"))[0])
        if time_60 == 0:
            return 1
        time_60 = time_60/1000000000
        fps = 60//time_60
        return fps

    def screen_shot(self,num):
        png_data = self.android.shell("screencap -p", encoding=None)
        pathlib.Path("lowFPS{num}.png".format(num=num)).write_bytes(png_data)
    
    def main(self,run):
        if len(self.FPS) == 10:
            with open("{model}.csv".format(model=self.model),"a") as f:
                for line in self.FPS:
                    f.write(",".join(line))
                    f.write("\n")
                self.FPS = []
        new_fps = self.get_fps()
        now = int(time.time())
        if new_fps < 25 and self.old_FPS >=25:
            t = threading.Thread(target=self.screen_shot,args=(run,))
            t.start()
            print("检测到帧率低于25,截图lowFPS{num}.png,设备：{device_model}".format(num=run,device_model=self.model))
            self.FPS.append([str(now-self.start_time),str(new_fps),"lowFPS{num}.png".format(num=run)])
            run = run+1
        else:
            self.FPS.append([str(now-self.start_time),str(new_fps)])
        self.old_FPS = copy.deepcopy(new_fps)
        return run


if __name__ == "__main__":
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    devices = []
    for i in adb.list():
        if i.state == 'device':
            devices.append(i.serial)
    android_devices =[]
    for serial in devices:
        android_devices.append(check_FPS(serial))
    #初始化layername
    for mobile in android_devices:
        mobile.get_layer()
    run = 0
    while True:
        for command in android_devices:
            # 如果想要兼容多个应用，解封下面行
            # command.get_layer()
            run = command.main(run)











