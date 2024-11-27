from fastapi import APIRouter, Depends, Request
from models import (
    TaskDataRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
    TaskMetrics,   
    TaskRequest         
)
from routers.router_models import (
    ConversationItem,    
    SessionData,
    OpenAIChatBaseModel
    
)
from routers.session import get_session, clear_session
from typing import Dict, List
from tasks.task_interface import Task
import asyncio
import logging
from grpc_server.queue_handler import queue_handler
import grpc_server.tasks_pb2 as grpc_models
from datetime import datetime

logger = logging.getLogger(__name__)
task_router = APIRouter(prefix="/api/v1/task")


class TaskRouter:
    def _init__(self):
        pass

    def set_Task(self, task: Task):
        self.task = task

    def get_requirements(self) -> TaskRequirements:
        return self.task.get_requirements()

    def build_model_request(
        self, request: TaskDataRequest, history: List[ConversationItem]
    ) -> grpc_models.taskRequest:
        currentElement = self.task.generate_model_request(request)
        grpc_taskRequest = grpc_models.taskRequest()
        # Extend the history by the current request.
        logger.info(currentElement.text)        
        current
        # Now, we convert this into the taskRequest
        currentRequestObject = TaskRequest(
            text=history, image=currentElement.image, system=currentElement.system
        )
        history.append(ConversationItem(role="user", content=currentElement.text))
        grpc_taskRequest.request = currentRequestObject.model_dump_json()
        return grpc_taskRequest

    def interpret_model_response(
        self, response: grpc_models.modelAnswer, history: List[ConversationItem]
    ) -> TaskDataResponse:
        # Load the json
        logger.info(response)
        logger.info(response.answer)
        data = ModelResponse.model_validate_json(response.answer)
        history.append({"role": "assistant", "content": data.text})
        return self.task.process_model_answer(data)


task_handler = TaskRouter()

from uuid import uuid4


@task_router.post("/completions")
async def chat_completion_endpoint(
    task_data: OpenAIChatBaseModel, session: SessionData = Depends(get_session)
):
    """Generate prompt endpoint:
    process pieces' data and plug them into the prompt
    """
    sessionID = session.id
    messageID = str(uuid4())
    task_props = task_handler.get_requirements()
    startRequest = grpc_models.modelRequirements()
    startRequest.sessionID = sessionID
    # Since we don't know, this will only work with models,
    # that can use text and images.
    startRequest.needs_text = True
    startRequest.needs_image = True
    logger.info(startRequest)
    if not sessionID in queue_handler.response_queues:
        queue_handler.start_queue.put(startRequest)

    # Wait for the response queue to be created
    while not sessionID in queue_handler.response_queues:
        await asyncio.sleep(1)
    # Submit the task to the model
    logger.info("Task started, submitting to model")

    # get the messages that have a role of system from the task_data
    system_messages = [
        message for message in task_data.messages if message.role == "system"
    ]
    converted_task_data = TaskDataRequest(
        text="", image=None, objective="", inputData=None
    )
    converted_task_data.objective = system_messages[0].content
    # get the last message
    last_message = task_data.messages[-1]
    #Convert the messages array into ConversationItems for our framework. 
    #We will not supplement with history apart from whats supplied here
    data = []
    for message in task_data.messages[:-1]:
        role = message.role
        for element in message.content:
            if message.content.type == "text":
                data.append(
                    ConversationItem(role=message.role, content=message.content.text)
                )
            elif message.content.type == "image":
                data.append(
                    ConversationItem(role=message.role, content=message.content.image_url)
                )
            # Currently, we cannot handle audio.


    text_messages = [
        ConversationItem(content=message, role=last_message.role)
        for message in last_message.content
        if message.type == "text"
    ]
    # we simply combine everything with newlines...
    converted_task_data.text = "\n".join([message.text for message in text_messages])
    image_messages = [
        message for message in last_message.content if message.type == "image"
    ]
    if len(image_messages) > 0:
        converted_task_data.image = image_messages[0].url
    history = []
     
    model_request = task_handler.build_model_request(converted_task_data, history)
    # Add the session ID to the model request
    model_request.sessionID = sessionID
    model_request.messageID = messageID
    queue_handler.task_queue.put(model_request)
    logger.info("Submitted, awaiting response")
    # And wait for the response to arrive:
    while True:
        answer = queue_handler.get_answer(sessionID, messageID)
        if answer == None:
            queue_handler.process_queue(sessionID)
            await asyncio.sleep(1)
        else:
            logger.info("Supplying response")
            update = task_handler.interpret_model_response(answer, history)
            choices = [
                {
                    "index": 0,
                    "logpobs": None,
                    "finish_reason": "stop",
                    "message": {"role": "assistant", "content": update.text},
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


@task_router.post("/process")
async def process_task_data(
    task_data: TaskDataRequest, session: SessionData = Depends(get_session)
):
    """Generate prompt endpoint:
    process pieces' data and plug them into the prompt
    """
    history = session.history
    sessionID = session.id
    messageID = str(uuid4())
    task_props = task_handler.get_requirements()
    startRequest = grpc_models.modelRequirements()
    startRequest.sessionID = sessionID
    startRequest.needs_text = task_props.needs_text
    startRequest.needs_image = task_props.needs_image
    logger.info(startRequest)
    if not sessionID in queue_handler.response_queues:
        queue_handler.start_queue.put(startRequest)

    # Wait for the response queue to be created
    while not sessionID in queue_handler.response_queues:
        await asyncio.sleep(1)
    # Submit the task to the model
    logger.info("Task started, submitting to model")
    model_request = task_handler.build_model_request(task_data, history)
    # Add the session ID to the model request
    model_request.sessionID = sessionID
    model_request.messageID = messageID
    queue_handler.task_queue.put(model_request)
    logger.info("Submitted, awaiting response")
    # And wait for the response to arrive:
    while True:
        answer = queue_handler.get_answer(sessionID, messageID)
        if answer == None:
            queue_handler.process_queue(sessionID)
            await asyncio.sleep(1)
        else:
            logger.info("Supplying response")
            update = task_handler.interpret_model_response(answer, history)
            return update


@task_router.post("/finish")
async def finish(
    source_request: Request,
    request: TaskMetrics,
    session: SessionData = Depends(get_session),
):
    """Finish task endpoint:
    delete the session based on the session_id cookie when the user decides
    their task is done
    """
    finishObj = {"sessionID": session.id, "metrics": str(request.metrics)}
    queue_handler.finish_queue.put(finishObj)
    clear_session(source_request)
    return {"response": "session cleared"}
