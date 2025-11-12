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


model = torch.hub.load('D:/gitcode/dev/atuotest/yolov5-master', 'custom', path='D:/gitcode/dev/atuotest/yolov5-master/runs/train/zx/weights/best.pt', source='local')

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


# %%
import scrcpy
import cv2

client = scrcpy.Client()

def on_frame(frame):
    # 使用 OpenCV 将图像显示出来
    cv2.imshow("Screen", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        client.stop()

client.add_listener(scrcpy.EVENT_FRAME, on_frame)        

client.start()