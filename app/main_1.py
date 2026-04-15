import os
import io
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
print(f"DEBUG: API_KEY is {os.getenv('GEMINI_API_KEY')}")
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    print(f"DEBUG:APIキーを読み込みました (先頭4文字: {API_KEY[:4]}...)")
else:
    print("DEBUG:APIキーが読み込めていません")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={"response_mime_type": "application/json"} 
)

# これをコードに追記して再起動
print("利用可能なモデル")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

app = FastAPI(title="Calorie AI")

@app.post("/analyze")
async def analyze_food(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))

    prompt = """
    画像内の料理を分析し、以下のJSON形式で回答してください。
    推定が難しい場合は、一般的な1人前の分量で計算してください。
    Markdownの装飾('''json ... ''')や\nなど不必要なものは一切含めないでください。
    
    {
      "dishes": [
        {"name":"料理名", "estimate_weight":"00g", "calories":"000kcal"}
      ],
      "total_calories_kcal":"000kcal",
      "advice": "栄養バランスへのアドバイス"
    }
    """

    response = model.generate_content([prompt, img])
    
    return {"result": response.text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)