import copy

from openai import OpenAI
from dataclasses import dataclass

class Character:
    def __init__(self, character_description: str, model_name="gpt-4-turbo"):
        self.client = OpenAI()
        self.model_name = model_name
        self.character_description = character_description

    def _get_prompt(self, story_summary: str) -> str:
        return f"""
        You will play a role of a character in a story.

        Your character is described as follows:
        ```
        {self.character_description}
        ```

        You are now given the following story summary:
        ```
        {story_summary}
        ```

        Your task is to write what is the next action your character will take. Provide a short description of the action.
        The maximum length of the action description is 100 words.
        Your action description:
        """

    def get_action(self, story_summary: str) -> str:
        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "system", "content": self._get_prompt(story_summary)}]
        )
        return chat_completion.choices[0].message.content

@dataclass
class ActionOutcome:
    what_happened: str
    world_state_change: str

class WorldSimulator:
    def __init__(self,
                 world_rules: str,
                 model_name="gpt-4-turbo"):

        self.client = OpenAI()
        self.model_name = model_name
        self.rules = world_rules

    def _get_system_prompt(self,
                           story_summary: str,
                           action_description: str,
                           character_description: str) -> str:
        return f"""
        You will be given a story summary, character description and a description of the action the character took.
        Your task is to write what happened as a result of the character's action and how the world state changed.

        The world is described by the following rules:
        ```
        {self.rules}
        ```

        The story so far:
        ```
        {story_summary}
        ```

        Character description:
        ```
        {character_description}
        ```

        The character took the following action:
        ```
        {action_description}
        ```

        You will now decide what happened as a result of the character's action and how the world state changed.
        """

    def _get_prompt_outcomes(self) -> str:
        return """
        What happened as a result of the character's action?
        Describe the outcome of the action. The maximum length of the description is 100 words.
        """
    
    def _get_prompt_world_state_change(self) -> str:
        return """
        How did the world state change as a result of the character's action?
        Describe the changes in the world state. The maximum length of the description is 100 words.
        """

    def get_outcome(self,
                    story_summary: str,
                    character_description: str,
                    action_description: str) -> ActionOutcome:

        messages = [{"role": "system",
                     "content": self._get_system_prompt(story_summary=story_summary,
                                                        action_description=action_description,
                                                        character_description=character_description)},
                    {"role": "user", "content": self._get_prompt_outcomes()}]

        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )

        what_happened = chat_completion.choices[0].message.content
        messages.append({"role": "assistant", "content": what_happened})
        messages.append({"role": "user", "content": self._get_prompt_world_state_change()})

        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )

        world_state_change = chat_completion.choices[0].message.content

        return ActionOutcome(what_happened=what_happened,
                             world_state_change=world_state_change)

@dataclass
class StoryPart:
    agent_action: str
    what_happened: str
    world_state_change: str

    def as_str(self):
        out =  f"### Character Action ###\n{self.agent_action}\n"
        out += f"### Character Action Outcome ###\n {self.what_happened}\n"
        out += f"### World State Change ###\n{self.world_state_change}\n"
        return out

class ProfessionalCritique:
    def __init__(self, model_name="gpt-4-turbo"):
        self.client = OpenAI()
        self.model_name = model_name
    
    def get_prompt(self, story: str) -> str:
        return f"""
        You are given an incomplete story outline.
        Your task is to critique the story and provide constructive feedback on how to improve it.
        The maximum length of the critique is 200 words.

        The story so far:
        ```
        {story}
        ```

        This is not complete story. You will now provide feedback on how to improve the story.
        """

    def get_critique(self, story: str) -> str:
        messages = [{"role": "system", "content": self.get_prompt(story)}]
        
        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )

        return chat_completion.choices[0].message.content

class UserFeedbackApplicator:
    def __init__(self, model_name="gpt-4-turbo"):
        self.client = OpenAI()
        self.model_name = model_name

    def _get_prompt(self, story: str, user_feedback ) -> str:
        return f"""
        You are given a story summary and the story so far.
        Your task is to rewrite the story to incorporate the user feedback.
        
        You will output the story in the exactly the same format as the input story.

        The input story:
        ```
        {story}
        ```

        The user feedback:
        ```
        {user_feedback}
        ```

        You will now rewrite the story to incorporate the user feedback.
        """

    def apply_user_feedback(self, story:str, user_feedback: str) -> str:
        messages = [{"role": "system",
                     "content": self._get_prompt(story=story, user_feedback=user_feedback)}]

        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )

        return chat_completion.choices[0].message.content

class FullTextGenerator:
    def __init__(self, model_name="gpt-4-turbo"):
        self.client = OpenAI()
        self.model_name = model_name

    def get_prompt(self, story: str) -> str:
        return f"""
        You are given a story summary.
        Your task is to generate a full text story based on the summary.

        The story so far:
        ```
        {story}
        ```

        You will now generate a full text story based on the summary.
        """
    
    def generate_full_text(self, story: str) -> str:
        messages = [{"role": "system", "content": self.get_prompt(story)}]
        
        chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )

        return chat_completion.choices[0].message.content

class StoryMaker:
    def __init__(self,
                 world_rules: str,
                 initial_world_state: str,
                 character_description: str):
        self.character = Character(character_description)
        self.world_sim = WorldSimulator(world_rules)
        self.initial_world_state = initial_world_state
        self.critique = ProfessionalCritique()
        self.user_feedback_applicator = UserFeedbackApplicator()
        self.full_text_generator = FullTextGenerator()

        self.story: str = ""
        self.step_id = 1

    # Gives you what happened
    def step(self) -> StoryPart:
        character_action = self.character.get_action(self.get_story_summary())

        action_outcome = self.world_sim.get_outcome(self.get_story_summary(),
                                                    self.character.character_description,
                                                    character_action)

        part = StoryPart(agent_action=character_action,
                         what_happened=action_outcome.what_happened,
                         world_state_change=action_outcome.world_state_change)

        self.story += f"### Part {self.step_id} ###\n"
        self.story += part.as_str()
        return copy.deepcopy(part)
    
    def critique_story(self):
        return self.critique.get_critique(self.get_story_summary())
    
    def apply_user_feedback(self, user_feedback: str):
        self.story = self.user_feedback_applicator.apply_user_feedback(self.get_story_summary(), user_feedback)
    
    def generate_full_text(self):
        return self.full_text_generator.generate_full_text(self.get_story_summary())
    
    def get_story_summary(self) -> str:
        summary = self.initial_world_state + "\n"
        summary += self.story
        return summary

def main():
    world_rules = """The world is a D&D dungeon. There is a chest in the middle of the room.
    The chest is locked. The key is on the table.
    The room is dimly lit.
    """

    initial_world_state = """You are in the dungeon. You have a torch."""

    character_description = """
    You are a mage. You have a spellbook and a staff.
    """

    story_maker = StoryMaker(world_rules, initial_world_state, character_description)

    for i in range(3):
        part = story_maker.step()
        print(f"### Story Part {i} ###")
        print(part.as_str())

# Story that we have to provide to the user
    print("\n\n########## Story Summary #############")
    print(story_maker.get_story_summary())
# Critique 
    print("\n\n########## Story Critique #############")
    print(story_maker.critique_story())

    user_feedback = "I do not like the fact that the there is no monster in the dungeon. It is too boring."
    story_maker.apply_user_feedback(user_feedback)

    print("\n\n########## Story Summary After User Feedback #############")
    print(story_maker.get_story_summary())
        
# Calling this at the end only when we are done
    print("\n\n########## Full Text Story #############")
    print(story_maker.generate_full_text())

if __name__ == "__main__":
    main()

sys_prompt = f"""
You are an assistant dedicated to helping the user create a fictional world. Your primary role is to enhance the user's creative capabilities by offering suggestions on ways to gather new ideas and inspiration. Guide the user through their creation process without dictating specific content unless explicitly requested. Focus on nurturing the user's creativity and helping them explore their imagination to its fullest potential.
The user prefers to use certain techniques in their creative process, including: {notitle_prompt}.
Use these techniques to provide suggestions, but feel free to introduce other methods that might stimulate the user's creativity. Your ultimate goal is to empower the user to bring their fictional world to life with originality and depth.
Additionally, if the user requests to "finalize" their work, you should compile the entire description of the world they have written so far and present it in one comprehensive response which. The output should contain only the description of the world without any additional text.
"""