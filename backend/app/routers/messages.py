from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any, Literal, Optional
from datetime import datetime, timedelta
import time
from app.dependencies import get_user_from_cookie
from pydantic import BaseModel

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

# threads.pyのモックデータを参照するため、importする
from app.routers.threads import MOCK_THREADS, MAX_MESSAGE_ID

# リクエストのモデル定義
class MessageCreate(BaseModel):
    text: str


@router.get("/{thread_id}")
async def get_messages(
    thread_id: int, 
    user: Dict[str, Any] = Depends(get_user_from_cookie)
) -> List[Dict[str, Any]]:
    """
    ログインユーザー専用: 指定されたスレッドのメッセージ一覧を取得します
    
    Args:
        thread_id: メッセージを取得するスレッドのID
        user: 認証されたユーザー情報（依存関数から取得）
    
    Returns:
        List[Dict]: メッセージの一覧
    """
    # ログイン情報をログに出力（デバッグ用）
    print(f"User {user['name']} (ID: {user['id']}) accessed messages for thread {thread_id}")
    
    # 指定されたIDのスレッドを検索
    for thread in MOCK_THREADS:
        if thread["id"] == thread_id:
            return thread["messages"]
    
    # スレッドが見つからない場合は404エラー
    raise HTTPException(status_code=404, detail="Thread not found")


@router.post("/{thread_id}", status_code=201)
async def create_message(
    thread_id: int,
    message_data: MessageCreate,
    user: Dict[str, Any] = Depends(get_user_from_cookie)
) -> Dict[str, Any]:
    """
    ログインユーザー専用: 指定されたスレッドに新しいメッセージを作成します
    
    Args:
        thread_id: メッセージを追加するスレッドのID
        message_data: 作成するメッセージのデータ
        user: 認証されたユーザー情報（依存関数から取得）
        
    Returns:
        Dict: 作成されたメッセージ情報
    """
    global MAX_MESSAGE_ID
    
    # 指定されたIDのスレッドを検索
    thread = None
    for t in MOCK_THREADS:
        if t["id"] == thread_id:
            thread = t
            break
    
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # スレッドがアクティブでない場合はエラー
    if not thread["isActive"]:
        raise HTTPException(status_code=400, detail="Cannot add message to inactive thread")
    
    # 現在の時刻を取得（ミリ秒）
    current_time = int(time.time() * 1000)
    
    # IDをインクリメント
    MAX_MESSAGE_ID += 1
    
    # 新しいメッセージを作成
    new_message = {
        "id": MAX_MESSAGE_ID,
        "text": message_data.text,
        "sender": "user",
        "timestamp": current_time
    }
    
    # スレッドのメッセージリストに追加
    thread["messages"].append(new_message)
    
    # スレッドの更新日時を更新
    thread["updatedAt"] = current_time
    
    # ログイン情報をログに出力（デバッグ用）
    print(f"User {user['name']} (ID: {user['id']}) added message to thread {thread_id}")
    
    return new_message


@router.post("/{thread_id}/assistant", status_code=201)
async def create_assistant_message(
    thread_id: int,
    message_data: MessageCreate,
    user: Dict[str, Any] = Depends(get_user_from_cookie)
) -> Dict[str, Any]:
    """
    ログインユーザー専用: 指定されたスレッドにアシスタントのメッセージを作成します
    主にテスト用や管理者の操作用のエンドポイントです
    
    Args:
        thread_id: メッセージを追加するスレッドのID
        message_data: 作成するメッセージのデータ
        user: 認証されたユーザー情報（依存関数から取得）
        
    Returns:
        Dict: 作成されたメッセージ情報
    """
    global MAX_MESSAGE_ID
    
    # 指定されたIDのスレッドを検索
    thread = None
    for t in MOCK_THREADS:
        if t["id"] == thread_id:
            thread = t
            break
    
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # スレッドがアクティブでない場合はエラー
    if not thread["isActive"]:
        raise HTTPException(status_code=400, detail="Cannot add message to inactive thread")
    
    # 現在の時刻を取得（ミリ秒）
    current_time = int(time.time() * 1000)
    
    # IDをインクリメント
    MAX_MESSAGE_ID += 1
    
    # 新しいアシスタントメッセージを作成
    new_message = {
        "id": MAX_MESSAGE_ID,
        "text": message_data.text,
        "sender": "assistant",
        "timestamp": current_time
    }
    
    # スレッドのメッセージリストに追加
    thread["messages"].append(new_message)
    
    # スレッドの更新日時を更新
    thread["updatedAt"] = current_time
    
    # ログイン情報をログに出力（デバッグ用）
    print(f"User {user['name']} (ID: {user['id']}) added assistant message to thread {thread_id}")
    
    return new_message 