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
    modelID = "o1-mini",
    hostname=os.environ.get("SERVICE_NAME", "unknown")
)



class o1miniAalto(AIModel):
    def get_model_definition(self) -> ModelDefinition:
        return model_definition

    def publish_metrics(self, metrics_json: str) -> None:
        logger.info(metrics_json)

    async def get_response(self, message: TaskInput) -> TaskOutput:
        model = ChatOpenAI(
            base_url="https://aalto-openai-apigw.azure-api.net/v1/openai/deployments/o1-mini-2024-09-12/",
            default_headers=default_headers,
        )
        ai_messages = message.model_dump()["messages"]
        for ai_message in ai_messages:
            if ai_message["role"] == "system":
                # o1mini does not understand system messages
                ai_message["role"] = "user"
        AIresponse = model.invoke(ai_messages)
        taskResponse = TaskOutput()
        taskResponse.text = AIresponse.content
        return taskResponse
