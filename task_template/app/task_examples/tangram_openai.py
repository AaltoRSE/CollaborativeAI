import json
import logging

from fastapi import HTTPException

from tasks.task_interface import OpenAITask
from routers.router_models import Message
from models import (
    OpenAIBasedDataRequest,
    OpenAIBasedRequest,
    TaskDataRequest,    
    TaskDataResponse,
    ModelResponse,
    TaskRequest,
    TaskRequirements,

)

logger = logging.getLogger(__name__)

count = 0
hardMAX = 3

def get_chat_prompt(objective: str) -> str:
    game_reference = {
        "type": "text", "text":"""Reference Information about the game: 
        You and the human user are playing a tangram game, arranging the pieces to form an objective shape. 
        The pieces are named by their colors: Red, Purple, Yellow, Green, Blue, Cream, and Brown.
        Red and Cream are two large triangles, Yellow and green are two small triangles, Blue is a medium triangle, Purple is a small square, Brown is a tilted parallelogram.
        We consider 0 degrees of rotation the triangles with their hypotenuse facing down, and the square in the square position (so the diamond shape corresponds to 45 degrees of rotation)
        Example logical plays: Matching shapes can allow new larger shapes to appear, uniting two triangles of the same size by their Hypotenuse creates a square of in the location. The Purple Square or a square created of 2 triangles can serve to form many things like heads, bodies, bases of structures. 
        Two triangles can also form a larger triangle when combined.
        """
    }
    chat_prompt = {"type": "text", "text": """You are an AI chatting with a Human Player thats arraging tangram tangram pieces with you and your co-assistents to reach a certain objective. 
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
        """
    }
    objective = {"type": "text", "text": f"Your objetive this game is to form the shape of {objective}"}
    return {"role" : "system", "content":  [game_reference, chat_prompt, objective]}

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

def get_move_piece_message(objective : str) -> Message:
    game_logic = {
        "type": "text",
        "text": """Reference Information about the game: 
        You and the human user are playing a tangram game, arranging the pieces to form an objective shape. 
        The pieces are named by their colors: Red, Purple, Yellow, Green, Blue, Cream, and Brown.
        Red and Cream are two large triangles, Yellow and green are two small triangles, Blue is a medium triangle, Purple is a small square, Brown is a tilted parallelogram.
        We consider 0 degrees of rotation the triangles with their hypotenuse facing down, and the square in the square position (so the diamond shape corresponds to 45 degrees of rotation)
        Example logical plays: Matching shapes can allow new larger shapes to appear, uniting two triangles of the same size by their Hypotenuse creates a square of that size in the location or a diamond (can be used as a circle) shape if the triangles are angled by 45 degrees. The Purple Square or a square created of 2 triangles can serve to form many things like heads, bodies, bases of structures. two triangles can also form a larger triangle when combined by their cathetus green and yellow can usually be used together or to fill similar objectives this could be used to make a another medium sized triangle like blue if used with yellow and green.
        It often makes sense to use pieces of the same shape to furfil similar objectives, for example if theres 2 arms, it makes sense to use similar pieces for each. Maintain friendly, concise dialogue (1-3 sentences). Suggest ideas to progress us towards our objective, collaboratively, not demands. Follow all formatting rules from the prompt.
    
        You and the human user are playing a tangram game, arranging pieces to form an objective shape.  
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
    return game_logic
        
def get_feedback_message(objective: str, game_state: str, hasOverlaps: bool) -> list:

    game_logic = {
        "type": "text",
        "text": (
                """You are adjusting the previous move based on the feedback from an action. 
                Your goal is to adjust the placement of the piece as described by another agent by checking if the image of the board correctly includes the piece in a way that executes the ideia the agent explained.
                
                **Rules for Adjustments:**
                - **Only adjust the piece you moved this turn**—do **not** switch to a different piece.
                - Make **minor changes only** to avoid issues like overlapping or incorrect positioning, you can make bigger changes if its very far from the desired location.
                - when overlaping try to understand from the image what direction would free the piece from the overlap and respect the agents request.
                - Do **not** make more than 5 adjustments unless overlap persists.
                - You can go back to a previous answer if you think it was better and had no overlaps.

                - For the **format**: `PLAY {piece}, {rotation}, {x}, {y}`
                - {rotation} = Rotation in degrees (0, 45, 90, ..., 315)
                - {x}, {y} = Float coordinates from 5 to 95 positive only (100,100 is the top-right corner, so lower values are closer to the bottom and left respectively), you can think of coordenates as percentages of the board aswel 

                **Stopping Condition:**
                - If there is **no overlap** and the move is correct, reply with exactly: `FINISH` (no extra words).
                - Continue refining your move until it has no overlaps.
                - Analyse all the images in previous messages and current without overlaps and choose the imput that caused the best representation of the agents request without overlap, 
                - if you cant find a good solution within **4** atempts, finish with the first non overlaped state you fond, if previous messages had one of these states return to the best previous one found.
                - NEVER EXCEED 8 ATTEMPTS if its past your 8th atempt send a finish.

                *Reason*
                - You should reason what the best thing to do would be so explain your chain of thought like: 
                "The agent was atemppting to place cream left of red, however the rotation is off, I will try to rotate it to 45 degrees and move it to the left by decreasing the first coordenate" followed by the response format.
                
                **Required Output Format:**
                output for adjustments:
                PLAY {piece}, {rotation}, {x}, {y} | {logic}
                output to end:
                "FINISH"  {logic}

                **Example Adjustments:**
                These are sequences of adjustments that could be made to a move, never send more than 1 line at a time.
                In a case where the piece is close but maybe slightly overlapping or slightly off the desired location:


                PLAY Red, 0, 40, 50 | The piece seems to be slightly overlaping with cream, the original prompt wanted it bellow cream and the overlap is only minor on top so we should lower the y coordinate


                PLAY Red, 0, 45, 50 | Red is now too low, the request wanted it just bellow, we should move it up slightly while being careful not to overdo it, 5 units should be enough so 40 + 5 = 45


                PLAY Red, 0, 44, 51 | Red is overlapping by a few pixels at the top, again the original message wanted it bellow so lets lower it just a bit again.


                FINISH  The piece seems to now be correctly placed and not overlapping. i think we are done.  


                In a case where the piece is really far from the desired location:


                PLAY Green, 0, 40, 15 | The agent wanted green near purple to the right, currently i can see in the image that the pieces are on opposite parts of the board, purple is at 15, 15 according to the game state, so lets move green closer to purple but to its right.


                PLAY Green, 0, 30, 15 | From the board i can see that while theres no overlapping, the piece is too far away, lets bring it closer to the left


                PLAY Green, 0, 33, 15 | Green is now overlapping with yellow, moving it slightly right would fix this while staying as loyal to the agents request as possible lets go with 3 units so 30 + 3 = 33


                FINISH  The piece seems correctly placed according to the request.

                In a case the rotation didnt match the request and 0 produces the best result:


                PLAY Green, 45, 30, 30 | Green is placed in requested location, however the current rotation doesnt make it look like a body as requested, lets try rotating it 45 degrees. 


                PLAY Green, 90, 30, 30 | Green is still placed in requested location, however the current rotation is still not making it look like a body as requested by the agent, lets try rotating it another 45 degrees, thus 45 + 45 = 90.


                FINISH  Green now looks like a body and is in the correct are, since it now matches what the agent asked for we are done adjusting.  

                In a case where the piece should be on top but is overlapping:


                PLAY Yellow, 90, 25, 40 | Yellow should be on top of blue, but its currently overlapping with it, from the image the overlap seems small, it was placed at y 45 before so lets decrease 5 units making 40.


                PLAY Yellow, 90, 25, 50 | Looking at the board image the previous adjustment lowered it, since we want it on top this was a mistake, lets revert it back to 45 as it was before and add 5 to properly raise it and avoid overlapping, thus 45 + 5 = 50.


                FINISH  Yellow now seems in the correct spot.

                **Reminder**
                to move left decrease the X coordinate so calculate the current X - amount, to move right increase the X coordinate so calculate the current X + amount
                to move down decrease the Y coordinate so calculate the current Y - amount, to move Up increase the Y coordinate so calculate the current Y + amount
                """
        )
    }

    prompt_text = [
                    {"type": "text", "text": f"Feedback game state: {game_state}"},
                    {"type": "text", "text": f"Are there Overlaps?: {hasOverlaps}, This is the your atempt number {count}"},
                    {"type": "text", "text": f"Objective: {objective}, This is the your atempt number {count}"},
                  ]
                  
    return [game_logic, prompt_text]


class Tangram(OpenAITask):

    def process_model_answer_openAI(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        if "FINISH" in answer.text or "PLAY" in answer.text:
            result = json.dumps(self.parsePlayResponse(answer.text))
            return TaskDataResponse(text=result)

        result =  json.dumps([{"type": "chat", "message": answer.text}])
        return TaskDataResponse(text=result)
        
    def parsePlayResponse(self, response, data=None):
        global count
        # Check if the response indicates no changes are needed
        if "FINISH" in response:#response.strip().split()[0].upper() == "FINISH":
            count=0
            if len(response.strip().split()) > 1: 
                return [{"type": "chat", "message": response.split("FINISH")[1].strip()}, 
                        {"type": "finish", "timestamp": data["timestamp"] if data and "timestamp" in data else ""}]
            return {"type": "finish", "timestamp": data["timestamp"] if data and "timestamp" in data else ""}
        
        try:
         
            # Split into move and message parts
            response = response.split("PLAY")[1].strip()
            lines = response.split("|", 1)
            move_part = lines[0]
            message_part = lines[1] if len(lines) > 1 else False
            parts = [part.strip() for part in move_part.split(",")]
            if len(parts) != 4:
                raise ValueError("Incorrect number of elements in move part.")
            piece, rotation, x, y = parts
            self.randomShape = piece
            res = [{
                "type": "play",
                "shape": piece,
                "position": (float(x), float(y)),
                "rotation": float(rotation),
                "timestamp": data["timestamp"] if data and "timestamp" in data else ""
            }]
            if message_part:
                res.append({"type": "chat", "message": message_part.strip()})
                return res
            
            return res[0]
        except Exception as e:
            print(f"Error parsing play response: {e}, response received: {response}")
            return [{"type": "chat", "message": "Sorry had some trouble playing this turn."}, 
                    {"type": "finish", "timestamp": data["timestamp"] if data and "timestamp" in data else ""}]

    def generate_model_request_openAI(self, request: OpenAIBasedDataRequest) -> OpenAIBasedRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        system_message =""
        message=""
        
        try:
            requests = json.loads(request.inputData)
            if requests and requests["target"]:

                target = requests["target"]
                hasOverlaps = "No" 

                if target == "playRequest":
                    system_message = get_move_piece_message(request.objective)
                    message = requests

                elif target == "playFeedback":
                    global count
                    count+=1

                    for shape in requests["state"]["on_board"]:
                        if len(requests["state"]["on_board"][shape]["collisions"]) > 0:
                            hasOverlaps = "Yes"
                            break

                    if count > hardMAX + 1:

                        count=0
                        system_message = get_feedback_message(request.objective,requests, hasOverlaps)
                        message = "you have exceeded your attempts end your play now by replying FINISH"
                                    
                    else:
                        system_message = get_feedback_message(request.objective,requests, hasOverlaps)
                        message = requests

                elif target == "chatRequest":
                    system_message = get_chat_prompt(request.objective)
                else:
                    logger.error(f"Invalid target {target}")
                    raise HTTPException(400, "Input target type!")
            else:
                logger.error(request)
                raise HTTPException(400, "Input target type!")
        except Exception as e:
            logger.error(e)
            raise HTTPException(400, "Input data invalid!")

        message = [
            {"role" : "system", "content" : json.dumps(system_message)},
            {"role": "user", "content": json.dumps(message)}
        ]

        # This could include an image, but for this task, we currently don't supply one
        return OpenAIBasedRequest(
            messages=message
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=True)

    def is_openai_task(self):
        return True