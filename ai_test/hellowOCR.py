# %%
import easyocr

reader = easyocr.Reader(['en', 'ch_sim'])  # 支持英语和简体中文

# 识别图像中的文本
result = reader.readtext('D:/gitcode/dev/atuotest/yolov5-master/data/images/train/img234.jpg')

for detection in result:
    print(detection[1])  # 打印识别到的文本






# %%



