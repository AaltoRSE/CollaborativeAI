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

class Recipe(Task):

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are working together with a user to give instruction for a food/meal recipe. 
            The user provides the recipe they want to make as follows: {objective}
            You will get a message from the user in the form COMMENT_LINE: COMMENT_LINE is the comment made by the user.
            Your answer must take the user's comment into consideration.
            Your recipe must be wrapped inside square brackets, along with some comments about the recipe that 
            you gave: (example: "[<the recipe>] <the comment>").
            The recipe MUST be valid raw JSON that can be parsed using JavaScript's JSON.parse. Do not write the recipe as a 
            JSON string. DO NOT escape quotes or wrap the entire JSON in quotes. The recipe must be a valid JSON object, not a stringified version.
            The field of the JSON must have the following, word-by-word: name, ingredients, instruction, servings, prep_time, cook_time, total_time
            The JSON must follows this example, each fields have to be followed word by word:
            {{
              "name": "Spaghetti Bolognese",
              "ingredients:
                  {{
                    "Olive oil": "2 tbsp",
                    "Onion": "1, finely chopped",
                    "Garlic": "2 cloves, minced",
                    "Carrot": "1, finely chopped",
                    "Celery": "1 stalk, finely chopped",
                    "Ground beef": "500g",
                    "Tomato paste": "2 tbsp",
                    "Canned tomatoes": "400g, crushed",
                    "Beef broth": "250ml",
                    "Red wine": "125ml (optional)",
                    "Dried oregano": "1 tsp",
                    "Dried basil": "1 tsp",
                    "Salt": "to taste",
                    "Black pepper": "to taste",
                    "Bay leaf": "1",
                    "Milk": "100ml",
                    "Spaghetti": "400g",
                    "Parmesan cheese": "to serve",
                    "Fresh basil": "to garnish"
                  }},
              "instruction":
                  {{
                      "0": "Heat olive oil in a large pan over medium heat.",
                      "1": "Add onion, garlic, carrot, and celery. Sauté until softened.",
                      "2": "Increase heat, add ground beef, and cook until browned.",
                      "3": "Stir in tomato paste, then add canned tomatoes, beef broth, red wine (if using), oregano, basil, salt, pepper, and bay leaf.",
                      "4": "Reduce heat and let simmer for at least 30 minutes, stirring occasionally.",
                      "5": "Add milk and stir well. Simmer for another 10-15 minutes.",
                      "6": "Meanwhile, cook spaghetti according to package instructions. Drain well.",
                      "7": "Remove bay leaf from the sauce and discard.",
                      "8": "Serve sauce over spaghetti, topped with grated Parmesan and fresh basil."
                  }}
              "servings": "4",
              "prep_time": "15 minutes",
              "cook_time": "45 minutes",
              "total_time": "1 hour"
            }}
            Remember the recipe must be a valid JSON, all the key names and structure must follow the example, 
            wrapped inside squared brackets, follows by the comment.
            Do not add redundant string such as "```json", "```", or equivalent. Do not include markdown, or code blocks. 
            If the user ask or request something, you answer it as a comment.
            You are curious, and always ready and eager to ask the user question if needed."""
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        logger.info(request)
        linetag = "COMMENT" if request.inputData["comment"] else "NEWRECIPE"
        plan = f"RECIPES : {json.dumps(request.inputData['recipes'])}"
        newplan = f"{linetag} : {request.text}"

        return TaskRequest(
            text=f"{plan} \n{newplan}",
            system=self.get_system_prompt(request.objective),
            image=None,
        )
    
    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
    

    