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


class CodeTutor(Task):

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""Imagine yourself as a coding tutor who is teaching a coding concept/problem to a student.
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

            The recipe must be a valid JSON object, not a stringified version. The JSON has exactly 1 field:
            1. message: this field contains the actual tutoring and guiding. 
            
            If your response contains codes, you must present it in valid markdown form. You must not add additional
            characters/words immediately before or after the equation (such as new line).

            An example response is as follows:
            {{
                "message": "Great! Let's start with the basics of graphs in coding. A graph is a data structure that consists 
                of a set of nodes (vertices) and a set of edges connecting pairs of nodes. \\n\\nVertices represent entities and 
                edges represent relationships between these entities.\\n\\nWe can represent graphs in code using various methods. 
                The common representations are:\\n\\n1. **Adjacency Matrix**: A 2D array of size VxV where V is the number of vertices 
                in the graph. A cell in the matrix represents whether there is an edge between the vertices or not.\\n\\n2. **Adjacency 
                List**: An array of lists. The index of the array represents a vertex and the list at that index contains all the adjacent 
                vertices.\\n\\n3. **Edge List**: A list of pairs representing the edges.\\n\\nHere's a question for you: How would you represent 
                the following graph using an adjacency list?\\n\\nVertices: 0, 1, 2\\nEdges: (0-1), (1-2)"
            }}

            Remember the recipe must be a valid JSON, all the key names and structure must follow the example.
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
    

    