#%%
import torch
import cv2
import matplotlib.pyplot as plt
from pathlib import Path

# 加载训练好的 YOLOv5 模型（可以是yolov5s，yolov5m等）
model = torch.hub.load('D:/gitcode/dev/atuotest/yolov5-master', 'custom', path='D:/gitcode/dev/atuotest/yolov5-master/runs/train/exp/weights/first.pt', source='local')

# 使用OpenCV读取图像
image = cv2.imread('D:/gitcode/dev/atuotest/yolov5-master/data/images/train/img306.jpg')

# 转换BGR图像为RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 显示图像
plt.imshow(image)
plt.show()

# 对图像进行推理
results = model(image_rgb)

results.show()  # 可视化推理结果

predictions = results.xywh[0].cpu().numpy()
#逐个获取识别信息
for pred in predictions:
    x_center, y_center, width, height, confidence, class_id = pred
    # print(f"Class ID: {class_id}, Confidence: {confidence}")
    # print(f"Bounding Box: x_center={x_center}, y_center={y_center}, width={width}, height={height}")
# %%
