import os
import json
import cv2

# 数据集路径
image_dir = 'D:\\P5X_train'

# 获取图像和标签文件列表
image_files = set(os.listdir(image_dir))

# 过滤掉图像文件后缀
# image_files = {f for f in image_files if f.endswith(('.jpg', '.png'))}
path_list = "D:\\gitcode\\dev\\atuotest\\ai_test\\img_list.txt"
path_json = "D:\\gitcode\\dev\\atuotest\\ai_test\\record.json"
with open(path_list,'r') as il:
    img_list = json.load(il)

while len(img_list) > 0:
    if len(img_list) % 100 == 0:
        print("---------------",len(img_list))
    img_name = img_list.pop()
    image = cv2.imread(image_dir+'\\'+img_name)

    scale_percent = 50  # 百分比
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow(img_name,resized)
    cv2.waitKey(0)
    action = input('action:')
    if action == '':
        action='blank'
    # button = input('button:')
    cv2.destroyAllWindows()
    mo = {
        "image" : img_name,
        "action" : action
        # {
        #     "type":action,
        #     # "button":button
        # }
    }
    with open(path_json,'r') as record:
       data = json.load(record)
    data.append(mo)
    with open(path_json,'w') as record:
        json.dump(data,record)
    with open(path_list,'w') as il:
        json.dump(img_list,il)

