
from typing import Annotated
import logging

from fastapi import APIRouter, Depends

from app.services.model_service import ModelService
from app.schemas.api_schemas import  ModelAnswer, ModelRequest

router = APIRouter(prefix="/model", tags=["model"], include_in_schema=False)

logger = logging.getLogger("model")


# This resets the given ser to the default status.
# This is mostly for testing purposes....
@router.post("/request")
async def process_request(
    request_data: ModelRequest,
    model_service: Annotated[ModelService, Depends(ModelService)]
) -> ModelAnswer:
    print("got request")
    response = await model_service.predict(request_data)
    return response