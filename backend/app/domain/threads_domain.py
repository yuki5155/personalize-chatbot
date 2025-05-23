from app.domain.base import AbstractDomain
from pydantic import Field
from datetime import datetime
import uuid
from app.domain.chat_messages_domain import ChatMessagesDomain

class ThreadDomain(AbstractDomain):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="The name of the thread")
    createdAt: str = Field(default_factory=lambda: datetime.now().isoformat())
    updatedAt: str = Field(default_factory=lambda: datetime.now().isoformat())
    chat_messages: ChatMessagesDomain = Field(..., description="The chat messages of the thread")
    user_id: str = Field(..., description="The user ID")
    is_active: bool = Field(default=True, description="The active status of the thread")
    title: str = Field(default="", description="The title of the thread")

    
    def add_user_message(self, message: str):
        self.chat_messages.add_user_message(message)
    
    def add_assistant_message(self, message: str):
        self.chat_messages.add_assistant_message(message)
    
    def to_repository(self):
        # Import inside method to avoid circular import
        from app.infrastructure.models.chat_model import ChatModel
        return ChatModel(
            id=self.id,
            messages=self.chat_messages.to_repository(),
            user_id=self.user_id,
            is_active=self.is_active,
            title=self.title,
            createdAt=self.createdAt,
            updatedAt=self.updatedAt
        )
    

if __name__ == "__main__":
    from app.domain.chat_messages_domain import ChatMessageDomain, ChatMessageRole
    chat_messages = ChatMessagesDomain(
        user_id="123",
        messages=[ChatMessageDomain(message="Hello, how are you?", role=ChatMessageRole.USER)]
    )
    thread = ThreadDomain(
        name="Test Thread",
        chat_messages=chat_messages,
        user_id="123",
        is_active=True,
        title="Test Title"
    )
    
    print(thread.to_repository())