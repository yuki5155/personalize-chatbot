from fastapi import APIRouter
from app.routers import users_router

api_router = APIRouter()

# ルーターの登録
api_router.include_router(users_router)

# 新しいルーターを追加する場合、ここに追加します
# api_router.include_router(items_router)
# api_router.include_router(auth_router)
# など 