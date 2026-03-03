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
    can_image = False,
    modelID = "GPT4_turbo",
    hostname=os.environ.get("SERVICE_NAME", "unknown")
)



class OpenAIModel(AIModel):
    def get_model_definition(self) -> ModelDefinition:
        return model_definition

    def publish_metrics(self, metrics_json: str) -> None:
        logger.info(metrics_json)

    async def get_response(self, message: TaskInput) -> TaskOutput:
        model = ChatOpenAI(model="gpt-4o")
            
        AIresponse = model.invoke(message.model_dump()["messages"])
        print(f"AIresponse: {AIresponse.content}")
        taskResponse = TaskOutput()
        taskResponse.text = AIresponse.content
        return taskResponse


ai_model = AIModel()
