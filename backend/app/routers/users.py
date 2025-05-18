from fastapi import APIRouter, Depends, Response
from typing import Dict, Any
from app.dependencies import get_user_from_cookie

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("")
def get_users():
    """
    固定のユーザーリストを返します
    """
    return [
        {"id": 1, "name": "User 1", "email": "user1@example.com"},
        {"id": 2, "name": "User 2", "email": "user2@example.com"},
        {"id": 3, "name": "User 3", "email": "user3@example.com"}
    ]


@router.get("/me")
async def get_current_user(user: Dict[str, Any] = Depends(get_user_from_cookie)):
    """
    Cookieからユーザー情報を取得し、現在ログインしているユーザーの情報を返します
    
    依存関数 get_user_from_cookie を使用して、Cookieからユーザー情報を取得します。
    """
    return user


@router.get("/set-cookie")
async def set_user_cookie(response: Response):
    """
    テスト用: ユーザーIDをCookieに設定します
    
    Args:
        response: レスポンスオブジェクト
    
    Returns:
        Dict: 処理結果
    """
    # Cookieを設定（実際のアプリではセキュアな設定が必要）
    response.set_cookie(key="user_id", value="default_user")
    return {"message": "ユーザーIDをCookieに設定しました"} 