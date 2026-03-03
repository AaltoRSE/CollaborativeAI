from typing import  List, Annotated
import logging
import json
from datetime import datetime


from fastapi import Depends
from app.schemas.models import (
    TaskDataRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
    OpenAIBasedDataRequest,
    TaskRequest   
)
from app.schemas.api_schemas import APITaskRequest, ModelAnswer
from app.schemas.router_models import (
    ConversationItem,
    TextMessage,
    ImageMessage,
    Message,
    ImageURL,
)
from app.tasks.task import task
from app.tasks.task_interface import Task, OpenAITask
from app.utils.lifecycle import get_httpx_client, httpx

logger = logging.getLogger(__name__)

class CompletionService:
    def __init__(self,
                 httpx_client: Annotated[httpx.AsyncClient, Depends(get_httpx_client)],):        
        self.task : Task | OpenAITask  = task
        self.httpx_client = httpx_client
        logger.info(f"Task set to {self.task}")

    def get_requirements(self) -> TaskRequirements:
        return self.task.get_requirements()

    def build_model_request(
        self, request: TaskDataRequest, history: List[ConversationItem]
    ) -> str:
        # Ask the task to generate the Request
        currentElement : TaskRequest = self.task.generate_model_request(request)        
        # Extend the history by the current request.        
        # Now, convert this into the grpc request
        messages = [Message(role="system", content=currentElement.system)]
        messages.extend([Message(role="user", content=element.content) for element in history])
        currentMessage = Message(role="user", content=[TextMessage(type="text", text=currentElement.text)])

        if currentElement.image:
            currentMessage.content.append(ImageMessage(type="image_url", image_url=ImageURL(url=currentElement.image)))        
        messages.append(currentMessage)        
        # Store it in the history, if this version is used, we do not store images.
        history.append(ConversationItem(role="user", content=currentElement.text))        
        # set the system message
                
        return json.dumps([message.model_dump() for message in messages])        

    def build_model_request_from_open_AI_request(self,request : OpenAIBasedDataRequest) -> str:
        if request.userMessages is not None:
            for message in request.userMessages:
                if message.role == "system":
                    raise ValueError("System messages are not allowed in the openAI request")
                    
        messageRequest = self.task.generate_model_request_openAI(request)
                
        return json.dumps(messageRequest.model_dump()["messages"])

    
    def build_open_AI_response( self, response: ModelAnswer, messageID : str):
            data = ModelResponse.model_validate_json(response.answer)            
            choices = [
                {
                    "index": 0,
                    "logpobs": None,
                    "finish_reason": "stop",
                    "message": {"role": "assistant", "content": data.text},
                }
            ]
            openAIResponse = {
                "id": "chatcmpl-123456",
                "object": "chat.completion",
                # timestamp in ms
                "created": datetime.now().timestamp(),
                "model": "unknown",
                "choices": choices,
                "usage": {
                    "prompt_tokens": 1,
                    "completion_tokens": 1,
                    "total_tokens": 2,
                },
                "system_fingerprint": messageID,
            }
            return openAIResponse
    
    def interpret_model_response_openAI(self, response: ModelAnswer) -> TaskDataResponse:
        """
        This function is used to interpret the model response for the OpenAI model.
        This is for openAI models, which do not store the history on the server.
        """
        # Return an unfiltered data response. This is what comes back from the completions endpoint.
        # That endpoint assumes all processing to be done in the frontend.
        answer = ModelResponse.model_validate_json(response.answer)
        return self.task.process_model_answer_openAI(answer)

    def interpret_model_response(
        self, response: ModelAnswer, history: List[ConversationItem]
    ) -> TaskDataResponse:
        # Load the json
        data = ModelResponse.model_validate_json(response.answer)
        history.append(ConversationItem(role="assistant", content=data.text))
        return self.task.process_model_answer(data)

    async def send_task_request_to_model(self, request : APITaskRequest, history : List[ConversationItem]) -> TaskDataResponse:
        print(self.httpx_client.timeout)
        logger.warning(f"Timeout is set to {self.httpx_client.timeout}")
        httpx_response = await self.httpx_client.post("http://model_handler:8000/model/send_request", json=request.model_dump())
        httpx_response.raise_for_status()
        return self.interpret_model_response(response=ModelAnswer.model_validate(httpx_response.json()), history=history)
    
    async def send_task_request_to_model_openai(self, request : APITaskRequest) -> TaskDataResponse:
        print(self.httpx_client.timeout)
        logger.warning(f"Timeout is set to {self.httpx_client.timeout}")
        httpx_response = await self.httpx_client.post("http://model_handler:8000/model/send_request", json=request.model_dump())
        httpx_response.raise_for_status()
        return self.interpret_model_response_openAI(ModelAnswer.model_validate(httpx_response.json()))