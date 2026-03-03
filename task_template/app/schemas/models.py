from typing import Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.router_models import InputMessage, Message
from app.schemas.api_schemas import ModelRequirements
class TaskDataRequest(BaseModel):
    text: Optional[str] = None
    inputData: Any
    image: Optional[str] = None
    objective: Optional[str] = None


class TaskRequest(BaseModel):
    # The text of the request
    text: Optional[str] = Field(default="", description="The text message of the request")
    # the image of the request
    image: Optional[str] = Field(default=None, description="The image associated with the request")
    # The system message of the request
    system: str


class OpenAIBasedRequest(BaseModel):
    # The messages that the model should process
    messages: Optional[List[Message]] = None
    # The model configuration
    model_config = ConfigDict(extra="ignore")

class OpenAIBasedDataRequest(BaseModel):
    userMessages: Optional[List[InputMessage]] = []
    objective: Optional[str] = None
    inputData: Optional[Any] = None
    model_config = ConfigDict(extra="ignore")

class ModelResponse(BaseModel):
    # The text of the request
    text: str
    # the image of the request
    image: Optional[str] = Field(default=None, description="The image associated with the request")


class TaskDataResponse(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None
    outputData: Optional[Any] = None


class TaskRequirements(ModelRequirements):
    pass

class TaskMetrics(BaseModel):
    metrics: Any
