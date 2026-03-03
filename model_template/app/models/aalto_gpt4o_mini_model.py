import os
import logging

from langchain_openai import ChatOpenAI
from app.schemas.data_models import *
from app.models.basemodel import AIModel
from app.schemas.api_schemas import ModelDefinition
logger = logging.getLogger("app")

# NOTE: This needs to be defined in the environment this model is running in.
default_headers = {"Ocp-Apim-Subscription-Key": os.environ["OPENAI_API_KEY"]}

model_definition = ModelDefinition(
    needs_text = True,
    needs_image = False,
    can_text = True,
    can_image = False,
    modelID = "GPT4o-mini",
    hostname=os.environ.get("SERVICE_NAME", "unknown")
)


class aalto_gpt4o_mini(AIModel):
    def get_model_definition(self) -> ModelDefinition:
        return model_definition

    def publish_metrics(self, metrics_json: str) -> None:
        logger.info(metrics_json)

    async def get_response(self, message: TaskInput) -> TaskOutput:
        model = ChatOpenAI(
            base_url="https://aalto-openai-apigw.azure-api.net/v1/openai/deployments/gpt-4o-mini-2024-07-18/",
            default_headers=default_headers,
        )
        AIresponse = model.invoke(message.model_dump()["messages"])
        taskResponse = TaskOutput()
        taskResponse.text = AIresponse.content
        return taskResponse
