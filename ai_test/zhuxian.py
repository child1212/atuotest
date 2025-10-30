#%%
import torch
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import adbutils

adb = adbutils.AdbClient(host="127.0.0.1",port=5037)
device = adb.device()
# device = adb(devices[0].serial)

img = device.screenshot()


model = torch.hub.load('D:/gitcode/dev/atuotest/yolov5-master', 'custom', path='D:/gitcode/dev/atuotest/yolov5-master/runs/train/exp/weights/best.pt', source='local')

# image = cv2.imread('D:/gitcode/dev/atuotest/yolov5-master/data/images/train/img306.jpg')

# image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# plt.imshow(img)
# plt.show()

results = model(img)

results.show()  # 可视化推理结果

predictions = results.xywh[0].cpu().numpy()

position = {}

# for pred in predictions:
#     x_center, y_center, width, height, confidence, class_id = pred
#     if position.get(int(class_id)):
#         position[int(class_id)].append((int(x_center), int(y_center)))
#     else:
#         position[int(class_id)] = [(int(x_center), int(y_center))]
# print(position)

# if position.get(2):
#     for pos in position.get(2):
#         device.click(pos[0],pos[1])
# elif position.get(4):
#     if position.get(12):
#         for pos in position.get(12):
#             device.click(pos[0],pos[1])
#     for pos in position.get(4):
#         device.click(pos[0],pos[1])
#%%
import torch
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import adbutils
import time
adb = adbutils.AdbClient(host="127.0.0.1",port=5037)
device = adb.device()
# device = adb(devices[0].serial)
model = torch.hub.load('D:/gitcode/dev/atuotest/yolov5-master', 'custom', path='D:/gitcode/dev/atuotest/yolov5-master/runs/train/exp/weights/best.pt', source='local')
model.eval()
model.half()
cuda = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(cuda)
i = 0
while True:
    i += 1
    # print(i)
    img = device.screenshot()

    # image = cv2.imread('D:/gitcode/dev/atuotest/yolov5-master/data/images/train/img306.jpg')

    # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # plt.imshow(img)
    # plt.show()

    results = model(img,size=320)

    # results.show()  # 可视化推理结果

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
    else:
        device.click(0.5,0.7)
        print('blank')
    time.sleep(0.3)
    if i == 5:
        i = 0

