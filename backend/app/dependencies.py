from fastapi import Cookie, HTTPException, status
from typing import Optional, Dict, Any

# 簡易的なユーザーデータベース（実際の環境ではDBを使用します）
USERS_DB = {
    "1": {"id": "default_user", "name": "User 1", "email": "user1@example.com", "role": "admin"},
    "2": {"id": "default_user", "name": "User 2", "email": "user2@example.com", "role": "user"},
    "3": {"id": "default_user", "name": "User 3", "email": "user3@example.com", "role": "user"}
}

async def get_user_from_cookie(user_id: Optional[str] = Cookie(None)) -> Dict[str, Any]:
    """
    Cookieからユーザー情報を取得する依存関数
    
    Args:
        user_id: ユーザーIDが格納されたクッキー（任意）
        
    Returns:
        Dict[str, Any]: ユーザー情報
        
    Raises:
        HTTPException: ユーザーが見つからない場合は401エラー
    """

    print("get_user_from_cookie")
    # Cookieが存在しない場合
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証されていません。ユーザーIDのCookieが必要です。",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = {
        "id": user_id,
        "name": "User 1",
        "email": "user1@example.com",
        "role": "admin"
    }
    
    return user 