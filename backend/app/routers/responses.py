from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime


class Message(BaseModel):
    id: int
    text: str
    sender: Literal["user", "assistant"]
    timestamp: int


class Thread(BaseModel):
    id: int
    title: str
    messages: List[Message]
    createdAt: int
    updatedAt: int
    isActive: bool


class ThreadListResponse(BaseModel):
    threads: List[Thread]


class ThreadResponse(BaseModel):
    thread: Thread


class MessageResponse(BaseModel):
    message: Message


# get_threadsのレスポンススキーマ（リストとして直接返すためのスキーマ）
class ThreadItem(BaseModel):
    id: int
    title: str
    messages: List[Message]
    createdAt: int
    updatedAt: int
    isActive: bool

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "AI技術についての議論",
                "messages": [
                    {
                        "id": 1,
                        "text": "最近の生成AIの進歩についてどう思いますか？",
                        "sender": "user",
                        "timestamp": 1677123456789
                    }
                ],
                "createdAt": 1677123456789,
                "updatedAt": 1677123456999,
                "isActive": True
            }
        }

# create_threadとget_threadのレスポンススキーマ（単一スレッドの直接返却用）
class ThreadItemSingle(BaseModel):
    id: int
    title: str
    messages: List[Message]
    createdAt: int
    updatedAt: int
    isActive: bool

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "新しいスレッド",
                "messages": [
                    {
                        "id": 1,
                        "text": "初めてのメッセージ",
                        "sender": "user",
                        "timestamp": 1677123456789
                    }
                ],
                "createdAt": 1677123456789,
                "updatedAt": 1677123456789,
                "isActive": True
            }
        } 