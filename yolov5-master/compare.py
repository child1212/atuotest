import os

# 数据集路径
image_dir = 'D:\\gitcode\\dev\\atuotest\\yolov5-master\\data\\images\\train'
label_dir = 'D:\\gitcode\\dev\\atuotest\\yolov5-master\\data\\labels\\train'

# 获取图像和标签文件列表
image_files = set(os.listdir(image_dir))
label_files = set(os.listdir(label_dir))

# 过滤掉图像文件后缀
image_files = {f for f in image_files if f.endswith(('.jpg', '.png'))}
label_files = {f for f in label_files if f.endswith('.txt')}

# 确保标签文件与图像文件匹配
image_basename = {os.path.splitext(f)[0] for f in image_files}
label_basename = {os.path.splitext(f)[0] for f in label_files}

# 打印没有标签文件的图像
missing_labels = image_basename - label_basename
if missing_labels:
    print(f"Missing labels for images: {missing_labels}")

# 打印没有图像文件的标签文件
extra_labels = label_basename - image_basename
if extra_labels:
    print(f"Extra label files without corresponding images: {extra_labels}")
