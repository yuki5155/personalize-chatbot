from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any, Literal, Optional
from datetime import datetime, timedelta
import time
import asyncio
from fastapi.responses import StreamingResponse
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

@router.post("/{thread_id}/assistant/stream", status_code=200)
async def create_assistant_message_stream(
    thread_id: int,
    message_data: MessageCreate,
    user: Dict[str, Any] = Depends(get_user_from_cookie)
):
    """
    ログインユーザー専用: 指定されたスレッドにアシスタントのメッセージをストリーミングで作成します
    メッセージの文字列を10秒間かけて少しずつ送信します
    
    Args:
        thread_id: メッセージを追加するスレッドのID
        message_data: 作成するメッセージのデータ
        user: 認証されたユーザー情報（依存関数から取得）
        
    Returns:
        StreamingResponse: 文字列を徐々に返すストリーミングレスポンス
    """
    global MAX_MESSAGE_ID
    
    print(f"ストリーミングリクエスト受信: thread_id={thread_id}, message={message_data.text}")
    
    # 指定されたIDのスレッドを検索
    thread = None
    for t in MOCK_THREADS:
        if t["id"] == thread_id:
            thread = t
            break
    
    if thread is None:
        print(f"スレッド {thread_id} が見つかりません")
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # スレッドがアクティブでない場合はエラー
    if not thread["isActive"]:
        print(f"スレッド {thread_id} は非アクティブです")
        raise HTTPException(status_code=400, detail="Cannot add message to inactive thread")
    
    # 現在の時刻を取得（ミリ秒）
    current_time = int(time.time() * 1000)
    
    # IDをインクリメント
    MAX_MESSAGE_ID += 1
    print(f"新しいメッセージID: {MAX_MESSAGE_ID}")
    
    message_text = message_data.text
    
    # 新しいアシスタントメッセージを作成 (最初は空の状態で)
    new_message = {
        "id": MAX_MESSAGE_ID,
        "text": "",  # 空の状態で始める
        "sender": "assistant",
        "timestamp": current_time
    }
    
    # スレッドのメッセージリストに追加
    thread["messages"].append(new_message)
    
    # スレッドの更新日時を更新
    thread["updatedAt"] = current_time
    
    # ログイン情報をログに出力（デバッグ用）
    print(f"User {user['name']} (ID: {user['id']}) started streaming assistant message to thread {thread_id}")
    
    async def message_generator():
        """メッセージを少しずつ生成するジェネレータ関数"""
        full_text = message_text
        chars_total = len(full_text)
        
        print(f"ストリーミング開始: 全文字数={chars_total}, 予想時間=10秒")
        
        # 完全なメッセージを10秒かけて送信
        delay_per_char = 10.0 / chars_total if chars_total > 0 else 0
        
        # 少しずつ文字を送信
        for i in range(chars_total):
            # スレッドのメッセージを更新
            new_message["text"] = full_text[:i+1]
            
            # 現在の文字を送信
            current_char = full_text[i:i+1]
            print(f"文字送信: '{current_char}' ({i+1}/{chars_total})")
            yield current_char
            
            # 次の文字までの待機時間
            await asyncio.sleep(delay_per_char)
        
        print("ストリーミング完了")
    
    print("StreamingResponseを返します")
    return StreamingResponse(
        message_generator(),
        media_type="text/plain"
    ) 