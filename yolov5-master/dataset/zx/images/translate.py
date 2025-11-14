import os
import xml.etree.ElementTree as ET
import cv2

def convert_annotation(xml_file, class_dict, img_width, img_height):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    yolo_format = []
    
    for obj in root.iter('object'):
        class_name = obj.find('name').text
        class_id = class_dict.get(class_name, -1)
        
        if class_id == -1:
            continue
        
        # 解析边界框
        xml_bndbox = obj.find('bndbox')
        xmin = int(xml_bndbox.find('xmin').text)
        ymin = int(xml_bndbox.find('ymin').text)
        xmax = int(xml_bndbox.find('xmax').text)
        ymax = int(xml_bndbox.find('ymax').text)

        # 计算中心坐标、宽度和高度
        x_center = (xmin + xmax) / 2.0 / img_width
        y_center = (ymin + ymax) / 2.0 / img_height
        width = (xmax - xmin) / float(img_width)
        height = (ymax - ymin) / float(img_height)
        
        yolo_format.append(f"{class_id} {x_center} {y_center} {width} {height}")
    
    return yolo_format

# 示例：用来转换整个文件夹的标注文件
def convert_voc_to_yolo(xml_dir, img_dir, class_dict):
    for xml_file in os.listdir(xml_dir):
        if not xml_file.endswith('.xml'):
            continue
        
        # 获取图像大小
        img_path = os.path.join(img_dir, xml_file.replace('.xml', '.jpg'))
        img = cv2.imread(img_path)
        img_height, img_width, _ = img.shape
        
        yolo_data = convert_annotation(os.path.join(xml_dir, xml_file), class_dict, img_width, img_height)
        
        # 保存为 YOLO 格式的 txt 文件
        yolo_txt_file = os.path.join(xml_dir, xml_file.replace('.xml', '.txt'))
        with open(yolo_txt_file, 'w') as f:
            for line in yolo_data:
                f.write(line + '\n')

# 定义类别字典（根据你的数据集）
class_dict = {'closeButton': 0, 'backButton': 1, 'guideButton':2,'skipButton':3,'mission':4,'useButton':5,'login':6}  # 更新为你的类别

# 转换目录
xml_dir = 'D:\\screenshot'
img_dir = 'D:\\screenshot'

convert_voc_to_yolo(xml_dir, img_dir, class_dict)