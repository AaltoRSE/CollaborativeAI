import json
import logging
from http.client import HTTPException
from tasks.task_interface import OpenAITask
from routers.router_models import Message
from models import (
    OpenAIBasedDataRequest,
    OpenAIBasedRequest,
    TaskRequest,
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,
    TaskDataRequest
    )

logger = logging.getLogger(__name__)

def get_chat_prompt(objective: str) -> str:
    game_reference = {
        "type": "text",
        "text": """Reference Information about the game: 
        You and the human user are playing a tangram game, arranging the pieces to form an objective shape. 
        The pieces are named by their colors: Red, Purple, Yellow, Green, Blue, Cream, and Brown.
        Red and Cream are two large triangles, Yellow and green are two small triangles, Blue is a medium triangle, Purple is a small square, Brown is a tilted parallelogram.
        We consider 0 degrees of rotation the triangles with their hypotenuse facing down, and the square in the square position (so the diamond shape corresponds to 45 degrees of rotation)
        Example logical plays: Matching shapes can allow new larger shapes to appear, uniting two triangles of the same size by their Hypotenuse creates a square of in the location. The Purple Square or a square created of 2 triangles can serve to form many things like heads, bodies, bases of structures. 
        Two triangles can also form a larger triangle when combined.
        """,
    }
    chat_prompt = {
        "type": "text",
        "text": """You are an AI chatting with a Human Player thats arraging tangram tangram pieces with you and your co-assistents to reach a certain objective. 
        To answer them, you will have access to the message history, an image of the current board, an image of the current piece drawer where the unplaced pieces lie.
        Your task:
        1. Review what you know about the game state.
        2. Consider the players message and reply logically in an approachable and friendly way.

        Rules:
        - If you suggest moves or plays, always explicity describe how pieces should be placed in relation to each other.
        - If you suggest either the move to create a large square or to create a large triangle, say it explicity. Ex: "Make a big square by using Cream and Red" or "Make a big triangle, placing Red to clockwise direction of Cream"
        - Each individual piece, if present in a suggested move, should have a explicit rotation (except for the moves that form big squares and big triangles).
        - If you disagree with an idea given by the player on how you should approach the challege, try to find a middle ground.
        - If the game already looks finished to you, you can say it looks done.

        Consider the previous messages and keep your message short, at most 1-3 sentences, the objective is a human-like nice short reply.
        Remember you are collaborating so don't order ideias suggest them in a collaborative manner.
        This message may not be the first in the conversation, but u can see the chat history in the previous message.
        Examples:
        - "Hey, well i think we could begin with the tail, using the medium blue triagle for it."
        - "Ok, got it, i'll try to help you achieve that."
        - "Alright I'll try to use the brown piece to create a tail."
        - "I don't think the yellow piece would make a good roof due to it's size, maybe we could use cream for the same objective."
        - "Sounds great, let's begin then!"
        - "I think the game already looks like our objective."
        """,
    }
    objective = {
        "type": "text",
        "text": f"Your objetive this game is to form the shape of {objective}",
    }
    return {"role": "system", "content": [game_reference, chat_prompt, objective]}


def get_move_extraction_prompt(figures_names: str, possible_directions: str) -> str:
    move_extraction_system_prompt = f"""You are currently extracting the first move from a detailed play suggestion by the AI. 
        You must convert that move into one of the following grammars formats: 
        - [PieceToMove], [Direction], [PieceOnBoard], (Optional: [Direction], [PieceOnBoard], ...), [DegreesOfRotation], [FlipXAxis], [FlipYAxis]. 
        Where any piece name is a valid name piece between the names {figures_names}, any direction is one of the following {possible_directions} + ", any rotation degrees value must be 0,45,90,135,180,225,270,315 and any flip value is 0 or 1 (if not mentioned 0).
        This format is the default one, except when special moves for triangle and square creation are suggested.
        - Square [reference piece] [piece to move]
        This format is only used when a suggested move says something along the lines of "Form a Square with" and then two triangle pieces names, note which one is being moved and which one is already in place.
        - Triangle [reference piece] [direction] [piece to move]
        Where direction is either clockwise or anticlockwise.
        This format is only used when a suggested move says something along the lines of "Form a triangle with" and then two triangle pieces names and a direction, note which one is being moved and which one is already in place.
        - Finish: [Message]
        This format is only used when a suggested move says something along the lines of "Looks finished" or something of the type, message should be a friendly message to the human.
        - Rotate [piece to rotate] [rotation]
        This format is only used when a suggested move says something along the lines of "Just rotate" or something of the type, rotation should be the suggested one.
                        
        For example (for each possible grammar): 
        Cream, right, Red, 90, 0, 0. 
        Square Cream Red
        Triangle Cream clockwise Red
            
        You should ONLY RESPOND WITH THE MOVE IN ONE OF THE THREE GRAMMAR FORMATS. 
    """
    return move_extraction_system_prompt


def get_reasoning_prompt() -> str:
    return "You are currently extracting ONLY the reasoning behind the first move from a list of suggested moves. No need for any text beside the reasoning in the response you'll provide."

def get_move_piece_message(objective: str) -> list:

    game_logic = {
        "type": "text",
        "text": """Reference Information about the game: 
        You and the human user are playing a tangram game, arranging the pieces to form an objective shape. 
        The pieces are named by their colors: Red, Purple, Yellow, Green, Blue, Cream, and Brown.
        Red and Cream are two large triangles, Yellow and green are two small triangles, Blue is a medium triangle, Purple is a small square, Brown is a tilted parallelogram.
        We consider 0 degrees of rotation the triangles with their hypotenuse facing down, and the square in the square position (so the diamond shape corresponds to 45 degrees of rotation)
        Example logical plays: Matching shapes can allow new larger shapes to appear, uniting two triangles of the same size by their Hypotenuse creates a square of that size in the location or a diamond (can be used as a circle) shape if the triangles are angled by 45 degrees. The Purple Square or a square created of 2 triangles can serve to form many things like heads, bodies, bases of structures. two triangles can also form a larger triangle when combined by their cathetus green and yellow can usually be used together or to fill similar objectives this could be used to make a another medium sized triangle like blue if used with yellow and green.
        It often makes sense to use pieces of the same shape to furfil similar objectives, for example if theres 2 arms, it makes sense to use similar pieces for each. Maintain friendly, concise dialogue (1-3 sentences). Suggest ideas to progress us towards our objective, collaboratively, not demands. Follow all formatting rules from the prompt.""",
    }

    prompt_text = {"type":  "text", 
                "text" :
                """You and the human user are playing a tangram game, arranging pieces to form an objective shape.
                You will be provided with previous messages to consider past discussions and decisions. as well as a game state and an image of the board. You should ananlyse these to make a logical play move, if you previously said you would do a certain move and its not yet been done, you should perform it.
                Try to undestand what the parts already on the board are representing with the image and how they can be used to form the objective shape.
                Your answer should ideally say what the piece is meant to represent and where you are trying to place it in.
                You can move pieces both on and off the board as well as rotating them to provide better parts.
                \n
                The tangram pieces are:
                - Red: Large Triangle
                - Cream: Large Triangle
                - Yellow: Small Triangle
                - Green: Small Triangle
                - Blue: Medium Triangle
                - Purple: Square
                - Brown: Tilted Parallelogram

                **Rotation Rules:**
                - 0°: Triangles' hypotenuse faces down, thus somewhat like an arrow pointing up; 
                - Square is in a square position at 0°
                - 45°: Square appears as a diamond
                - Rotations must be multiples of 45°

                *Reason*
                - You should reason what the best thing to do would be so explain your chain of thought like: 
                "I can see that purple is already placed and looks like and head, also the user said that red was a good torso, moving red would make sense" followed by the response format.
                - Consider what the pieces current visible in the board look like in our context, and what was previously discussed.
                - Think about how the missing pieces can be used to form missing parts of the objective shape.
                - Consider if you agreed with the player on doing something that wasn't yet been done.

                **Board Coordinates:**
                - X and Y range from **5 to 95** (100,100 is the top-right corner)
                **Required Output Format (One Move Per Line):**
                Exact Format: 
                PLAY {piece}, {rotation}, {x}, {y} | {message}

                Where:
                - {piece} = One of the piece names
                - {rotation} = Rotation in degrees (0, 45, 90, ..., 315)
                - {x}, {y} = Float coordinates from 5 to 95 positive only
                - {message} = Short reasoning (1-3 lines)

                In the ocasion you think the game is finished send the exact format:
                "FINISH" {message}

                **Example Output:**
                PLAY Red, 0, 50, 50 | I'm going to place the red triangle at the center as it could work as a base.
                PLAY Purple, 45, 30, 70 | Maybe the square as a diamond would form a head if placed on top of the body we have been building with the triangles.
                PLAY Green, 45, 30, 70 | I like green as a hat, on top of purple.
                """
        }

    return [game_logic, prompt_text]
        

class Tangram(OpenAITask):
    

    def get_system_prompt(self, objective: str, hasImage: bool = False) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""Your are working with a user to solve some task with a tangram puzzle that consists only of two pieces, a small triangle and a square. 
            The stated task is : {objective}
            In each round, you should select one piece and indicate where you want to place it. 
            You will be provided an image with the current placement of all available pieces, no other pieces are available.py
            You might also get some comment by the user on their move.
            If you decide, that the task is fullfilled, tell the user.
            Be brief in your instruction. Instruct the user one step at a time - move one piece in one turn.
            """
        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(
        self, request: TaskDataRequest
    ) -> TaskDataResponse:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """

        try:
            if request.inputData and request.text:
                target = request.text
                print(target)
                if target == "playFeedback" or target == "playRequest":
                    system_message = get_move_piece_message(request.objective)
                    message = request.inputData

                elif target == "chatRequest":
                    system_message = get_chat_prompt(request.objective)
                    message = request.inputData
                else:
                    logger.error(f"Invalid target {target}")
                    raise HTTPException(400, "Input target type!")
            else:
                logger.error(request)
                raise HTTPException(400, "Input target type!")
        except Exception as e:
            logger.error(e)
            raise HTTPException(400, "Input data invalid!")

        # This could include an image, but for this task, we currently don't supply one

        return TaskRequest(
            text=str(message),
            system=str(system_message),
            image=None,
        )


    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
