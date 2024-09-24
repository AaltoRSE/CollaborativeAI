import logging
import tasks.tangram_models as tangram_models
from typing import Any, List
import json
from tasks.task_interface import Task
from models import (
    TaskDataRequest,
    TaskRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
)

logger = logging.getLogger(__name__)


class Gesture(Task):

    def get_system_prompt(self) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = open("/usr/project/task_examples/gesture_prompt.txt", "r").read()
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        logger.info(request)
        # This could include an image, but for this task, we currently don't supply one
        return TaskRequest(
            text=request.text,
            system=self.get_system_prompt(),
            image=None,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
