from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from datetime import datetime

    
# abstractmethodを持つモデルを定義
class AbstractModel(BaseModel, ABC):
    createdAt: str = Field(default_factory=lambda: datetime.now().isoformat())
    updatedAt: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    @abstractmethod
    def to_domain(self) -> dict:
        pass
    
    