import os
import logging

from langchain_openai import ChatOpenAI
from app.schemas.data_models import *
from app.models.basemodel import AIModel
from app.schemas.api_schemas import ModelDefinition

logger = logging.getLogger("app")

# NOTE: This needs to be defined in the environment this model is running in.
model_definition = ModelDefinition(
    needs_text = True,
    needs_image = False,
    can_text = True,
    can_image = True,
    modelID = "TestModel",
    hostname=os.environ.get("SERVICE_NAME", "unknown")
)


class TestModel(AIModel):
    def get_model_definition(self) -> ModelDefinition:
        return model_definition

    def publish_metrics(self, metrics_json: str) -> None:
        logger.info(metrics_json)

    async def get_response(self, message: TaskInput) -> TaskOutput:        
        taskResponse = TaskOutput()
        taskResponse.text = "This is just for testing"
        logger.info("Returning Message")
        return taskResponse


ai_model = AIModel()
