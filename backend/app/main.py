from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.api import api_router

app = FastAPI(
    title="US-reporting API",
    description="US-reportingシステムのバックエンドAPI",
    version="1.0.0",
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターの登録
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    ルートエンドポイント
    """
    return {"message": "Welcome to US-reporting API"} 