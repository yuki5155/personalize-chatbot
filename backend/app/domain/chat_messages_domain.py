from app.domain.base import AbstractDomain
import uuid
from pydantic import Field
from datetime import datetime
from typing import List
from app.domain.enums import ChatMessageRole

class ChatMessageDomain(AbstractDomain):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str = Field(..., description="The message content")
    role: ChatMessageRole = Field(..., description="The role of the message sender")

    def _add_message(self, message: str, role: ChatMessageRole):
        self.message = message
        self.role = role

    def add_user_message(self, message: str):
        self._add_message(message, ChatMessageRole.USER)

    def add_assistant_message(self, message: str):
        self._add_message(message, ChatMessageRole.ASSISTANT)

    
    def to_repository(self):
        # Import inside method to avoid circular import
        from app.infrastructure.models.chat_model import ChatMessage
        return ChatMessage(
            id=self.id,
            message=self.message,
            role=self.role,
            createdAt=self.createdAt,
            updatedAt=self.updatedAt
        )

class ChatMessagesDomain(AbstractDomain):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: List[ChatMessageDomain] = Field(default_factory=list)

    def to_repository(self):
        return [x.to_repository() for x in self.messages]
    
    def add_message(self, message: str, role: ChatMessageRole):
        new_message = ChatMessageDomain(
            message=message,
            role=role
        )
        self.messages.append(new_message)
        return new_message
        
    def add_user_message(self, message: str):
        return self.add_message(message, ChatMessageRole.USER)
        
    def add_assistant_message(self, message: str):
        return self.add_message(message, ChatMessageRole.ASSISTANT)

if __name__ == "__main__":
    chat_message = ChatMessageDomain(
        message="Hello, how are you?",
        role=ChatMessageRole.USER
    )
    print(chat_message.to_repository())
    
    chat_messages = ChatMessagesDomain(
        messages=[chat_message],
    )
    print(chat_messages.to_repository())