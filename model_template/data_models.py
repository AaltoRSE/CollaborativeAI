from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Union


class TaskMessage(BaseModel):
    role: str  # The role of the Message (either "assistant" or "user")
    content: str  # The content of the message


class TaskOutput(BaseModel):
    text: str = Field(default="", nullable=True)  # The response Message
    image: str = Field(default=None, nullable=True)  # The image to be processed



class OpenAIMessage(BaseModel):
    type: str


class ImageMessage(OpenAIMessage):
    type: str = "image_url"
    image_url: str
    model_config = ConfigDict(extra="ignore")


class TextMessage(OpenAIMessage):
    type: str = "text"
    text: str
    model_config = ConfigDict(extra="ignore")


class Message(BaseModel):
    role: str
    content: Union[str, List[Union[ImageMessage, TextMessage]]]
    model_config = ConfigDict(extra="ignore")


class TaskInput(BaseModel):
    # The text of the request
    content : List[Message]    
