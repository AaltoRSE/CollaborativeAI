import logging
from tasks.task_interface import Task
import json
from models import (
    TaskDataRequest,
    TaskRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
)

logger = logging.getLogger(__name__)


class MathTutor(Task):

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""Imagine yourself as a math tutor who is teaching a math concept/problem to a student.
            The user provides the concept/problem they want to learn as follows: {objective}.
            You must make the lesson interactive by asking questions, giving hints, and guide the student in the
            correct path. Avoid giving the answer straight away.
            You will get a message from the user in the form COMMENT_LINE: COMMENT_LINE is the comment made by the user.
            Your response must take the user's comment into consideration.
            Your response must be wrapped inside square brackets, along with additional guidance about the concept/problem.
            If your response contains mathematic equations you must present it in valid markdown form. You must not add additional
            characters/words immediately before or after the equation (such as new line).
            An example of the form of your response is "[<your answer>] <your comment>".
            
            An example response: [Sure! Let's dive into finding the limit of the expression $$frac{{1}}{{1+x}}$$. First, do you know what 
            it means to find the limit of a function as $$x$$ approaches a specific value or infinity?]Understanding limits is crucial 
            in calculus as it helps describe the behavior of functions as they approach certain points or values."

            Do not add redundant string such as "```json", "```", or equivalent. Only add the comment after the answer 
            according to the form above.
            If the user ask or request something, you answer it as a comment."""
        return system_prompt
    
    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        logger.info(request)
        linetag = "COMMENT" if request.inputData["comment"] else "MESSAGE"
        plan = f"Lesson : {json.dumps(request.inputData['messages'])}"
        newplan = f"{linetag} : {request.text}"

        return TaskRequest(
            text=f"{plan} \n{newplan}",
            system=self.get_system_prompt(request.objective),
            image=None,
        )
    
    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
    

    