import logging

from fastapi import HTTPException

from tasks.task_interface import OpenAITask
from routers.router_models import Message
from models import (
    OpenAIBasedDataRequest,
    OpenAIBasedRequest,    
    TaskDataResponse,
    ModelResponse,
    TaskRequirements,

)

logger = logging.getLogger(__name__)

<<<<<<< Updated upstream

def get_chat_prompt(objective : str) -> str :
=======
count = 0
hardMAX = 3

def get_chat_prompt(objective: str) -> str:
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream

def get_move_extraction_prompt(figures_names: str, possible_directions : str) -> str:
=======
def get_move_extraction_prompt(figures_names: str, possible_directions: str) -> str:
>>>>>>> Stashed changes
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

    game_logic = {"type": "text", "text":"""Reference Information about the game: 
        You and the human user are playing a tangram game, arranging the pieces to form an objective shape. 
        The pieces are named by their colors: Red, Purple, Yellow, Green, Blue, Cream, and Brown.
        Red and Cream are two large triangles, Yellow and green are two small triangles, Blue is a medium triangle, Purple is a small square, Brown is a tilted parallelogram.
        We consider 0 degrees of rotation the triangles with their hypotenuse facing down, and the square in the square position (so the diamond shape corresponds to 45 degrees of rotation)
        Example logical plays: Matching shapes can allow new larger shapes to appear, uniting two triangles of the same size by their Hypotenuse creates a square of that size in the location or a diamond (can be used as a circle) shape if the triangles are angled by 45 degrees. The Purple Square or a square created of 2 triangles can serve to form many things like heads, bodies, bases of structures. two triangles can also form a larger triangle when combined by their cathetus green and yellow can usually be used together or to fill similar objectives this could be used to make a another medium sized triangle like blue if used with yellow and green.
        It often makes sense to use pieces of the same shape to furfil similar objectives, for example if theres 2 arms, it makes sense to use similar pieces for each.
        """}

    prompt_text = f"""You are an AI-Player helping the Human Player arrange Tangram Pieces in a board in order to create {objective}. 
		A move involves moving one of the tangram pieces on the board or placing a piece on the board from the piece drawer. 

		NEVER use a piece in the drawer as a reference in any of the following
		
		You will receive the current game state in an image format, an image showing the state of the piece drawer, 
		a dictionary specifying the current rotation value of each piece, the full chat history between you (you're the AI) and the player 
		and an history of all played moves, by the player and the AI.  

		After analysing the given image of the state you should suggest your moves in one of the following ways:
		
		You can describe a relative position, done in relation to pieces already placed on the board by indicating which side 
		(right, left, top, bottom, top-right, top-left, bottom-right, bottom-left) of them the piece to be moved should be placed. 
		A move can be done in relation to a reference piece or more.
		You can rotate a piece rotate in a move, always try to describe move rotation in terms of explicit degrees to add, 
		avoid using phrases which require deducting or interpreting the rotation values.
		Example: Place Red to the left of Cream with a 90º rotation.
		This is your main way to play, you should only use the next ones if they match exactly what you consider the best move.
		
		You can suggest to make a Square/diamond shape using a pair of triangles. By moving one of them to next to one already on the board.
		The triangle pair must consist of Cream and Red OR Green and Yellow, since these match in size.
		Whenever suggesting a square creation move, you need to say "Form a Square" and then the triangle that needs to be placed followed by the referenced triangle.
		Example: Form a Square by putting Cream next to Red (note, here red the one that MUST be already on the board, we would be moving cream, you can make this more clear in your replies)
		
		You can suggest to make a larger Triangle by using a pair of smaller triangles. One of them must already be on the board for the move to be valid.
		Since this move leads to two possible positions and may be applied on different orientations, you must indicate if the triangle is placed clockwise or anticlockwise from the reference triangle.
		The triangle pair must also consist of Cream and Red OR Green and Yellow.
		Whenever suggesting a triangle creation move, you need to say "Form a Triangle by placing" and then the triangle piece name to be placed, followed by clockwise or anticlockwise, and then the reference triangle piece name.
		Example: Form a Triangle by placing Cream anticlockwise from Red

		You can simply rotate a piece without moving it, "Just rotate" and then the piece and the rotation you intend for it to have.
		Example: Just rotate Blue 90

		If and only if you believe the objective has already been achieved, that is if you think it looks close enough to the objective then say "Looks finished" followed by a small friendly message to the human player.
		Example: Looks finished: I think this already resembles our objective well. Do you agree?
		
		KEEP IN MIND THE PLAY YOU SHOULD MAKE THE MOST IS THE RELATIVE MOVE
		
		You should always follow the commands and reasoning in the chat history behind the user and the AI. 
		ALWAYS check and respect if you promised something in a recent previous message that wasnt been done yet.
		User commands prevail above AI commands, in case they conflict, as well as newest messages above older ones. 
		Following the chat instructions and considering the state of the game, 
		list all moves that should be done in order to create {objective}, providing explanations for each one."""
    
    system_message = {"role" : "system", "content":  [game_logic, { "type": "text", "text" : prompt_text} ]}
    return system_message
        
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
                {logic}
                PLAY {piece}, {rotation}, {x}, {y}
                output to end:
                "FINISH"

                **Example Adjustments:**
                These are sequences of adjustments that could be made to a move, never send more than 1 line at a time.
                In a case where the piece is close but maybe slightly overlapping or slightly off the desired location:

                The piece seems to be slightly overlaping with cream, the original prompt wanted it bellow cream and the overlap is only minor on top so we should lower the y coordinate
                PLAY Red, 0, 40, 50

                Red is now too low, the request wanted it just bellow, we should move it up slightly while being careful not to overdo it, 5 units should be enough so 40 + 5 = 45
                PLAY Red, 0, 45, 50

                Red is overlapping by a few pixels at the top, again the original message wanted it bellow so lets lower it just a bit again.
                PLAY Red, 0, 44, 51

                The piece seems to now be correctly placed and not overlapping. i think we are done.
                FINISH


                In a case where the piece is really far from the desired location:

                The agent wanted green near purple to the right, currently i can see in the image that the pieces are on opposite parts of the board, purple is at 15, 15 according to the game state, so lets move green closer to purple but to its right.
                PLAY Green, 0, 40, 15

                From the board i can see that while theres no overlapping, the piece is too far away, lets bring it closer to the left
                PLAY Green, 0, 30, 15

                Green is now overlapping with yellow, moving it slightly right would fix this while staying as loyal to the agents request as possible lets go with 3 units so 30 + 3 = 33
                PLAY Green, 0, 33, 15
                
                The piece seems correctly placed according to the request.
                FINISH

                In a case the rotation didnt match the request and 0 produces the best result:

                Green is placed in requested location, however the current rotation doesnt make it look like a body as requested, lets try rotating it 45 degrees.
                PLAY Green, 45, 30, 30

                Green is still placed in requested location, however the current rotation is still not making it look like a body as requested by the agent, lets try rotating it another 45 degrees, thus 45 + 45 = 90.
                PLAY Green, 90, 30, 30
                
                Green now looks like a body and is in the correct are, since it now matches what the agent asked for we are done adjusting.
                FINISH

                In a case where the piece should be on top but is overlapping:

                Yellow should be on top of blue, but its currently overlapping with it, from the image the overlap seems small, it was placed at y 45 before so lets decrease 5 units making 40.
                PLAY Yellow, 90, 25, 40

                Looking at the board image the previous adjustment lowered it, since we want it on top this was a mistake, lets revert it back to 45 as it was before and add 5 to properly raise it and avoid overlapping, thus 45 + 5 = 50.
                PLAY Yellow, 90, 25, 50

                Yellow now seems in the correct spot.
                FINISH

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
<<<<<<< Updated upstream
        try:
            if request.inputData and request.inputData["target"]:
                target = request.inputData["target"]
                if target == "ai_move":
                    system_message = get_move_piece_message(request.objective)
                elif target == "extract_move":
                    system_message = { "role" : "system", "content" : get_move_extraction_prompt(request.inputData["figures_names"], request.inputData["possible_directions"]) }
                elif target == "get_reasoning":
                    system_message = { "role" : "system", "content" : get_reasoning_prompt() }
                elif target == "chat":
=======
        system_message =""
        message=""

        try:
            if request.inputData and request.text:

                target = request.text
                hasOverlaps = "No" 

                if target == "playRequest":
                    system_message = get_move_piece_message(request.objective)
                    message = request.inputData

                elif target == "playFeedback":
                    global count
                    count+=1
                    for shape in request.inputData["state"]["on_board"]:
                        if len(request.inputData["state"]["on_board"][shape]["collisions"]) > 0:
                            hasOverlaps = "Yes"
                            break

                    if count > hardMAX + 1:
                        count=0
                        system_message = get_feedback_message(request.objective,request.inputData, hasOverlaps)
                        message = "you have exceeded your attempts end your play now by replying FINISH"
                                    
                    else:
                        system_message = get_feedback_message(request.objective,request.inputData, hasOverlaps)
                        message = request.inputData

                elif target == "chatRequest":
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
        messages = [system_message]
        messages.extend(request.userMessages)
        return OpenAIBasedRequest(messages=messages)
        
=======
        # This could include an image, but for this task, we currently don't supply one
        return TaskRequest(
            text=str(message),
            system=str(system_message),
            image=None,
        )

>>>>>>> Stashed changes

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=True)
