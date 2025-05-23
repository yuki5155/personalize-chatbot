from app.infrastructure.models.base import AbstractModel
import uuid
from pydantic import Field
from typing import List
import json
from app.domain.enums import ChatMessageRole

class ChatMessage(AbstractModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str
    role: ChatMessageRole

    def to_domain(self):
        # Import inside method to avoid circular import
        from app.domain.chat_messages_domain import ChatMessageDomain
        return ChatMessageDomain(
            id=self.id,
            message=self.message,
            role=self.role,
            createdAt=self.createdAt,
            updatedAt=self.updatedAt
        )
    
    def to_json(self) -> str:
        return json.dumps({
            "id": self.id,
            "message": self.message,
            "role": self.role.value,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ChatMessage':
        data = json.loads(json_str)
        # Convert string role to enum if needed
        if isinstance(data["role"], str):
            data["role"] = ChatMessageRole(data["role"])
        return cls(**data)


class ChatModel(AbstractModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[ChatMessage] = Field(default_factory=list)
    user_id: str
    is_active: bool = Field(default=True)
    title: str = Field(default="")

    def to_domain(self):
        # Import inside method to avoid circular import
        from app.domain.threads_domain import ThreadDomain
        from app.domain.chat_messages_domain import ChatMessageDomain, ChatMessagesDomain
        
        # Create ChatMessagesDomain with the messages
        chat_messages = ChatMessagesDomain(
            messages=[message.to_domain() for message in self.messages]
        )
        
        return ThreadDomain(
            id=self.id,
            name="Chat Session",  # Default name
            chat_messages=chat_messages,
            user_id=self.user_id,
            is_active=self.is_active,
            title=self.title,
            createdAt=self.createdAt,
            updatedAt=self.updatedAt
        )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "messages": [message.to_json() for message in self.messages],
            "user_id": self.user_id,
            "is_active": self.is_active,
            "title": self.title,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

    def from_dict(self, data: dict) -> 'ChatModel':
        return ChatModel(
            id=data["id"],
            messages=[ChatMessage.from_json(message) for message in data["messages"]],
            user_id=data["user_id"],
            is_active=data["is_active"],
            title=data["title"],
            createdAt=data["createdAt"],
            updatedAt=data["updatedAt"]
        )
        
if __name__ == "__main__":
    chat_message = ChatMessage(
        message="Hello, how are you?",
        role=ChatMessageRole.USER
    )
    # print(chat_message.to_domain())
    
    chat_model = ChatModel(
        messages=[chat_message],
        user_id="test-user-123",
        is_active=True,
        title="Test Title"
    )
    print(chat_model.to_domain())

    print(chat_model.to_dict())

    print(chat_model.from_dict(chat_model.to_dict()))