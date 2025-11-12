import adbutils

def get_FPS(adb_device):
    android_version = adb_device.shell("getprop ro.build.version.release")
    SurfaceInfo = adb_device.shell('dumpsys SurfaceFlinger')

    if android_version == "9":
        SurfaceInfo1 = SurfaceInfo[SurfaceInfo.find(" HWC layers"):]
        layerName = SurfaceInfo1[:SurfaceInfo1.find("h/w composer state:")].split("\n")[5][78:]
    else:
        if "[*]" in SurfaceInfo:
            layerName = SurfaceInfo[SurfaceInfo.find(" HWC layers"):SurfaceInfo.find("[*]")].split("\n")[-2][1:]
        else:
            SurfaceInfo1 = SurfaceInfo[SurfaceInfo.find(" HWC layers"):]
            layerName = SurfaceInfo1[:SurfaceInfo1.find("DEVICE")].split("\n")[-2][1:]
    if "[...]" in layerName:
            layerNameBreak2 = layerName.split("[...]")
            layerNameAll = adb_device.shell("dumpsys SurfaceFlinger --list").split("\n")
            for line in layerNameAll:
                if layerNameBreak2[0] in line and line.find(layerNameBreak2[0])==0 and layerNameBreak2[1] in line:
                    layerName = line
    command1 = adb_device.shell('dumpsys SurfaceFlinger --latency "{layerName}"'.format(layerName=layerName))
    Frames_temp = command1.split("\n")
    time_60 = int((Frames_temp[-5].split("\t"))[1])-int((Frames_temp[-65].split("\t"))[0])
    if time_60 == 0:
        return 1
    time_60 = time_60/1000000000
    fps = 60//time_60
    return fps

if __name__ == "__main__":
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    device = adb.device()
    print(get_FPS(device))