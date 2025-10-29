import ast
import json
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import model_pb2
from data_models import TaskInput, TaskOutput
from models.basemodel import AIModel

default_headers = {"Ocp-Apim-Subscription-Key": os.environ["OPENAI_API_KEY"]}
base_url = (
    "https://aalto-openai-apigw.azure-api.net/v1/openai/deployments/o3-mini-2025-01-31/",
)


logger = logging.getLogger("app")

model_definition = model_pb2.modelDefinition()
model_definition.needs_text = True
model_definition.needs_image = False
model_definition.can_text = True
model_definition.can_image = True
model_definition.modelID = "TangramAgent-o3-mini"


class ChatAgent:
    def __init__(self, model):
        super().__init__()
        self.chatLog = []
        self.model = model
        self.temperature = 0.7
        self.max_tokens = 1024
        self.historyLimit = 20
        self.client = ChatOpenAI(
            base_url=base_url,
            default_headers=default_headers,
        )
        # Initial system message for chat
        self.chatLog.append(
            {
                "role": "system",
                "content": """You and the human user are playing a tangram game, arranging the pieces to form an objective shape. 
            The pieces are named by their colors: Red, Purple, Yellow, Green, Blue, Cream, and Brown.
            Red and Cream are two large triangles, Yellow and green are two small triangles, Blue is a medium triangle, Purple is a small square, Brown is a tilted parallelogram.
            We consider 0 degrees of rotation the triangles with their hypotenuse facing down, and the square in the square position (so the diamond shape corresponds to 45 degrees of rotation)
            Example logical plays: Matching shapes can allow new larger shapes to appear, uniting two triangles of the same size by their Hypotenuse creates a square of that size in the location or a diamond (can be used as a circle) shape if the triangles are angled by 45 degrees. The Purple Square or a square created of 2 triangles can serve to form many things like heads, bodies, bases of structures. two triangles can also form a larger triangle when combined by their cathetus green and yellow can usually be used together or to fill similar objectives this could be used to make a another medium sized triangle like blue if used with yellow and green.
            It often makes sense to use pieces of the same shape to furfil similar objectives, for example if theres 2 arms, it makes sense to use similar pieces for each. Maintain friendly, concise dialogue (1-3 sentences). Suggest ideas to progress us towards our objective, collaboratively, not demands. Follow all formatting rules from the prompt.""",
            }
        )

    async def handleChat(self, objective, game_state, user_msg, board_img, drawer_img):
        messages = self.chatLog[-self.historyLimit :]
        user_message = await self.makeChatMessage(
            objective, game_state, user_msg, board_img
        )
        messages.append(user_message)

        try:
            response = self.client.invoke(messages[-1]["content"][-1]["text"])

        except Exception as e:
            print(f"OpenAI API error in handleChat: {e}")
            return "I'm having trouble responding right now."

        assistant_message = response.content
        self.chatLog.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    async def makeChatMessage(self, objective, game_state, user_msg, board_img):
        return {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Objective: {objective}"},
                {"type": "text", "text": f"Game State: {game_state}"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{board_img}"},
                },
                {
                    "type": "text",
                    "text": f"The message you are replying to: {user_msg}",
                },
            ],
        }


class PlayAgent:
    def __init__(self, chat_agent, model):
        super().__init__()
        self.model = model
        self.temperature = 0.7
        self.max_tokens = 1024
        self.client = ChatOpenAI(
            base_url=base_url,
            default_headers=default_headers,
        )
        self.chat_agent = chat_agent
        self.last_play_context = []
        # System message for play decisions
        self.play_system_message = {
            "role": "system",
            "content": (
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
            ),
        }

    async def generatePlay(self, objective, game_state, board_img, drawer_img):
        context = [
            self.play_system_message,
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Objective: {objective}.\nGame State: {game_state}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{board_img}"},
                    },
                ],
            },
        ]

        try:
            mgs = TaskInput(messages=self.chat_agent.chatLog + context)

            response = self.client.invoke(mgs.model_dump()["messages"])

        except Exception as e:
            print(f"OpenAI API error in generatePlay: {e}")
            return "Error generating play move."

        assistant_content = response.content
        # Update last_play_context for feedback (retain context without altering feedback later)
        self.last_play_context = [
            {"role": "assistant", "content": "The agent said: " + assistant_content}
        ]
        self.chat_agent.chatLog.append(
            {"role": "assistant", "content": assistant_content.split("PLAY")[0].strip()}
        )
        return assistant_content


class FeedbackAgent:
    def __init__(self, play_agent, model):
        super().__init__()
        self.model = model
        self.temperature = 0.7
        self.max_tokens = 256
        self.client = ChatOpenAI(
            base_url=base_url,
            default_headers=default_headers,
        )
        self.playAgent = play_agent
        self.memory = []
        self.count = 0
        self.hardMAX = 10
        self.latestValid = ""
        # System message for adjustments
        self.system_message = {
            "role": "system",
            "content": (
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
            ),
        }

    async def adjustPlay(self, game_state, board_img, hasOverlaps="No"):
        self.count += 1
        # Determine if there are any collisions in the game state
        for shape in game_state["on_board"]:
            if len(game_state["on_board"][shape]["collisions"]) > 0:
                hasOverlaps = "Yes"
                break

        if hasOverlaps == "No" and len(self.memory) > 0:
            self.latestValid = self.memory[-1]["content"]
        if self.count > self.hardMAX + 1:
            print("forcing finish")
            return "FINISH"
        if self.count > self.hardMAX:
            print("forcing return")
            return self.latestValid

        messages = [msg for msg in self.playAgent.last_play_context]
        messages += self.memory
        messages.append(self.system_message)
        adjustData = {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Feedback game state: {game_state}"},
                {
                    "type": "text",
                    "text": f"Are there Overlaps?: {hasOverlaps}, This is the your atempt number {self.count}",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{board_img}"},
                },
            ],
        }
        messages.append(adjustData)
        try:
            response = self.client.invoke(messages)

        except Exception as e:
            print(f"OpenAI API error in adjustPlay: {e}")
            return "Error adjusting play move."

        assistant_content = response.content
        self.memory.append(adjustData)
        self.memory.append({"role": "assistant", "content": assistant_content})
        messages.append({"role": "assistant", "content": assistant_content})

        if "FINISH" in assistant_content:
            self.count = 0
            self.memory = []
        return assistant_content


class CustomAgent(AIModel):
    def __init__(self):
        super().__init__()
        self.model = "gpt-4o"
        self.chat_agent = ChatAgent(self.model)
        self.play_agent = PlayAgent(self.chat_agent, self.model)
        self.feedback_agent = FeedbackAgent(self.play_agent, self.model)
        self.recent_messages = []

    def get_model_definition(self) -> model_pb2.modelDefinition:
        return model_definition

    def publish_metrics(self, metrics_json: str) -> None:
        logger.info(metrics_json)

    async def get_response(self, message: TaskInput) -> TaskOutput:
        msg = message.model_dump()["messages"]
        try:
            data = ast.literal_eval(msg[-1]["content"][-1]["text"])

            if data["target"] == "chatRequest":
                taskResponse = TaskOutput()
                taskResponse.text = await self.chatRequest(data)
                return taskResponse

            elif data["target"] == "playRequest":
                taskResponse = TaskOutput()
                taskResponse.text = await self.playRequest(data)
                return taskResponse

            elif data["target"] == "playFeedback":
                taskResponse = TaskOutput()
                taskResponse.text = await self.playFeedback(data)
                return taskResponse

        except:
            model = ChatOpenAI(
                base_url=base_url,
                default_headers=default_headers,
                max_tokens=4096,
            )

            ai_messages = message.model_dump()["messages"]

            for ai_message in ai_messages:
                if ai_message["role"] == "system":
                    ai_message["role"] = "user"
            AIresponse = model.invoke(ai_messages)
            print(f"AIresponse: {AIresponse.content}")
            taskResponse = TaskOutput()
            taskResponse.text = AIresponse.content
            return taskResponse

    async def playRequest(self, data):
        # Generate play with full game state and chat history
        play_response = await self.play_agent.generatePlay(
            data["objective"], data["state"], data["board_img"], data["drawer_img"]
        )

        # a = await self.parsePlayResponse(play_response, data)
        return json.dumps(play_response)

    async def playFeedback(self, data):
        # Get adjustments based on recent context (pass full feedback data)
        adjusted_play = await self.feedback_agent.adjustPlay(
            data["state"], data["board_img"]
        )
        return json.dumps(
            adjusted_play
        )  # await self.parsePlayResponse(adjusted_play, data))

    async def chatRequest(self, data):
        # Store the incoming message
        self.recent_messages.append(data["message"])

        # Generate chat response with full history
        chat_response = await self.chat_agent.handleChat(
            data["objective"],
            data["state"],
            data["message"],
            data["board_img"],
            data["drawer_img"],
        )
        return json.dumps(chat_response)

    async def parsePlayResponse(self, response, data=None):
        # Check if the response indicates no changes are needed
        if "FINISH" in response:  # response.strip().split()[0].upper() == "FINISH":
            if len(response.strip().split()) > 1:
                return [
                    {"type": "chat", "message": response.split("FINISH")[1].strip()},
                    {
                        "type": "finish",
                        "timestamp": (
                            data["timestamp"] if data and "timestamp" in data else ""
                        ),
                    },
                ]
            return {
                "type": "finish",
                "timestamp": data["timestamp"] if data and "timestamp" in data else "",
            }

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
            res = [
                {
                    "type": "play",
                    "shape": piece,
                    "position": (float(x), float(y)),
                    "rotation": float(rotation),
                    "timestamp": (
                        data["timestamp"] if data and "timestamp" in data else ""
                    ),
                }
            ]
            if message_part:
                res.append({"type": "chat", "message": message_part.strip()})
                return res
            return res[0]
        except Exception as e:
            print(f"Error parsing play response: {e}, response received: {response}")
            return [
                {
                    "type": "chat",
                    "message": "Sorry had some trouble playing this turn.",
                },
                {
                    "type": "finish",
                    "timestamp": (
                        data["timestamp"] if data and "timestamp" in data else ""
                    ),
                },
            ]
