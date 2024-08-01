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
from openai import OpenAI
from noun_extraction.noun_extraction import GetNoun


logger = logging.getLogger(__name__)


class Poetry(Task):
    ############################################## my code ##############################################
    # put your open ai api key to openai_api_key
    openai_api_key = ''
    def __init__(self):
        self.noun = GetNoun()
        self.sentence_entities_nouns = {}
        self.theme = 'poem'
        self.current_input_list = []
        self.store_dict = {}
        self.client = OpenAI(api_key =openai_api_key)


    # def get_gpt4_response(self, prompt):
    #     response = openai.ChatCompletion.create(
    #         model="GPT4_turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": f"请给我提供一个关于 {prompt} 在中文语境和文化中最有名的故事。如果有，请直接返回这一系列故事的简要介绍（最多3个故事，每个故事最多2-3句话）。特别注意，这个故事应该是只有在中文文化中才能存在的。如果没有关于此事物的故事，请返回“no store”。请用英语回答！"}
    #         ],
    #         max_tokens=1500
    #     )
    #     return response.choices[0].message['content']

    ############################################## my code ##############################################

    def get_system_prompt(self, objective: str) -> str:
        """Generate response endpoint:
        generate the response based on given prompt and store the conversation
        in the history of the session (based on the session_id cookie)
        """

        # 调用API获取回复
        if objective!= None:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "assistant", "content": "You're a well translator ."},
                    {"role": "user", "content": f"Please help me translate the following languages into English( Just give me the answer in English and don't say anything else, such as the opening line): \n {objective}"}
                ]
                )
            objective = completion.choices[0].message.content
        
        system_prompt = f"""You are working together with a user to iteratively create an English story about the theme {objective}. 
            Each of you should generate one line in each step. You will get a message from the user in the form 
            POEM_LINE COMMENT_LINE: POEM_LINE is the new story line provided by the user and it is 
            wrapped inside square brackets while COMMENT_LINE are the comment made by the user.
            Your answer should take the comment and the story line into consideration.
            If the COMMENT_LINE and a POEM_LINE are both empty, it means they want you to start the story, 
            and you must answer by generating the first line of story in English, the first line should be about the {objective},
            wrapped inside square brackets. 
            When starting the story, you also need to provide background information to user about
            the theme in its original cultural backgrouand using English if the {objective} is not in English. 
            Also tried to provide similar stories in other cultural background.

            If the COMMENT_LINE is not empty and the POEM_LINE is empty, you give your 
            opinion or answer about the content of COMMENT_LINE that the user provided (example: "I like the story so far, 
            it depicts a beautiful picture"). If the user ask a question, you anser it.

            Otherwise, your answer must follow this form: [YOUR_POEM_LINE] [YOUR_COMMENT] where 
            YOUR_POEM_LINE is the story line you created and it has to be wrapped inside square brackets while YOUR_COMMENT
            is your answer or opinion about the content of COMMENT_LINE that the user provided provided in normal text form (example:
            "[In a golden sky, the sun starts to set] I like the idea of a golden sky in the sun set"). You should say your
            feeling about the story line the user gave and give recommendation about it if needed.
            You are curious, and always ready and eager to ask the user question if needed.

            Create a new fictional story that seamlessly blends the plots and characters from [BACKGROUND], [YOUR_POEM_LINE], and [YOUR_COMMENT]. Ensure that the story incorporates as many elements from these sources as possible while maintaining a coherent and engaging plot.

            ### Please create a new fictional story with the following requirements:
            1. The story must incorporate as many plots and characters from [BACKGROUND] as possible.
            2. Each new sentence must include characters from [YOUR_POEM_LINE] and [YOUR_COMMENT].
            3. Integrate certain plots or characters from [BACKGROUND] to interact with the characters from [YOUR_POEM_LINE] and [YOUR_COMMENT].
            4. Ensure each scene is specific and clear, avoiding any vague descriptions.
            5. The storyline must be coherent and logical, allowing the reader to easily understand the progression of the story.


            Your story line must not repeat what the user has already given, or what you have generated before.
            The story should follow the following ten rules.
            #### rules
            1. Turn-taking: Each participant, whether human or robot, takes turns adding one sentence to the story.
            2. Coherence: Each sentence must connect logically with the previous one, ensuring the story flows smoothly.
            3. Length Limit: Each sentence should be between 20 to 40 words to avoid being too long or too short.
            4. Creativity: Participants are encouraged to be creative, introducing new characters, plot twists, or settings, but must maintain overall coherence of the story.
            5. Character Limit: Each participant can introduce only one new character per turn to prevent the story from becoming overly complex.
            6. Temporal Elements: At least one element of time travel must be included every five sentences to highlight the core feature of the story machine.
            7. Respect and Inclusion: Story content must respect all participants, avoiding offensive, discriminatory, or inappropriate material.
            8. Cultural Diversity: Participants are encouraged to incorporate and explore elements from different countries and cultures, enriching the story's diversity.
            9. Periodic Summaries: Every ten sentences, provide a brief summary to review the plot and ensure all participants understand the current progression of the story.
            10. Collaborative Spirit: Participants are encouraged to collaborate actively, embracing and building on others' ideas rather than just pushing their own.
            """
        return system_prompt


    def process_model_answer(self, answer: ModelResponse) -> TaskDataResponse:
        # Again, we ignore the potential image here...
        # if self.store_dict != {}:
        #     store_background = 'We have provided you with some related stories for your reference: \n'
        #     for nouns in self.store_dict.keys():
        #         store_background += '**' + nouns +'**: \n'
        #         store_background += '' +self.store_dict[nouns].replace('\n','')+'\n'
        #     store_background += '\n'
        #     answer.text += store_background+'\n'

        return TaskDataResponse(text=answer.text)

    def generate_model_request(self, request: TaskDataRequest) -> TaskRequest:
        """Generate prompt endpoint:
        process pieces' data and plug them into the prompt
        """
    ############################################## my code ##############################################

        # extract entities from sentences
        self.current_input_list = []
        print('%'*10)
        print(request.text)
        print(request.inputData)
        if request.objective!=None:
            if len(request.objective) > 0:
                completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "assistant", "content": "You're a well translator ."},
                    {"role": "user", "content": f"Please help me translate the following languages into English( Just give me the answer in English and don't say anything else, such as the opening line): \n {request.objective}"}
                ]
                )
                request.objective = completion.choices[0].message.content
                self.theme = request.objective
        if request.text!=None and request.text!='':
            if len(request.text) > 0:
                completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "assistant", "content": "You're a well translator ."},
                    {"role": "user", "content": f"Please help me translate the following languages into English( Just give me the answer in English and don't say anything else, such as the opening line): \n {request.text}"}
                ]
                )
                request.text = completion.choices[0].message.content
                self.current_input_list.append(request.text)
        if request.inputData['commentData']!=None and request.inputData['commentData']!='':
            if len(request.inputData['commentData']) > 0:
                completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "assistant", "content": "You're a well translator ."},
                    {"role": "user", "content": f"Please help me translate the following languages into English( Just give me the answer in English and don't say anything else, such as the opening line): \n {request.inputData['commentData']}"}
                ]
                )
                request.inputData['commentData'] = completion.choices[0].message.content
                self.current_input_list.append(request.inputData['commentData'])
        print(self.theme)
        print(type(self.theme))
        print(self.current_input_list)
        self.sentence_entities_nouns = self.noun.getSimilarity(self.theme, self.current_input_list)
        print('---'*10)
        print(self.sentence_entities_nouns)
        nouns_list = list(self.sentence_entities_nouns.keys())
        if len(nouns_list)>0:
            if len(nouns_list)>5:
                nouns_list = nouns_list[:3]
            for nouns in nouns_list:
                # self.store_dict[nouns] = TaskRequest(text=f"请给我提供一个关于 {nouns} 在中文语境和文化中最有名的故事。如果有，请直接返回这一系列故事的简要介绍（** 最多2个故事 **，每个故事最多1-2句话）。特别注意，这个故事应该是只有在中文文化中才能存在的。如果没有关于此事物的故事，请返回“no store”。请用英语回答！", 
                # system='', 
                # image=None, sessionID = "98766")
                
                # print('*'*30)


                # 多国语言 - 改
                completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "assistant", "content": "You're a well-read historian."},
                    {"role": "user", "content": f"Please provide a brief introduction (2-3 sentences each, up to 5 stories, ** The total generated length should not exceed 35 words. **) of the most famous stories in the contexts and cultures of Chinese, Russian, Japanese, German, Dutch, etc., about or related to {nouns}. If there are no such stories, please return 'no story'."}
                ]
                )  
                if 'no story' not in completion.choices[0].message.content:
                    self.store_dict[nouns] = completion.choices[0].message.content

                # # 中文
                # completion = self.client.chat.completions.create(
                # model="gpt-4o",
                # messages=[
                #     {"role": "assistant", "content": "You're a well-read historian."},
                #     {"role": "user", "content": f"请给我提供一个关于或者类似 {nouns} 在中文语境和文化中最有名的故事。如果有，请直接返回这一系列故事的简要介绍（最多2个故事，每个故事最多2-3句话）。特别注意，这个故事应该是只有在中文文化中才能存在的。如果没有关于此事物的故事，请返回“no store”。请用英语回答！"}
                # ]
                # )  
                # if 'no story' not in completion.choices[0].message.content:
                #     self.store_dict[nouns] = completion.choices[0].message.content

                # 德文
                # completion = self.client.chat.completions.create(
                # model="gpt-4o",
                # messages=[
                #     {"role": "assistant", "content": "You're a well-read historian."},
                #     {"role": "user", "content": f"Bitte geben Sie mir eine berühmte Geschichte über oder ähnlich wie {nouns} im deutschen Kontext und in der deutschen Kultur. Wenn vorhanden, geben Sie eine kurze Beschreibung dieser Geschichten (maximal 3 Geschichten, jede Geschichte maximal 2-3 Sätze). Bitte beachten Sie, dass diese Geschichten nur in der deutschen Kultur existieren sollten. Wenn es keine Geschichten über dieses Substantiv gibt, schreiben Sie bitte „no store“. Bitte auf Englisch antworten!"}
                # ]
                # )
                # if 'no story' not in completion.choices[0].message.content:
                #     if nouns in self.store_dict.keys():
                #         self.store_dict[nouns] += completion.choices[0].message.content
                #     else:
                #         self.store_dict[nouns] = completion.choices[0].message.content

                # 打印API回复
                # print(self.store_dict[nouns])
                # print('*'*30)
        print('---'*10)
        store_background = '\n Here are some related stories for keywords that you can try to combine to create new and interesting stories:\n'

        for nouns in self.store_dict.keys():
            store_background += '**' + nouns +'**: \n'
            store_background += self.store_dict[nouns].replace('\n','')+'\n'
        store_background += '\n'

        print('*'*30)
        print(store_background)
        print('*'*30)
    ############################################## my code ##############################################


        # This could include an image, but for this task, we currently don't supply one
        logger.info(request)
        return TaskRequest(
            text=f"[POEM_LINE] : {request.text} \n[COMMENT_LINE] : {request.inputData['commentData']}\n[BACKGROUND] : {store_background}",
            system=self.get_system_prompt(request.objective) ,
            image=None,
        )

    def get_requirements(self) -> TaskRequirements:
        return TaskRequirements(needs_text=True, needs_image=False)
