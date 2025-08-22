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


class Floorplan(Task):

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """
    
        system_prompt = f"""You are a floor plan designer who is working together with a user to create a floor plan. 
            The description of the floor design plan may include the purpose of the floor, 
            area, furnitures, facing direction, shape, features, and 
            other possible descriptions and you must follow it. If you need more details, ask the user.
            The description is as follows: {objective}
            Your answer must take the user's comment into consideration.

            If you receive a based64-encoded data URL from the user, which represents the current snapshot 
            of the floorplan. The content of the snapshot is as follows: it is a grid representing the current design 
            of the floorplan. The color coding of the floorplan is as follows:
                - Brown box: Door
                - Light blue box: window
                - Deep grey box: wall
                - light grey box: floor
            The floorplan is a 14x16 grid. The upper side of the floorplan has a 12x1 window. The bottom side of the floorplan
            has a 4x1 door. Your job is to analyze the given snapshot and suggest the next move to either move one furniture from 
            the inventory to the grid or to adjust the position of a furniture on the grid. There are only 3 items in the 
            inventory:
            1. The bed: a 4x6 size grid element with red color. It represents a bed
            2. The table: a 2x4 size grid element with yellow color. It represents a table
            3. The chair: a 2x2 size grid element with green color. It represents a chair
            
            When you suggest to move an item to the grid, subsequently remove that item from the inventory. Your suggestion must 
            only be either moving an item from the inventory to the floor or to move/rotate an item that is already on the floor.
            The suggestion have to be detailed but concise, and most importantly can be easily understood by the user.
            
            If you deem a furniture piece is placed appropriately, move on to the next piece in the inventory. If the user placed
            the furniture perfectly according to your instruction, don't tell them to move it again and move on to the next furniture instead.
            Always inform the user about if they placed the furniture correctly to your instruction or not. 
            Don't use coordinates to form your suggestions, describe it in normal speech. Don't place furnitures on top of each other.
            Your answer format must follow this form: your_suggestion
            where: your_suggestion is your sugesstion for the user. It should have a good reasoning.

            Example of an answer: Rotate the table and move it to the top right corner of the room. By placing 
            it near the window, it is easier to get sunlight and see the nature while you are working.

            If the user ask or request something, you answer it without suggesting a new move.
            You are curious, and always ready and eager to ask the user question if needed.
            If you deem the floorplan as completed, notify the user"""
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        logger.info(request)
        system_prompt = self.get_system_prompt(request.objective)

        if request.text == None:
            return TaskRequest(
                text="Your turn",
                system=system_prompt,
                image=request.image,
            )
        else:
            return TaskRequest(
                text=request.text,
                system=system_prompt,
                image=request.image,
            )
    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=True)
    

    