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


class Poetry(Task):

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        #First you ask, the user what the poem's theme is by asking "What is the theme of your poem?"
        system_prompt = f"""You are working together with a user to iteratively create a poem. 
            The details of the poem are as follows : {objective}
            Each of you should generate one line in each step.
            You will get a message from the user in the form:
            [POEM_LINE] : the user poem line
            [COMMENT_LINE] : the user comment on the poem up till now
            The comment line can be empty
            Your answer should take the comment line and the poem line into consideration and consist and consist of the next line in the poem you want to create.
            Your anser should only be the poem line you created. Do not include the text '[POEM_LINE]' or '[COMMENT_LINE]' into your answer.
            Your answer should not repeat what the user give, or what you have generated before.
            """
        # system_prompt = f"""You are working together with a user to solve a math problem. 
        #     The details of the problem are as follows : {objective}
        #     """
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        # This could include an image, but for this task, we currently don't supply one
        return TaskRequest(
            text=f"[POEM_LINE] : {request.text} \n[COMMENT_LINE] : {request.inputData['commentData']}",
            system=self.get_system_prompt(request.objective),
            image=None,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
