from typing import Annotated
import asyncio
import logging
import json

from fastapi import APIRouter, Depends, Request
import httpx

from app.schemas.api_schemas import APITaskRequest, APITaskMetrics, ModelInfo
from app.schemas.models import (
    TaskDataRequest,
    TaskDataResponse,
    TaskMetrics,
    OpenAIBasedDataRequest,
)

from app.utils.lifecycle import get_httpx_client
from app.services.completion_service import CompletionService
from app.services.session_service import SessionService

logger = logging.getLogger(__name__)
task_router = APIRouter(prefix="/api/v1/task")



@task_router.post("/completions")
async def chat_completion_endpoint(
    request: Request,
    task_data: OpenAIBasedDataRequest,
    task_handler: Annotated[CompletionService, Depends(CompletionService)],
    session_service: Annotated[SessionService, Depends(SessionService)],
) -> TaskDataResponse:
    """
    More "openAI" like endpoint, which takes a set of messages along with additional input data.
    NOTE: the Messages are not allowed to contain a SYSTEM message, as the system message has to be added
    during task processing IN the server as to not allow free use of an endpoint for general chatting!
    """
    session_id = await session_service.get_session(request)
    # Submit the task to the model
    logger.info("Task started, submitting to model")

    # get the messages that have a role of system from the task_data
    model_request = task_handler.build_model_request_from_open_AI_request(task_data)
    # Add the session ID to the model request
    return await task_handler.send_task_request_to_model_openai(APITaskRequest(request=model_request, sessionID=session_id))


@task_router.post("/process")
async def process_task_data(
    request: Request,
    task_data: TaskDataRequest,
    task_handler: Annotated[CompletionService, Depends(CompletionService)],
    session_service: Annotated[SessionService, Depends(SessionService)],
) -> TaskDataResponse:
    """Generate prompt endpoint:
    process pieces' data and plug them into the prompt
    """
    session = await session_service.get_session(request)
    history = session.history
    sessionID = session.id        
    # Submit the task to the model
    logger.info("Task started, submitting to model")
    model_request = task_handler.build_model_request(task_data, history)    
    # Add the session ID to the model request
    task_request = APITaskRequest(request=model_request, sessionID=sessionID)    
    return await task_handler.send_task_request_to_model(task_request, history)    


@task_router.post("/finish")
async def finish(
    source_request: Request,
    request: TaskMetrics,
    session_service: Annotated[SessionService, Depends(SessionService)],
    httpx_client: Annotated[httpx.AsyncClient, Depends(get_httpx_client)],
):
    """Finish task endpoint:
    delete the session based on the session_id cookie when the user decides
    their task is done
    """
    session = await session_service.get_session(source_request)    
    finishObj = APITaskMetrics(sessionID=session.id, metrics=json.dumps(request.metrics))
    response = await httpx_client.post("http://model_handler:8000/session/endTask", json=finishObj.model_dump())
    model_info = ModelInfo.model_validate(response.json())
    session_service.clear_session(session.id)
    return {"modelInfo": model_info.model_name}
