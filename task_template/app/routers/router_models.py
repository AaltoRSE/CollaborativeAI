from typing import Any, List, Optional, Union
from pydantic import BaseModel, ConfigDict
from models import Message


class ConversationItem(BaseModel):
    role: str
    content: str
    


class SessionData(BaseModel):
    history: List[ConversationItem]
    id: str


class TaskRequest(BaseModel):
    text: List[ConversationItem]
    image: Optional[str] = None
    system: str

class OpenAIChatBaseModel(BaseModel):
    messages: Optional[List[Message]] = None
    model_config = ConfigDict(extra="ignore")