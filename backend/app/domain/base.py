from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from datetime import datetime

class AbstractDomain(BaseModel, ABC):
    createdAt: str = Field(default_factory=lambda: datetime.now().isoformat())
    updatedAt: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    @abstractmethod
    def to_repository(self):
        pass
    
    
    
