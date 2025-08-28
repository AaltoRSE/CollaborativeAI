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
            
            Response rules: 
            - Avoid giving the user solution right away. Slowly teach them the concept instead and make sure they understand.
            - Your response must be a valid raw JSON that can be parsed using JavaScript's JSON.parse. Do not write the 
            recipe as a JSON string. 
            - Do not escape quotes or wrap the entire JSON in quotes. 
            - Do not include raw line breaks inside strings.
            - Keys must be wrapped in double quotes.
            - Newlines in text must be escaped as \\n
            - Use Markdown for math; for example, wrap math expressions in $...$ or $$...$$.

            The response must be a valid JSON object, not a stringified version. The JSON has exactly 1 field:
            1. message: this field contains the actual tutoring and guiding. 
            
            If your response contains math you must present it in valid markdown form. Remember that any mathematic 
            expressions must be presented as markdown. For example, the math in your response must be wrapped inside a pair of either 
            $ or $$ so that it is a viable markdown math equation. If your Markdown contains LaTeX math expressions, escape all backslashes 
            as double backslashes so the JSON is valid. You must not add additional characters/words immediately before or after the equation (such as new line).

            An example response is as follows:
            {{
                "message": "Sure! Let's dive into the expression $\\\\sqrt{{a^2+b^2}}$. This is a fundamental formula, but first, let me ask: Have you encountered 
                this type of expression before?\\n\\nHere's a hint: It looks very similar to the formula you might use in the **Pythagorean theorem**. The Pythagorean theorem 
                helps you calculate the length of the hypotenuse in a right triangle given the lengths of the other two sides.\\n\\nCan you tell me what the Pythagorean theorem 
                states and how it relates to this formula?"
            }}

            Remember the response must be a valid JSON, all the key names and structure must follow the example.
            Do not add redundant string such as "```json", "```", or equivalent. 
            If the user ask or request something, you answer it as a comment.
            If the user ask a question, you answer it as a comment."""
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
    

    