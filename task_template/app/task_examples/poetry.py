import logging
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

        system_prompt = f"""You are working together with a user to iteratively create a poem. 
            The details of the poem are as follows : {objective}
            Each of you should generate one line in each step.
            You will get a message from the user in the form:
            COMMENT [POEM_LINE] COMMENT: POEM_LINE is the new poem line provided by the user and it is 
            wrapped inside square brackets while the rest (both COMMENT) are comments made by the user.
            Your answer should take the comment and the poem line into consideration and consist of the 
            next line in the poem you want to create.
            Your answer must follow this form: [YOUR_POEM_LINE] [YOUR_COMMENT]
            YOUR_POEM_LINE is the poem line you created, wrapped inside square brackets while YOUR_COMMENT
            is your answer or opinion about the content of COMMENT that the user provided.
            Your answer should not repeat what the user give, or what you have generated before.
            """
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        # This could include an image, but for this task, we currently don't supply one
        logger.info(request)
        return TaskRequest(
            text=f"[POEM_LINE] : {request.text} \n[COMMENT_LINE] : {request.inputData['commentData']}",
            system=self.get_system_prompt(request.objective),
            image=None,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
