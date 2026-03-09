from contextlib import asynccontextmanager
import logging
from typing import Any, AsyncGenerator
import asyncio

from fastapi import Request, FastAPI
import httpx

from app.model import ai_model


logger = logging.getLogger("app")

async def get_httpx_client(request : Request) -> httpx.AsyncClient:
    if not hasattr(request.app.state, "httpx_client"):
        request.app.state.httpx_client = httpx.AsyncClient()
    return request.app.state.httpx_client


def init_httpx_async_client(app_instance: FastAPI) -> httpx.AsyncClient:
    """
    Setup function for the httpx client
    """    
    httpx_client = httpx.AsyncClient(timeout=600)
    app_instance.state.httpx_client = httpx_client
    return httpx_client


@asynccontextmanager
async def startup(
    app_instance: FastAPI,
) -> AsyncGenerator[None, Any]:
    """
    Startup function
    """
    # We set a very high timeout here, since there is always
    # the possibility that a model needs to load first, which
    # takes substantial time.
    client = init_httpx_async_client(app_instance)
    # register with the model_handler    
    registered = False
    while not registered:
        logger.info(f"Registering model {ai_model.get_model_definition()} with model handler")
        try:
            response = await client.post(f"http://model_handler:8000/model/register", json=ai_model.get_model_definition().model_dump())
            response.raise_for_status()
            if response.status_code == 200:
                registered = True
        except httpx.RequestError as e:
            # Wait a bit before retrying
            logger.error(f"Error registering model: {e}, retrying in 5 seconds")
            await asyncio.sleep(5)
    logger.info("Model registered successfully")
    yield
    await client.aclose()
    