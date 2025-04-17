import os
import asyncio
import json
from uuid import uuid4

from grpc_server.queue_handler import QueueHandler
from models import (
    OpenAIBasedDataRequest,
    OpenAIBasedRequest,
    ModelResponse,
    TaskDataResponse,
    TaskRequirements,
)
import grpc_server.tasks_pb2 as grpc_models
from routers.router_models import Message, TextMessage, ImageMessage
from tasks.task import MultiRequestTask


class ExampleTask(MultiRequestTask):
    def __init__(self, queue_handler: QueueHandler):
        self.queue_handler = queue_handler

    def get_system_message_for_first_option(self):
        return Message(role="system", content="Some system message")

    def process_response_to_first_option(self, answer: ModelResponse) -> str:
        # You can do any post-processing here...
        return answer.text

    def create_response_for_second_option(
        self, first_response: ModelResponse, second_response: ModelResponse
    ) -> TaskDataResponse:
        # This can be a lot more complex.
        return TaskDataResponse(text=first_response.text, image=second_response.image)

    def get_requirements(self):
        return TaskRequirements(needs_image=True, needs_text=True)

    async def run_task(self) -> TaskDataResponse:
        self.preprocess()
        if self.target == "FirstOption":
            first_request = OpenAIBasedRequest(
                messages=[
                    self.get_system_message_for_first_option(),
                    Message(role="user", content="Some user message"),
                ]
            )
            messageID = self.submit_request(first_request)
            response = self.process_response_to_first_option(
                await self.wait_for_response(self.session_id, messageID)
            )
            return TaskDataResponse(text=response)
        if self.target == "SecondOption":
            # send one message
            first_request = OpenAIBasedRequest(
                [
                    Message(role="system", content="Some system message"),
                    Message(role="user", content="Some user message"),
                ]
            )
            first_messageID = self.submit_request(first_request)
            second_request = OpenAIBasedRequest(
                [
                    Message(role="system", content="Some other system message"),
                    Message(
                        role="user",
                        content="Some other user message maybe based on the input?",
                    ),
                ]
            )
            # Send two requests concurrently
            second_messageID = self.submit_request(second_request)
            first_response = await self.wait_for_response(
                self.session_id, first_messageID
            )
            second_response = await self.wait_for_response(
                self.session_id, second_messageID
            )

            # we can also send another request and use the answer from the first two for it. and then await the response agaim
            # third_request = OpenAIBasedRequest(
            #     [
            #         Message(role="system", content="Some Third system message"),
            #         Message(
            #             role="user",
            #             content=[
            #                 TextMessage(type="text", text=second_response.text),
            #                 ImageMessage(image_url=first_response.image),
            #             ],
            #         ),
            #     ]
            # )
            # third_messageID = self.submit_request(third_request)
            # third_response = await self.wait_for_response(self.session_id, third_messageID)

            return self.create_response_for_second_option(
                first_response, second_response
            )

    def preprocess(self):
        # This assumes that the input data has a field target, which will be relevant for processing
        self.target = self.task_data.inputData["target"]
