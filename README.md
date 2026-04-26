# Calorie_ai
画像から料理を自動で判別し、推定カロリーと栄養アドバイスを生成するAIバックエンドアプリです。

概要
Googleの最新AIモデル **Gemini 1.5 Flash** を活用し、食事の画像から以下の情報を抽出します。
- 料理ごとの推定重量とカロリー
- 合計摂取カロリー
- 管理栄養士のような栄養バランスのアドバイス

大学の課題や個人プロジェクトのベースとして、FastAPIを用いて効率的に開発しました。

使用技術
- **Language:** Python 3.12+
- **Framework:** FastAPI
- **AI Engine:** Google Gemini API (gemini-1.5-flash)
- **Environment:** venv, python-dotenv
- **API Documentation:** Swagger UI (FastAPI内蔵)
