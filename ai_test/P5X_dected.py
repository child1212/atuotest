import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image


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
action_map = {'blank':0,'up':1,'left':2,'right':3,'guide':4,'jump':5,'attack':6,'sumbit':7,'cancel':8,'close':9,'action':10,'chiose':11,'start':12}  # 根据实际操作调整
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
def infer(model, image_path):
    img = Image.open(image_path).convert("RGB")
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
    IMAGE_FILE = "D:\\P5X_train\\P5X125.jpg"   # 你要推理的图像

    model = load_model(MODEL_PATH, num_actions=4)

    result = infer(model, IMAGE_FILE)

    print(f"动作识别结果: {result}")
