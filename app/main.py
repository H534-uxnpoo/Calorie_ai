from fastapi import FastAPI, UploadFile, File
#import shutil
#import os
from PIL import Image  #pillow → 画像読み込み
from io import BytesIO
import torch  #torch → AI本体
from torchvision import models, transforms  #torchvision → 画像モデル


# FastAPI設定
app = FastAPI(title="Calorie AI")

# 必要ならCORS設定（ブラウザからアクセスする場合）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Reactなどのフロント指定
    allow_methods=["*"],
    allow_headers=["*"],
)

# モデル読み込み

device = torch.device("cpu")
model = models.mobilenet_v2(pretrained=False)
model.classifier[1] = torch.nn.Linear(model.last_channel, 101)
model.load_state_dict(torch.load("models/mobilenet_v2_food101.pth", map_location=device))
model.eval()


# Food101ラベル読み込み
with open("data/food101_labels.txt", "r") as f:
    food101_labels = [line.strip() for line in f.readlines()]

# ImageNetのラベル取得
#import urllib.request
#LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
#labels = urllib.request.urlopen(LABELS_URL).read().decode('utf-8').splitlines()

#import torch.nn.functional as F
#app = FastAPI()
#UPLOAD_DIR="uploads"

# モデル読み込み（初回だけ）
#model = models.resnet18(pretrained=True)
#model.eval()

# 前処理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
    ])

calorie_dict = {
    "pizza": 300,
    "burger": 250,
    "hotdog": 200,
    "spaghetti": 280,
    "ramen": 450,
    "salad": 100
}

def preprocess_image(file_bytes):
    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    return transform(image).unsqueeze(0)

@app.get("/")
def read_root():
    return {"message": "Hello Calorie AI"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_bytes = await file.read()
    input_tensor = preprocess_image(file_bytes)
    #file_path=os.path.join(UPLOAD_DIR, file.filename)

    #with open(file_path, "wb") as buffer:  #buffer → データをコピーさずに目盛を共有
    #    shutil.copyfileobj(file.file, buffer)  #読み込み元のファイルオブジェクトから、書き込み先のファイルオブジェクトへコピーする

    # 画像読み込み
    #image = Image.open(file_path)
    #image = transform(image).unsqueeze(0)

    # AIで判定
    with torch.no_grad():
        file_bytes = await file.read()
        input_tensor = preprocess_image(file_bytes)
        #output = model(image)

    # 一番確率が高いもの
    #_, predicted = torch.max(output, 1)
    #label = labels[predicted.item()]

    predicted_label = food101_labels[predicted_idx.item()]
    calorie = calorie_dict.get(predicted_label, "不明")

    return {"prediction": predicted_label, "calorie": calorie}