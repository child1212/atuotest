#%%
import os,csv
import time
import numpy as np
from matplotlib import pyplot as plt
from subprocess import Popen, PIPE
# from check_package import check_package
import math

fps_list=[]
time_list=[]
adress='app'
# package_name,activity=check_package(adress)
package_name,activity="com.games.fairyadventure","com.fotoable.dragon.MyUnityPlayerActivity"

# 写入表头
def write_head():
    headers = []
    headers.append('time')
    headers.append('init_fps')
    with open('files/fpsinfo.csv','w+',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=headers)
        writer.writeheader()

def dump_layer_stats(str_command):
    L = []
    p = Popen(str_command, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    for line in p.stdout:
        if line != '\n':
            ldata1 =(line[:-1].split('\t'))
            ldata=[]
            for i in ldata1:
                ldata.append(int(i))
            if len(ldata)== 1:
                pass
            else:
                if (ldata[1]) >= 9223372036854775807:
                    continue
                elif (ldata[1]) == 0:
                    continue
                L.append((ldata[1]))
                #    p.terminate()
    return L

def get_fps():
   while True:
        str_command = 'adb shell dumpsys SurfaceFlinger --latency  {}/{}#0'.format(package_name,activity)
        # print(str_command)
        end_time = time.time()
        if (end_time-start_time)/60>=total_time:
            break
        L =dump_layer_stats(str_command)
        size = len(L)
        interval = 0
        now = time.strftime('%H:%M:%S',time.localtime())
        time_list.append(now)
        if size > 0:
            interval = L[size - 1] - L[0]
        else:
            # 获取不到返回异常
            return -1
        if interval == 0:
            continue
        fps = 1000000000 * (size - 1) / interval
        fps_list.append(round(fps,2))


        
# 将数据写入csv
def write_report():
    with open('fpsinfo.csv','a+',newline='') as f:
        writer = csv.writer(f)
        for i in range(0,len(fps_list)):
            writer.writerow([time_list[i],fps_list[i]])
        print('数据插入成功')

# 绘制折线图
def mapping():
    hights = fps_list
    # 将cpu值转换为浮点类型数据
    hights_float = list(map(float,hights))
    wights = time_list
    total=0
    for hight in hights_float:
        total+=hight
    ave = round(total/len(hights_float),2)
    # 计算cpu最高值和最低值
    sort_hights_float = sorted(hights_float)
    min_hight = round(sort_hights_float[0],2)
    max_hight = round(sort_hights_float[-1],2)
    print('最大值为：%.2f，最小值为%.2f，平均值为%.2f'%(max_hight,min_hight,ave))
    # 根据数据绘制图形
    # 创建自定义图像
    plt.figure(figsize=(11,4),dpi=600)
    # 生成网格,只展示y轴
    plt.grid(axis='y')
    # 绘制折线图
    plt.plot(wights,hights_float,'c-',linewidth=1,label=app_name)
    # 设置坐标轴范围
    plt.xlabel('time(H:Min:S)',fontsize=16)
    plt.ylabel('fps_realtime(%)',fontsize=16)
    plt.title('{} fps'.format(app_name),fontsize=24)
    # 显示label
    plt.legend()
    # 横坐标显示间隔
    # 进行时间列表去重
    wights = list(set(wights))
    if len(wights)<=15:
        pass
    else:
        t = int(len(wights)/15)
        # 显示x轴的刻标，以时间间隔t展示
        plt.xticks(range(0,len(wights),t))
    # 旋转横坐标日期
    plt.gcf().autofmt_xdate()
    time_now = time.strftime('%H:%M:%S',time.localtime())
    save_path = 'pictures/'+'{}_fps_occupation_'.format(app_name)+ time_now
    plt.savefig(save_path)


if __name__ == '__main__':
    total_time = math.ceil(float(input('请输入脚本执行时间(分钟):')))
    start_time = time.time()
    app_name = input('请输入app名称:')
    get_fps()
    write_report()
    # mapping()
# %%
