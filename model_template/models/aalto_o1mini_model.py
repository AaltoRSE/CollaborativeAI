import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import logging
import model_pb2
from data_models import *
from models.basemodel import AIModel

logger = logging.getLogger("app")

# NOTE: This needs to be defined in the environment this model is running in.
default_headers = {"Ocp-Apim-Subscription-Key": os.environ["OPENAI_API_KEY"]}

model_definition = model_pb2.modelDefinition()
model_definition.needs_text = True
model_definition.needs_image = False
model_definition.can_text = True
model_definition.can_image = False
model_definition.modelID = "o1-mini"


class o1miniAalto(AIModel):
    def get_model_definition(self) -> model_pb2.modelDefinition:
        return model_definition

    def publish_metrics(self, metrics_json: str) -> None:
        logger.info(metrics_json)

    async def get_response(self, message: TaskInput) -> TaskOutput:
        model = ChatOpenAI(
            base_url="https://aalto-openai-apigw.azure-api.net/v1/openai/deployments/o1-mini-2024-09-12/",
            default_headers=default_headers,
        )       
        # ai_messages = message.model_dump()["messages"]
        # for ai_message in ai_messages:
        #     if ai_message["role"] == "system":
        #         ai_message["role"] = "user"                
        # AIresponse = model.invoke(ai_messages)
        # taskResponse = TaskOutput()
        # taskResponse.text = AIresponse.content
        # return taskResponse
        AIresponse = model.invoke(message.model_dump()["messages"])
        taskResponse = TaskOutput()
        taskResponse.text = AIresponse.content
        return taskResponse
