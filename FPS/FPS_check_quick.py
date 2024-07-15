#%%
import subprocess
import time
import copy
import os
import threading
def get_device_model(device):
    a = subprocess.check_output("adb -s {device} shell getprop ro.product.model".format(device=device))
    b = a.decode()
    return b.replace("\r\n", "")

def get_devices():
    a = subprocess.check_output("adb devices")
    b = a.decode().replace("\r\n",",").replace("\tdevice","").split(",")[1:-2]
    return b


def get_top_layer(device):
    a = subprocess.check_output("adb -s {device} shell dumpsys SurfaceFlinger".format(device=device))
    b = a.decode()[a.decode().find(" HWC layers"):a.decode().find("[*]")+3].replace(" ","").split("\r\n")[-2]
    if "[...]" in b:
        c = b.split("[...]")
        d = subprocess.check_output("adb -s {device} shell dumpsys SurfaceFlinger --list".format(device=device))
        e = d.decode().replace(" ","").split("\r\n")
        for line in e:
            if c[0] in line and c[1] in line:
                return line
    return b

def get_FPS(device,top_layer):
    # top_layer = get_top_layer(device).replace("(","\\(").replace(")","\\)")
    print(top_layer)
    a = subprocess.check_output("adb -s {device} shell dumpsys SurfaceFlinger --latency {top} ".format(device=device,top=top_layer))
    b = a.decode().split("\r\n")
    if len(b) < 10:
        return 0
    c = b[-65:-5]
    d = c[0].split("\t")
    e = c[-1].split("\t")
    f = int(60*1000000000/((int(e[1])-int(d[1]))))
    return f

def screen_shot(device,num):
    os.system("adb -s {device} exec-out screencap -p > lowFPS{num}.jpg".format(device=device,num=num))


def main():
    start_time = int(time.time())
    devices = get_devices()
    device_model = {}
    device_FPS = {}
    device_top_layer = {}
    old_FPS = {}
    file_name = open("device.txt", "w")
    for device in devices:
        device_model[device] = get_device_model(device)
        device_FPS[device] = []
        old_FPS[device] = 0
        device_top_layer[device] = get_top_layer(device).replace("(","\\(").replace(")","\\)")
        file_name.write("{device_model}.csv\n".format(device_model=device_model[device]))
        with open("{device_model}.csv".format(device_model=device_model[device]), "w") as f:
            f.write("time,FPS")
    file_name.close()
    run = 0  
    while True:
        for device in devices:
            if len(device_FPS[device]) == 10:
                with open("{device_model}.csv".format(device_model=device_model[device]), "a") as f:
                    print("{device_model}.csv".format(device_model=device_model[device]))
                    for line in device_FPS[device]:
                        f.write(",".join(line))
                        f.write("\n")
                device_FPS[device] = []
            FPS = get_FPS(device,device_top_layer[device])
            if old_FPS[device]>=25 and FPS <25:
                t = threading.Thread(target=screen_shot,args=(device,run,))
                t.start()
                print("检测到帧率低于25,截图lowFPS{num}.jpg,设备：{device_model}".format(num=run,device_model=device_model[device]))
                run += 1
            now = int(time.time())
            # timeArray = time.localtime(now)
            # otherStyleTime = time.strftime("%H:%M:%S", timeArray)
            old_FPS[device] = copy.deepcopy(FPS)
            device_FPS[device].append([str(now-start_time),str(FPS)])
#%%    
if __name__ == "__main__":
    main()
   
        






#%%
a = subprocess.check_output('adb shell dumpsys SurfaceFlinger --list "| grep SurfaceView" ')    




# %%
d = subprocess.check_output("adb -d shell dumpsys SurfaceFlinger --list")

e = d.decode().split("\r\n")


for top_layer in e:
    x = subprocess.check_output("adb shell dumpsys SurfaceFlinger --latency {top} ".format(top=top_layer.replace("(","\\(").replace(")","\\)")))

    y = x.decode().split("\r\n")
    if len(y) > 10:
        print(y[-5])
    print(top_layer)



# %%
