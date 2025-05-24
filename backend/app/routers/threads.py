from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any, Literal, Optional
from datetime import datetime, timedelta
import time
from app.dependencies import get_user_from_cookie
from pydantic import BaseModel
from app.routers.responses import ThreadItem, ThreadItemSingle, Message
from app.application.services.chat_message_service import ChatMessageService

router = APIRouter(
    prefix="/threads",
    tags=["threads"]
)

# グローバル変数としてモックデータを定義
# 現在のUNIXタイムスタンプ（ミリ秒）
CURRENT_TIME = int(time.time() * 1000)

# モックデータの作成
MOCK_THREADS = [
    {
        "id": 1,
        "title": "AI技術についての議論",
        "messages": [
            {
                "id": 1,
                "text": "最近の生成AIの進歩についてどう思いますか？",
                "sender": "user",
                "timestamp": CURRENT_TIME - 3600000  # 1時間前
            },
            {
                "id": 2,
                "text": "生成AIは非常に興味深い発展を遂げています。特に言語理解と生成の能力は飛躍的に向上しました。",
                "sender": "assistant",
                "timestamp": CURRENT_TIME - 3590000  # 59分50秒前
            }
        ],
        "createdAt": CURRENT_TIME - 3600000,  # 1時間前
        "updatedAt": CURRENT_TIME - 3590000,  # 59分50秒前
        "isActive": True
    },
    {
        "id": 2,
        "title": "旅行の計画",
        "messages": [
            {
                "id": 3,
                "text": "京都旅行のおすすめスポットを教えてください",
                "sender": "user",
                "timestamp": CURRENT_TIME - 86400000  # 1日前
            },
            {
                "id": 4,
                "text": "京都には多くの素晴らしい観光スポットがあります。特に嵐山、金閣寺、伏見稲荷大社は外せません。",
                "sender": "assistant",
                "timestamp": CURRENT_TIME - 86390000  # 23時間59分10秒前
            },
            {
                "id": 5,
                "text": "食事のおすすめはありますか？",
                "sender": "user",
                "timestamp": CURRENT_TIME - 86380000  # 23時間59分前
            },
            {
                "id": 6,
                "text": "京都では湯豆腐、おばんざい、京風すき焼きなどの伝統的な京料理がおすすめです。",
                "sender": "assistant",
                "timestamp": CURRENT_TIME - 86370000  # 23時間57分30秒前
            }
        ],
        "createdAt": CURRENT_TIME - 86400000,  # 1日前
        "updatedAt": CURRENT_TIME - 86370000,  # 23時間57分30秒前
        "isActive": True
    },
    {
        "id": 3,
        "title": "プログラミング質問",
        "messages": [
            {
                "id": 7,
                "text": "Pythonで効率的なリスト処理の方法を教えてください",
                "sender": "user",
                "timestamp": CURRENT_TIME - 172800000  # 2日前
            },
            {
                "id": 8,
                "text": "Pythonでリストを効率的に処理するには、リスト内包表記、map/filter関数、または専用ライブラリ（NumPy, pandas）の使用がおすすめです。",
                "sender": "assistant",
                "timestamp": CURRENT_TIME - 172790000  # 2日前（10秒後）
            }
        ],
        "createdAt": CURRENT_TIME - 172800000,  # 2日前
        "updatedAt": CURRENT_TIME - 172790000,  # 2日前（10秒後）
        "isActive": False
    }
]

# 最大のメッセージIDとスレッドIDを追跡
MAX_THREAD_ID = 3
MAX_MESSAGE_ID = 8

# リクエストのモデル定義
class ThreadCreate(BaseModel):
    title: str
    first_message: str


@router.get("", response_model=List[ThreadItem])
async def get_threads(user: Dict[str, Any] = Depends(get_user_from_cookie)) -> List[Dict[str, Any]]:
    """
    ログインユーザー専用: スレッドの一覧を取得します
    
    Args:
        user: 認証されたユーザー情報（依存関数から取得）
    
    Returns:
        List[Dict]: スレッドの一覧
    """
    # ログイン情報をログに出力（デバッグ用）
    print(f"User {user['name']} (ID: {user['id']}) accessed threads list")
    converted_threads = []
    
    chat_message_service = ChatMessageService()
    threads = await chat_message_service.get_threads_by_user_id(user['id'])
    for thread in threads:
        # Convert UUID string to integer for response model
        try:
            thread_id = int(thread.id.split('-')[0], 16)  # Convert first part of UUID to integer
        except (ValueError, IndexError):
            thread_id = hash(thread.id) % 10000000  # Fallback to hash if conversion fails
            
        # Convert ISO timestamps to Unix timestamps (milliseconds)
        try:
            # Handle ISO format with optional Z timezone indicator
            created_at_str = thread.createdAt.replace('Z', '')
            created_at = int(datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S.%f").timestamp() * 1000)
        except ValueError:
            created_at = int(time.time() * 1000)  # Fallback to current time
            
        try:
            # Handle ISO format with optional Z timezone indicator
            updated_at_str = thread.updatedAt.replace('Z', '')
            updated_at = int(datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%f").timestamp() * 1000)
        except ValueError:
            updated_at = int(time.time() * 1000)  # Fallback to current time
            
        # Convert messages with error handling
        thread_messages = []
        for message in thread.chat_messages.messages:
            try:
                # Parse timestamp with proper handling of Z timezone
                message_created_at = message.createdAt.replace('Z', '')
                timestamp = int(datetime.strptime(message_created_at, "%Y-%m-%dT%H:%M:%S.%f").timestamp() * 1000)
            except (ValueError, AttributeError):
                # Fallback to current time if parsing fails
                timestamp = int(time.time() * 1000)
                
            thread_messages.append(Message(
                id=int(hash(message.id) % 10000000) if isinstance(message.id, str) else message.id,
                text=message.message,
                sender=message.role,
                timestamp=timestamp
            ))
            
        converted_threads.append(ThreadItem(
            id=thread_id,
            title=thread.title,
            messages=thread_messages,
            createdAt=created_at,
            updatedAt=updated_at,
            isActive=thread.is_active
        ))

    return converted_threads


@router.post("", status_code=201, response_model=ThreadItemSingle)
async def create_thread(
    thread_data: ThreadCreate,
    user: Dict[str, Any] = Depends(get_user_from_cookie)
) -> Dict[str, Any]:
    """
    ログインユーザー専用: 新しいスレッドを作成します
    
    Args:
        thread_data: 作成するスレッドのデータ
        user: 認証されたユーザー情報（依存関数から取得）
        
    Returns:
        Dict: 作成されたスレッド情報
    """
    global MAX_THREAD_ID, MAX_MESSAGE_ID, MOCK_THREADS
    
    # 現在の時刻を取得（ミリ秒）
    current_time = int(time.time() * 1000)
    
    # IDをインクリメント
    MAX_THREAD_ID += 1
    MAX_MESSAGE_ID += 1
    
    # 新しいスレッドを作成
    new_thread = {
        "id": MAX_THREAD_ID,
        "title": thread_data.title,
        "messages": [
            {
                "id": MAX_MESSAGE_ID,
                "text": thread_data.first_message,
                "sender": "user",
                "timestamp": current_time
            }
        ],
        "createdAt": current_time,
        "updatedAt": current_time,
        "isActive": True
    }
    
    # モックデータに追加
    MOCK_THREADS.append(new_thread)
    
    # ログイン情報をログに出力（デバッグ用）
    print(f"User {user['name']} (ID: {user['id']}) created new thread {MAX_THREAD_ID}: {thread_data.title}")
    
    return new_thread


@router.get("/{thread_id}", response_model=ThreadItemSingle)
async def get_thread(thread_id: int, user: Dict[str, Any] = Depends(get_user_from_cookie)) -> Dict[str, Any]:
    """
    ログインユーザー専用: 指定されたIDのスレッドを取得します
    
    Args:
        thread_id: スレッドID
        user: 認証されたユーザー情報（依存関数から取得）
        
    Returns:
        Dict: スレッド情報
    """
    # ログイン情報をログに出力（デバッグ用）
    print(f"User {user['name']} (ID: {user['id']}) accessed thread {thread_id}")
    
    # 指定されたIDのスレッドを検索
    for thread in MOCK_THREADS:
        if thread["id"] == thread_id:
            return thread
    
    # スレッドが見つからない場合は404エラー
    raise HTTPException(status_code=404, detail="Thread not found") 