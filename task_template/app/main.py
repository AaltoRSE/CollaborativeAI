import logging
import logging.config

from fastapi import FastAPI, Request
import secrets
from starlette.middleware.sessions import SessionMiddleware

from app.routers.task_router import task_router


# This will need to be adapted by the individual task!
from app.tasks.task import task 
from app.static_files import SPAStaticFiles
from app.utils.lifecycle import startup

# Set the logger config
logging.config.fileConfig("app/logging.conf", disable_existing_loggers=False)

logger = logging.getLogger("app")
logger.info(f"Starting {task} task")
# Router handling.
app = FastAPI(lifespan=startup)

app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32), max_age=None)
logger.info("Session middleware added")
app.include_router(task_router)


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    path = request.url.path
    method = request.method
    log_message = f"Received request: {method} {path}"
    logger.info(log_message)
    logger.info(request.headers)
    response = await call_next(request)
    return response


# Serve the frontend

app.mount("/", SPAStaticFiles(directory="dist", html=True), name="FrontEnd")
