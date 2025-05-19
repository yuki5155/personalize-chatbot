from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Literal
from datetime import datetime, timedelta
import time

router = APIRouter(
    prefix="/threads",
    tags=["threads"]
)


@router.get("")
def get_threads() -> List[Dict[str, Any]]:
    """
    スレッドの一覧を取得します（モックデータ）
    
    Returns:
        List[Dict]: スレッドの一覧
    """
    # 現在のUNIXタイムスタンプ（ミリ秒）
    current_time = int(time.time() * 1000)
    
    # モックデータの作成
    mock_threads = [
        {
            "id": 1,
            "title": "AI技術についての議論",
            "messages": [
                {
                    "id": 1,
                    "text": "最近の生成AIの進歩についてどう思いますか？",
                    "sender": "user",
                    "timestamp": current_time - 3600000  # 1時間前
                },
                {
                    "id": 2,
                    "text": "生成AIは非常に興味深い発展を遂げています。特に言語理解と生成の能力は飛躍的に向上しました。",
                    "sender": "assistant",
                    "timestamp": current_time - 3590000  # 59分50秒前
                }
            ],
            "createdAt": current_time - 3600000,  # 1時間前
            "updatedAt": current_time - 3590000,  # 59分50秒前
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
                    "timestamp": current_time - 86400000  # 1日前
                },
                {
                    "id": 4,
                    "text": "京都には多くの素晴らしい観光スポットがあります。特に嵐山、金閣寺、伏見稲荷大社は外せません。",
                    "sender": "assistant",
                    "timestamp": current_time - 86390000  # 23時間59分10秒前
                },
                {
                    "id": 5,
                    "text": "食事のおすすめはありますか？",
                    "sender": "user",
                    "timestamp": current_time - 86380000  # 23時間59分前
                },
                {
                    "id": 6,
                    "text": "京都では湯豆腐、おばんざい、京風すき焼きなどの伝統的な京料理がおすすめです。",
                    "sender": "assistant",
                    "timestamp": current_time - 86370000  # 23時間57分30秒前
                }
            ],
            "createdAt": current_time - 86400000,  # 1日前
            "updatedAt": current_time - 86370000,  # 23時間57分30秒前
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
                    "timestamp": current_time - 172800000  # 2日前
                },
                {
                    "id": 8,
                    "text": "Pythonでリストを効率的に処理するには、リスト内包表記、map/filter関数、または専用ライブラリ（NumPy, pandas）の使用がおすすめです。",
                    "sender": "assistant",
                    "timestamp": current_time - 172790000  # 2日前（10秒後）
                }
            ],
            "createdAt": current_time - 172800000,  # 2日前
            "updatedAt": current_time - 172790000,  # 2日前（10秒後）
            "isActive": False
        }
    ]
    
    return mock_threads


@router.get("/{thread_id}")
def get_thread(thread_id: int) -> Dict[str, Any]:
    """
    指定されたIDのスレッドを取得します（モックデータ）
    
    Args:
        thread_id: スレッドID
        
    Returns:
        Dict: スレッド情報
    """
    # get_threadsから全スレッドを取得
    all_threads = get_threads()
    
    # 指定されたIDのスレッドを検索
    for thread in all_threads:
        if thread["id"] == thread_id:
            return thread
    
    # スレッドが見つからない場合は404エラー
    raise HTTPException(status_code=404, detail="Thread not found")
