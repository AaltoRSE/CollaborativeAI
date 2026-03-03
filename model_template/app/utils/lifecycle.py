from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from app.model import ai_model
from fastapi import Request, FastAPI
import httpx


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
    print(f"Registering model {ai_model.get_model_definition()} with model handler")
    await client.post(f"http://model_handler:8000/model/register", json=ai_model.get_model_definition().model_dump())    
    yield
    await client.aclose()
    