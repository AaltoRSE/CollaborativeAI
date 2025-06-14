from models import *
import os

model_to_use = os.environ.get("MODEL_TO_USE")
if model_to_use == "aalto_image":    
    ai_model = AaltoImageModel()
elif model_to_use == "openai":    
    ai_model = OpenAIModel()
elif model_to_use == "o1mini":    
    ai_model = o1mini()
elif model_to_use == "o1":    
    ai_model = o1()
elif model_to_use == "aalto":    
    ai_model = AaltoModel()
elif model_to_use == "simpleTangram":    
    ai_model = simpleAgent()
else:    
    ai_model = OpenAIImageModel()
