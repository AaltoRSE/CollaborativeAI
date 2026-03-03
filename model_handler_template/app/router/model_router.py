
from typing import Annotated, List
import logging

from fastapi import APIRouter, Request, Security, HTTPException, status, Depends

from app.services.model_service import ModelService
from app.schemas.api_schemas import ModelDefinition, ModelAnswer, TaskRequest
from app.services.session_service import SessionService


router = APIRouter(prefix="/model", tags=["model"])

logger = logging.getLogger("model")


# This resets the given ser to the default status.
# This is mostly for testing purposes....
@router.post("/send_request")
async def send_request(
    request_data: TaskRequest,
    model_service: Annotated[ModelService, Depends(ModelService)],
    session_service: Annotated[SessionService, Depends(SessionService)],
) -> ModelAnswer:    
    model_id = await session_service.get_model_for_session(request_data.sessionID)
    if not model_id:
        raise HTTPException(404, "Session not found or no model assigned")    
    response = await model_service.forward_request(model_id, request_data)
    print(response)
    return response

@router.post("/register")
def register_model(
    model_register: ModelDefinition,
    model_service: Annotated[ModelService, Depends(ModelService)],    
):
    print("Registering model")
    model_service.registerModel(model_register)
    return {}



