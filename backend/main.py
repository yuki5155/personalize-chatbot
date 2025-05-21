from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple API", description="固定値を返すシンプルなAPI")

# フロントエンドのオリジン
origins = [
    "http://localhost:5173",  # Viteのデフォルトポート
    "http://127.0.0.1:5173",
    "http://localhost:3000",  # Create React Appのデフォルトポート
    "http://127.0.0.1:3000",
    "http://localhost:8080",  # 他の一般的なフロントエンドポート
    "http://127.0.0.1:8080",
    # 必要に応じて追加
]

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # プリフライトリクエストのキャッシュ時間（秒）
)

# デバッグ用のミドルウェア
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request path: {request.url.path}")
    logger.info(f"Request headers: {request.headers}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# APIルーターの登録
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 