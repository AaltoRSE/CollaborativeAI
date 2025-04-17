import os
import asyncio
import json
from uuid import uuid4

from grpc_server.queue_handler import QueueHandler
from models import (
    OpenAIBasedDataRequest,
    OpenAIBasedRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
)
import grpc_server.tasks_pb2 as grpc_models


class MultiRequestTask:
    def __init__(self, queue_handler: QueueHandler, task_handler):
        self.queue_handler = queue_handler

    async def start_request(self, task_data: OpenAIBasedDataRequest, sessionID: str):
        self.task_data: OpenAIBasedDataRequest = task_data
        self.session_id = sessionID
        return await self.run_task()

    async def wait_for_response(self, sessionID, messageID) -> ModelResponse:
        while True:
            answer = self.queue_handler.get_answer(sessionID, messageID)
            if answer == None:
                self.queue_handler.process_queue(sessionID)
                await asyncio.sleep(1)
            else:
                return ModelResponse.model_validate_json(answer.answer)

    def submit_request(self, messageRequest: OpenAIBasedRequest):
        messageID = str(uuid4())
        grpc_taskRequest = grpc_models.taskRequest()
        grpc_taskRequest.request = json.dumps(messageRequest.model_dump()["messages"])
        grpc_taskRequest.messageID = messageID
        grpc_taskRequest.sessionID = self.sessionID
        # Submit the reques to the queue.
        self.queue_handler.put(grpc_taskRequest)
        return messageID

    async def run_task(self) -> TaskDataResponse:
        raise NotImplementedError()

    def get_requirements(self) -> TaskRequirements:
        raise NotImplementedError()
