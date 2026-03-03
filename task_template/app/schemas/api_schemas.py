"""Pydantic models converted from model_handler.proto

Each protobuf `message` has been mapped to a Pydantic `BaseModel`.
Field names follow the proto field names to preserve JSON compatibility.
"""
from typing import Optional
from pydantic import BaseModel


class APITaskRequest(BaseModel):
    request: Optional[str] = None
    sessionID: Optional[str] = None


class ModelAnswer(BaseModel):
    answer: str
    sessionID: Optional[str] = None


class IdMessage(BaseModel):
    sessionID: str


class APITaskMetrics(BaseModel):
    sessionID: str
    metrics: str

class ModelRequirements(BaseModel):
    needs_text: bool = False
    needs_image: bool = False    


class ModelInfo(BaseModel):
    model_name: str
    sessionID: str


class Empty(BaseModel):
    pass


__all__ = [
    "TaskRequest",
    "ModelAnswer",
    "IdMessage",
    "TaskMetrics",
    "ModelRequest",
    "ModelDefinition",
    "ModelRequirements",
    "ModelInfo",
    "Empty",
]
