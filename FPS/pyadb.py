#%%
#说明：https://github.com/openatx/adbutils
import adbutils

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
devices = []
for info in adb.list():
    # print(info.serial, info.state)
    devices.append(info.serial)
d = adb.device(devices[0])

d.shell("getprop ro.build.version.release")


SurfaceInfo = d.shell('dumpsys SurfaceFlinger')
print(SurfaceInfo)
#%%
# if android_version == 9:
SurfaceInfo1 = SurfaceInfo[SurfaceInfo.find(" HWC layers"):]
layerNameBreak = SurfaceInfo1[:SurfaceInfo1.find("h/w composer state:")].split("\n")[5][78:]


# if "[*]" in SurfaceInfo:
#     layerNameBreak = SurfaceInfo[SurfaceInfo.find(" HWC layers"):SurfaceInfo.find("[*]")].split("\n")[-2][1:]
# else:
#     SurfaceInfo1 = SurfaceInfo[SurfaceInfo.find(" HWC layers"):]
#     layerNameBreak = SurfaceInfo1[:SurfaceInfo1.find("DEVICE")].split("\n")#[-2][1:]
if "[...]" in layerNameBreak:
        layerNameBreak2 = layerNameBreak.split("[...]")
        layerNameAll = d.shell("dumpsys SurfaceFlinger --list").split("\n")
        for line in layerNameAll:
            if layerNameBreak2[0] in line and layerNameBreak2[1] in line:
                layerName = line
else:
    layerName = layerNameBreak


command1 = d.shell('dumpsys SurfaceFlinger --latency "{layerName}"'.format(layerName=layerName))

Frames_temp = command1.split("\n")

time_60 = int((Frames_temp[-5].split("\t"))[1])-int((Frames_temp[-65].split("\t"))[0])
while time_60 > 1000:
    time_60 = time_60//1000

FPS = 60//time_60
print(FPS)
     





# print(command1)




#%%































# %%
