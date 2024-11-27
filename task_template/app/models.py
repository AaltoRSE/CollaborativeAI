from typing import Any, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class TaskDataRequest(BaseModel):
    text: Optional[str] = None
    inputData: Any
    image: Optional[str] = None
    objective: Optional[str] = None


class ModelResponse(BaseModel):
    # The text of the request
    text: str
    # the image of the request
    image: Optional[str] = Field(default=None, nullable=True)


class TaskDataResponse(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None
    outputData: Optional[Any] = None


class TaskRequirements(BaseModel):
    needs_text: bool
    needs_image: bool
    multirequest: Optional[bool] = Field(default=False)


class TaskMetrics(BaseModel):
    metrics: Any

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


class TaskRequest(BaseModel):
    # The text of the request
    content : List[Message]    
