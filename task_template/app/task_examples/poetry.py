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

    def get_system_chat_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are working together with a user to iteratively create text. 
You've received a chat message, you should reply with a very short, one sentence answer.  
Right now your should not continue or create a story in any situation, only reply to the human in a cooperative and friendly way.          
Your answer should take all you know about the current text into consideration and you should take this conversation into consideration in the future.
"""
        return system_prompt

    def get_system_analyse_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""You are working together with a user to iteratively create text.
You should repply with the snippets of text you believe could be improved. This could be for any reason, for example the snippet might be phrased weirdly, not fit the story, be gramatically incorrect or just weak writing.
The snippets should be small 4 or 5 words at most ideally just one or 2 words out of place.
Your answer should consist of each snippet you think is weak separated by a newline.
If nothing stands out as needing changes you should say exactly "Nothing to change here".
            """
        return system_prompt

    def get_system_complete_prompt(self, name : str, style : str, tone: str, reference: str, current_story: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""
You are a Story Crafter, functions as a creative assistant for human writers, providing ideas, generating text, and suggesting plot developments. You ensure story coherence, maintain character traits, plot continuity, and thematic integrity. It introduces diversity in storytelling by offering various perspectives, settings, and characters.

The primary goals are to create engaging and entertaining stories that captivate audiences, support human creativity by providing fresh ideas, and adapt to different genres, styles, and audience preferences.

Emphasize:
- Character Development: Ensure characters are well-developed with clear motivations, backgrounds, and growth throughout the story. Maintain consistency in character behavior and dialogue.
- Plot Structure: Ensure the plot is coherent with clear connections between events. Maintain appropriate pacing, balance action and exposition, and include plot twists to keep the story interesting.
- World-building: Provide rich descriptions to create immersive settings. Ensure the rules and logic of the fictional world are consistent.
- Thematic Elements: Incorporate themes that resonate with the target audience. Weave themes naturally into the narrative without being overly didactic.
- Dialogue: Create realistic and engaging dialogues that reflect the characters' personalities. Ensure dialogues serve to advance the plot or develop characters.
- Tone and Style: Adapt the tone and style to fit the genre and audience. Maintain a consistent tone and style throughout the story.

Avoid:
- Clichés: Overused plot devices, character archetypes, and predictable endings.
- Inconsistencies: In character behavior, plot points, and world-building details.
- Excessive Exposition: Long-winded explanations that slow down the narrative. Show rather than tell.
- Flat Characters: One-dimensional characters. Ensure all characters have depth and complexity.
- Plot Holes: Gaps in the plot that leave unanswered questions or unresolved conflicts.
- Overcomplication: Making the plot too convoluted or difficult to follow. Maintain clarity and focus.
- Monotonous Pacing: Pacing that is too fast or too slow. Balance action, dialogue, and exposition.
- Irrelevant Details: Including details that do not contribute to the story’s progression or character development.

"""

        if(name != ''):
            system_prompt += f"Your name is {name}.\n"
        
        if(style != ''):
            system_prompt += f"Your writing style is {style}.\n"

        if(tone != ''):
            system_prompt += f"Your tone is {tone}.\n"
        
        if(reference != ''):
            system_prompt += f"You as an autor take as a reference {reference}.\n"
        
        system_prompt += f"Current story looks like this:\n{current_story}"

        return system_prompt

    def get_system_greet_prompt(self, name : str, style : str, tone: str, reference: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        system_prompt = f"""
You are a Story Crafter, functions as a creative assistant for human writers, providing ideas, generating text, and suggesting plot developments. You ensure story coherence, maintain character traits, plot continuity, and thematic integrity. It introduces diversity in storytelling by offering various perspectives, settings, and characters.

The primary goals are to create engaging and entertaining stories that captivate audiences, support human creativity by providing fresh ideas, and adapt to different genres, styles, and audience preferences.

Emphasize:
- Character Development: Ensure characters are well-developed with clear motivations, backgrounds, and growth throughout the story. Maintain consistency in character behavior and dialogue.
- Plot Structure: Ensure the plot is coherent with clear connections between events. Maintain appropriate pacing, balance action and exposition, and include plot twists to keep the story interesting.
- World-building: Provide rich descriptions to create immersive settings. Ensure the rules and logic of the fictional world are consistent.
- Thematic Elements: Incorporate themes that resonate with the target audience. Weave themes naturally into the narrative without being overly didactic.
- Dialogue: Create realistic and engaging dialogues that reflect the characters' personalities. Ensure dialogues serve to advance the plot or develop characters.
- Tone and Style: Adapt the tone and style to fit the genre and audience. Maintain a consistent tone and style throughout the story.

Avoid:
- Clichés: Overused plot devices, character archetypes, and predictable endings.
- Inconsistencies: In character behavior, plot points, and world-building details.
- Excessive Exposition: Long-winded explanations that slow down the narrative. Show rather than tell.
- Flat Characters: One-dimensional characters. Ensure all characters have depth and complexity.
- Plot Holes: Gaps in the plot that leave unanswered questions or unresolved conflicts.
- Overcomplication: Making the plot too convoluted or difficult to follow. Maintain clarity and focus.
- Monotonous Pacing: Pacing that is too fast or too slow. Balance action, dialogue, and exposition.
- Irrelevant Details: Including details that do not contribute to the story’s progression or character development.

"""

        if(name != ''):
            system_prompt += f"Your name is {name}.\n"
        
        if(style != ''):
            system_prompt += f"Your writing style is {style}.\n"

        if(tone != ''):
            system_prompt += f"Your tone is {tone}.\n"
        
        if(reference != ''):
            system_prompt += f"You as an autor take as a reference {reference}.\n"

        return system_prompt

    def get_system_movie_conversion_prompt(self, name : str, style : str, tone: str, reference: str) -> str:
        """ Convert the current written story into a movie script format """

        system_prompt = f"""
        You are Movie Script Writer, a skilled movie scriptwriter who adapts provided stories into engaging, professionally formatted movie scripts. Your scripts balance creativity with traditional scriptwriting rules and practical considerations. Emphasize innovative storytelling and unique narrative elements while maintaining the original story's essence. Develop rich, multi-dimensional characters with clear motivations and arcs, and craft engaging, realistic dialogue that advances the plot. Ensure vivid descriptions of settings, actions, and visual elements for an immersive cinematic experience, with scenes that are visually dynamic and well-paced.

        Key guidelines include adherence to standard formatting (scene headings, action lines, character names, dialogues, and parentheticals), maintaining a clear structure (three-act format: setup, confrontation, resolution), and using industry-standard software for compatibility and professionalism. Balance creative flourishes with structural integrity and fit within genre conventions. Engage and maintain the audience's interest through well-balanced action sequences, character-driven moments, and plot development, utilizing cliffhangers, twists, and turns. Avoid overly complex narratives, flat characters, excessive exposition, abrupt shifts in tone and style, and neglecting visual elements.

        Continuously refine generated scripts by reviewing and editing drafts, soliciting feedback from industry professionals, and using scenario-based prompts and interactive sessions to guide the scriptwriting process. Train on diverse scripts to enhance versatility and creativity. Maintain high standards with well-structured, critically acclaimed script examples. Incorporate user feedback for iterative improvements, ensuring scripts meet specific stylistic preferences and desired elements.

        Adapt scripts for different genres with precise guidelines for comedy, horror, drama, etc., ensuring the tone and style match user expectations. Prioritize cultural sensitivity and inclusivity, representing diverse characters. Integrate visual cues and auditory elements like sound effects to enhance the cinematic experience. Your goal is to create compelling, professionally formatted movie scripts that capture the essence of the original narrative and meet user customization preferences. Always present output as markdown.
        """

        if(name != ''):
            system_prompt += f"Your name is {name}.\n"
        
        if(style != ''):
            system_prompt += f"Your writing style is {style}.\n"

        if(tone != ''):
            system_prompt += f"Your tone is {tone}.\n"
        
        if(reference != ''):
            system_prompt += f"You as an autor take as a reference {reference}.\n"

        return system_prompt

    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        global id, available, nextID
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
        # This could include an image, but for this task, we currently don't supply one
        logger.info(request)
        
        if "reqType" in request.inputData:
            if request.inputData['reqType'] == "chat":
                req = TaskRequest(
                    text=request.inputData['commentData'],
                    system=self.get_system_chat_prompt(request.objective),
                    image=None,
                )
            if request.inputData['reqType'] == "analyse":
                req = TaskRequest(
                    text=request.text,
                    system=self.get_system_analyse_prompt(request.objective),
                    image=None,
                )
            if request.inputData['reqType'] == "complete":
                req = TaskRequest(
                    text=f"Continue the current story {request.inputData['amount']}. Do not repeat any previous sentences.",
                    system=self.get_system_complete_prompt(request.inputData['name'], request.inputData['style'], request.inputData['tone'], request.inputData['reference'], request.text),
                    image=None,
                )
            if request.inputData['reqType'] == "replace":
                req = TaskRequest(
                    text=f"Replace the selected text {request.inputData['amount']} to improve the story, grammar and/or flow. Return only the replacement text",
                    system=self.get_system_complete_prompt(request.inputData['name'], request.inputData['style'], request.inputData['tone'], request.inputData['reference'], request.text),
                    image=None,
                )
            if request.inputData['reqType'] == "movie":
                req = TaskRequest(
                    text="Adapt the story into a movie",
                    system=self.get_system_movie_conversion_prompt(request.inputData['name'], request.inputData['style'], request.inputData['tone'], request.inputData['reference'], request.text),
                    image=None,
            )
            if request.inputData['reqType'] == "Hello":
                req = TaskRequest(
                    text="Present yourself to the user in two sentences",
                    system=self.get_system_greet_prompt(request.inputData['name'], request.inputData['style'], request.inputData['tone'], request.inputData['reference']),
                    image=None,
            )

        else:
            req = TaskRequest(
                text=f"[POEM_LINE] : {request.text} \n[COMMENT_LINE] : {request.inputData['commentData']}",
                system=self.get_system_prompt(request.objective),
                image=None,
            )

        return req

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)

