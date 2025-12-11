import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import uiautomator2 as u2
from io import BytesIO
import cv2
import numpy as np

# ================================================
#  模型结构（必须和训练时一致）
# ================================================
class ActionCloneModel(nn.Module):
    def __init__(self, num_actions):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Flatten()
        )

        self.fc = nn.Sequential(
            nn.Linear(64 * 28 * 28, 256),
            nn.ReLU(),
            nn.Linear(256, num_actions)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.fc(x)
        return x


# ================================================
#  推理模型加载
# ================================================
def load_model(model_path, num_actions):
    model = ActionCloneModel(num_actions)
    state_dict = torch.load(model_path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model


# ================================================
#  动作反向映射（必须与训练一致）
# ================================================
action_map = {'blank':0,'up':1,'left':2,'right':3,'guide':4,'jump':5,'attack':6,'sumbit':7,'cancel':8,'close':9,'action':10,'chiose':11,'start':12,'direction':13}
inv_action_map = {v: k for k, v in action_map.items()}


# ================================================
#  图像预处理（与训练一致）
# ================================================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


# ================================================
#  推理函数
# ================================================
# def infer(model, image_path):
#     img = Image.open(image_path).convert("RGB")
#     img_tensor = transform(img).unsqueeze(0)  # shape (1, 3, 224, 224)

#     with torch.no_grad():
#         logits = model(img_tensor)

#     # 获取最大概率的类别
#     pred_idx = logits.argmax(dim=1).item()
#     action = inv_action_map[pred_idx]

#     return action

def infer_device(model,img):
    img_tensor = transform(img).unsqueeze(0)  # shape (1, 3, 224, 224)

    with torch.no_grad():
        logits = model(img_tensor)

    # 获取最大概率的类别
    pred_idx = logits.argmax(dim=1).item()
    action = inv_action_map[pred_idx]

    return action

# ================================================
#  主入口
# ================================================
if __name__ == "__main__":
    MODEL_PATH = "D:\\P5X_train\\action_clone_model.pth"

    model_yolo = torch.hub.load('D:/gitcode/dev/atuotest/yolov5-master', 'custom', path='D:/gitcode/dev/atuotest/yolov5-master/runs/train/p5x/weights/best.pt', source='local')
    model_yolo.eval()
    model_yolo.half()
    cuda = 'cuda' if torch.cuda.is_available() else 'cpu'
    model_yolo.to(cuda)

    device = u2.connect()
    model = load_model(MODEL_PATH, num_actions=14)




    while True:
        img=device.screenshot()
        result = infer_device(model, img)
        print(result)
        results = model_yolo(img)
        predictions = results.xywh[0].cpu().numpy()

        position = {}

        for pred in predictions:
            x_center, y_center, width, height, confidence, class_id = pred
            if position.get(int(class_id)):
                position[int(class_id)].append((int(x_center), int(y_center)))
            else:
                position[int(class_id)] = [(int(x_center), int(y_center))]

        if position.get(4):
            for guide in position.get(4):
                device.click(guide[0],guide[1])
        elif position.get(5):
            for jump in position.get(5):
                device.click(jump[0],jump[1])
        elif position.get(6):
            for attack in position.get(6):
                device.click(attack[0],attack[1])
        elif position.get(7):
            for sumbit in position.get(7):
                device.click(sumbit[0],sumbit[1])
        elif position.get(8):
            for cancel in position.get(8):
                device.click(cancel[0],cancel[1])
        elif position.get(9):
            for close in position.get(9):
                device.click(close[0],close[1])
        elif position.get(10):
            for action in position.get(10):
                device.click(action[0],action[1])
        elif position.get(11):
            for chiose in position.get(11):
                device.click(chiose[0],chiose[1])
        else:
            if result == 'blank':
                device.click(0.25,0.75)
            elif result == 'up':
                if position.get(2):
                    direction = position.get(2)[0]
                    device.swipe(direction[0],direction[1],direction[0],direction[1]-100)
                    print(direction[0],direction[1],direction[0],direction[1]-100)
                else:
                    device.click(0.25,0.75)
            elif result == 'left':
                if position.get(2):
                    direction = position.get(2)[0]
                    device.swipe(direction[0],direction[1],direction[0]-100,direction[1])
                    print(direction[0],direction[1],direction[0]-100,direction[1])
                else:
                    device.click(0.25,0.75)

            elif result == 'right':
                if position.get(2):
                    direction = position.get(2)[0]
                    device.swipe(direction[0],direction[1],direction[0]+100,direction[1])
                    print(direction[0],direction[1],direction[0]+100,direction[1]-0.1)
                else:
                    device.click(0.25,0.75)
            
#======================================================================================================================
        # if result == 'blank':
        #     device.click(0.25,0.75)
        # elif result == 'up':
        #     if position.get(2):
        #         direction = position.get(2)[0]
        #         device.swipe(direction[0],direction[1],direction[0],direction[1]-100)
        #         print(direction[0],direction[1],direction[0],direction[1]-100)
        #     else:
        #         device.click(0.25,0.75)
        # elif result == 'left':
        #     if position.get(2):
        #         direction = position.get(2)[0]
        #         device.swipe(direction[0],direction[1],direction[0]-100,direction[1])
        #         print(direction[0],direction[1],direction[0]-100,direction[1])
        #     else:
        #         device.click(0.25,0.75)

        # elif result == 'right':
        #     if position.get(2):
        #         direction = position.get(2)[0]
        #         device.swipe(direction[0],direction[1],direction[0]+100,direction[1])
        #         print(direction[0],direction[1],direction[0]+100,direction[1]-0.1)
        #     else:
        #         device.click(0.25,0.75)
            
        # elif result == 'guide':
        #     if position.get(4):
        #         direction = position.get(4)[0]
        #         device.click(direction[0],direction[1])
        #         print(direction[0],direction[1])
        #     else:
        #         device.click(0.25,0.75)
           
        # elif result == 'jump':
        #     if position.get(5):
        #         direction = position.get(5)[0]
        #         device.click(direction[0],direction[1])
        #         print(direction[0],direction[1])
        #     else:
        #         device.click(0.25,0.75)
        # elif result == 'attack':
        #     if position.get(6):
        #         direction = position.get(6)[0]
        #         device.click(direction[0],direction[1])
        #         print(direction[0],direction[1])
        #     else:
        #         device.click(0.25,0.75)
        # elif result == 'sumbit':
        #     if position.get(7):
        #         direction = position.get(7)[0]
        #         device.click(direction[0],direction[1])
        #         print(direction[0],direction[1])
        #     else:
        #         device.click(0.25,0.75)
        # elif result == 'cancel':
        #     if position.get(8):
        #         direction = position.get(8)[0]
        #         device.click(direction[0],direction[1])
        #         print(direction[0],direction[1])
        #     else:
        #         device.click(0.25,0.75)
        # elif result == 'close':
        #     if position.get(9):
        #         direction = position.get(9)[0]
        #         device.click(direction[0],direction[1])
        #         print(direction[0],direction[1])
        #     else:
        #         device.click(0.25,0.75)
        # elif result == 'action':
        #     if position.get(10):
        #         direction = position.get(10)[0]
        #         device.click(direction[0],direction[1])
        #         print(direction[0],direction[1])
        #     else:
        #         device.click(0.25,0.75)
        # elif result == 'chiose':
        #     if position.get(11):
        #         direction = position.get(11)[0]
        #         device.click(direction[0],direction[1])
        #         print(direction[0],direction[1])
        #     else:
        #         device.click(0.25,0.75)
        # elif result == 'start':
        #     pass
        # elif result == 'direction':
        #     device.click(0.25,0.75)


