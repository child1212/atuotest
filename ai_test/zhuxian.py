#%%
import torch
import adbutils
import time
import threading
import uiautomator2 as u2
import re
import pathlib
def screen_shot(adb_device,path):
        png_data = adb_device.shell("screencap -p", encoding=None)
        pathlib.Path(path).write_bytes(png_data)

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

def run(deviceid,adb_device,model):
    device = u2.connect(deviceid)
    i = 0
    with open('D:\\record.csv',"w",encoding='utf8') as record:
        record.write("time,package,memory(KB),fps,cpu_useage(%)\n")

    while True:
        cpu_temp = None
        pkg = device.info.get('currentPackageName')
        cpu_info = adb_device.shell('top -n 1 -o %CPU,CMDLINE,PID,USER,CMDLINE|grep {pkg}'.format(pkg=pkg))
        cpu = cpu_info.split('\n')
        cpu_temp = re.search(r'([0-9]+\.?[0-9]?) +com',cpu_info)
        cpu_useage = cpu_temp.group(1)
        memoryinfo = adb_device.shell('dumpsys meminfo {pkg}'.format(pkg=pkg))
        memory = re.search(r'TOTAL PSS: +([0-9]+) ',memoryinfo).group(1)
        fps = get_FPS(adb_device)
        with open('D:\\record.csv',"a",encoding='utf8') as record:
            record.write("{t},{pkg},{memory},{fps},{cpu_useage}\n".format(t=time.strftime("%H:%M:%S", time.localtime()),pkg=pkg,memory=memory,fps=fps,cpu_useage=cpu_useage))
        i += 1
        img = device.screenshot()
        threading.Thread(target=screen_shot,args=(adb_device,'D:\\screenshot\\{device}-{t}.jpg'.format(device=device.info['productName'],t=time.strftime("%H%M%S", time.localtime())))).start()
        results = model(img)
        predictions = results.xywh[0].cpu().numpy()

        position = {}

        for pred in predictions:
            x_center, y_center, width, height, confidence, class_id = pred
            if position.get(int(class_id)):
                position[int(class_id)].append((int(x_center), int(y_center)))
            else:
                position[int(class_id)] = [(int(x_center), int(y_center))]

        if position.get(2):
            for guide in position.get(2):
                device.click(guide[0],guide[1])
                print("guide")
            if position.get(7):
                for ok in position.get(7):
                    device.click(ok[0],ok[1])
                    print('ok')
        elif position.get(7):
            for ok in position.get(7):
                device.click(ok[0],ok[1])
                print('ok')
            if position.get(0):
                for close in position.get(0):
                    device.click(close[0],close[1])
                    print('close')
        elif position.get(3):
            for skip in position.get(3):
                device.click(skip[0],skip[1])
                print('skip')
            if position.get(4):
                for mission in position.get(4):
                    device.click(mission[0],mission[1])
                    print('mission')
        elif position.get(4):
            if position.get(12) and i==5:
                for skill in position.get(12):
                    device.click(skill[0],skill[1])
                    print('skill')
            for mission in position.get(4):
                device.click(mission[0],mission[1])
                print('mission')
        elif position.get(0):
            for close in position.get(0):
                device.click(close[0],close[1])
                print('close')
        elif position.get(8):
            for next in position.get(8):
                device.click(next[0],next[1])
                print('next')
        elif position.get(9):
            for create in position.get(9):
                device.click(create[0],create[1])
                print('next')
        else:
            device.click(0.6,0.6)
            print('blank')
        time.sleep(0.3)
        if i == 5:
            i = 0


adb = adbutils.AdbClient(host="127.0.0.1",port=5037)
devices = adb.device_list()
model = torch.hub.load('D:/gitcode/dev/atuotest/yolov5-master', 'custom', path='D:/gitcode/dev/atuotest/yolov5-master/runs/train/zx/weights/best.pt', source='local')
model.eval()
model.half()
cuda = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(cuda)

for device in devices:
    threading.Thread(target=run,args=(device.serial,adb.device(device.serial),model)).start()



