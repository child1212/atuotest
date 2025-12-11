import os
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
# ------------------------ 数据集定义 ------------------------

class ActionDataset(Dataset):
    def __init__(self, json_file, img_dir, transform=None):
        super().__init__()
        self.img_dir = img_dir  # 图片文件夹路径
        # 加载标签数据（JSON格式）
        with open(json_file, "r") as f:
            self.data = json.load(f)
        self.action_map = {'blank':0,'up':1,'left':2,'right':3,'guide':4,'jump':5,'attack':6,'sumbit':7,'cancel':8,'close':9,'action':10,'chiose':11,'start':12,'direction':13}  # 根据实际操作调整
        self.transform = transform  # 数据增强和预处理


    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        image_path = os.path.join(self.img_dir, item["image"])
        image = Image.open(image_path).convert("RGB")

        # 获取操作标签（如点击的按钮）
        action = item["action"]

        label = self.action_map.get(action, self.action_map["blank"])

        if self.transform:
            image = self.transform(image)
        
        return image, torch.tensor(label, dtype=torch.long)


# ------------------------ 模型定义 ------------------------

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


# ------------------------ 数据加载与训练 ------------------------

def train():
    # --------------------
    # 数据路径（请修改）
    # --------------------
    DATA_JSON = "D:\\gitcode\\dev\\atuotest\\ai_test\\record.json"
    IMG_DIR = "D:\\P5X_train"

    # --------------------
    # 图像预处理
    # --------------------
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    dataset = ActionDataset(DATA_JSON, IMG_DIR, transform)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

    # --------------------
    # 模型与损失
    # --------------------
    num_actions = 14  # tap/swipe/hold/other
    model = ActionCloneModel(num_actions)
    # 加载预训练的模型
    # model.load_state_dict(torch.load("behavior_clone_resnet50.pth"))

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0005)

    # --------------------
    # 开始训练
    # --------------------
    EPOCHS = 100
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    for epoch in range(EPOCHS):
        total_loss = 0

        for imgs, labels in dataloader:
            imgs = imgs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(imgs)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch + 1}/{EPOCHS}, Loss = {total_loss:.4f}")

    # --------------------
    # 保存模型
    # --------------------
        torch.save(model.state_dict(), "action_clone_model_temp.pth")
        print("模型已保存为 action_clone_model_temp.pth")
    torch.save(model.state_dict(), "action_clone_model.pth")
    print("模型已保存为 action_clone_model.pth")



# ------------------------ 程序入口 ------------------------

if __name__ == "__main__":
    train()
# #============================================================================================================================================================



# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.utils.data import Dataset, DataLoader
# from torchvision import models, transforms
# from PIL import Image
# import os
# import json

# # 数据集类：读取图像和标签
# class ActionDataset(Dataset):
#     def __init__(self, data_file, transform=None):
#         self.data = self.load_data(data_file)  # 加载数据
#         self.transform = transform

#     def load_data(self, data_file):
#         """加载数据文件，并返回图像路径和标签"""
#         with open(data_file, 'r') as f:
#             data = json.load(f)
        
#         image_paths = [item["image"] for item in data]
#         labels = [item["action"] for item in data]
        
#         return list(zip(image_paths, labels))

#     def __len__(self):
#         return len(self.data)

#     def __getitem__(self, idx):
#         image_path, label = self.data[idx]
        
#         # 读取图像
#         image = Image.open(image_path).convert("RGB")
        
#         # 图像预处理
#         if self.transform:
#             image = self.transform(image)
        
#         # 转换标签为数字
#         action_map = {'blank':0,'up':1,'left':2,'right':3,'guide':4,'jump':5,'attack':6,'sumbit':7,'cancel':8,'close':9,'action':10,'chiose':11,'start':12,'direction':13}  # 根据实际操作调整
#         label = action_map.get(label, action_map["other"])
        
#         return image, label


# # 定义ResNet50模型
# class ResNet50Model(nn.Module):
#     def __init__(self, num_classes):
#         super(ResNet50Model, self).__init__()
#         self.resnet50 = models.resnet50(pretrained=True)
#         self.resnet50.fc = nn.Linear(self.resnet50.fc.in_features, num_classes)

#     def forward(self, x):
#         return self.resnet50(x)


# # 主训练函数
# def main():
#     # 配置设备
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
#     # 数据预处理
#     transform = transforms.Compose([
#         transforms.Resize((224, 224)),  # 调整图像大小
#         transforms.ToTensor(),  # 转换为Tensor
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 标准化
#     ])
    
#     # 加载数据
#     train_data_file = 'D:\\gitcode\\dev\\atuotest\\ai_test\\record.json'  # 数据集文件路径（JSON格式）
#     dataset = ActionDataset(train_data_file, transform)
#     train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
#     # 初始化模型
#     num_classes = 14  # 动作类别数（tap, swipe, hold, other）
#     model = ResNet50Model(num_classes).to(device)
    
#     # 定义损失函数和优化器
#     criterion = nn.CrossEntropyLoss()  # 交叉熵损失
#     optimizer = optim.Adam(model.parameters(), lr=1e-4)

#     # 训练模型
#     num_epochs = 50  # 训练轮数
#     for epoch in range(num_epochs):
#         model.train()  # 切换到训练模式
#         running_loss = 0.0
#         for inputs, targets in train_loader:
#             inputs, targets = inputs.to(device), targets.to(device)
            
#             # 清空梯度
#             optimizer.zero_grad()

#             # 前向传播
#             outputs = model(inputs)
            
#             # 计算损失
#             loss = criterion(outputs, targets)
            
#             # 反向传播
#             loss.backward()
#             optimizer.step()

#             running_loss += loss.item()
        
#         print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader)}")
    
#     # 保存模型
#     torch.save(model.state_dict(), 'behavior_clone_resnet50.pth')
#     print("Model saved to 'behavior_clone_resnet50.pth'")


# if __name__ == "__main__":
#     main()
