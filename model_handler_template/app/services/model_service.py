
# This is code for a session handling interface using redis for storage.


import json
import logging
import random
from typing import Annotated, List

from fastapi import HTTPException, Depends
import redis
import httpx

import app.db.redis as redis_db
from app.schemas.api_schemas import ModelAnswer, ModelDefinition, ModelRequirements, ModelRequest, TaskRequest
from app.utils.lifecycle import get_httpx_client

logger = logging.getLogger("app")


class ModelService:
    def __init__(self, 
                 httpx_client: Annotated[httpx.AsyncClient, Depends(get_httpx_client)]
                 ):  
        self.redis_client: redis.StrictRedis = redis_db.redis_model_client
        self.httpx_client = httpx_client
        

    def registerModel(self, request : ModelDefinition):
        exists = self.redis_client.exists(request.modelID)       
        if exists:
            print(f"Overriding existing model: {self.redis_client.get(request.modelID)} with {request}")            
        
        self.redis_client.set(request.modelID, request.model_dump_json())

    async def find_fitting_model(self, requirements: ModelRequirements) -> ModelDefinition:
        models : List[ModelDefinition]= []
        keys = self.redis_client.keys()
        print(keys)
        for key in keys:
            model_data = self.redis_client.get(key)
            if model_data:
                print(f"Found model in redis: {model_data}")
                model = ModelDefinition.model_validate_json(model_data)
                models.append(model)
        suitable_models_list = []
        # Scan in the model list for the suitable model
        for model in models:
            if requirements.needs_text and requirements.needs_image:
                if model.can_text and model.can_image:
                    suitable_models_list.append(model)
            elif requirements.needs_text:
                if model.can_text and not model.needs_image:
                    suitable_models_list.append(model)
            elif requirements.needs_image:
                if model.can_image and not model.needs_text:
                    suitable_models_list.append(model)
        # choose a random model if there are multiple that sastisfy the requirements
        chosen_model = random.choice(suitable_models_list)
        print("The chosen model is")
        print(chosen_model)
        return ModelDefinition.model_validate(chosen_model)
        
    async def get_model(self, model_name: str) -> ModelDefinition:        
        model_str = json.loads(self.redis_client.get(model_name))        
        if not model_str:
            raise HTTPException(status_code=404, detail="Model not found")        
        return ModelDefinition.model_validate(model_str)

    async def forward_request(self, model: ModelDefinition, model_request: TaskRequest) -> ModelAnswer:        
        # Here you would implement the logic to forward the request to the actual model handler
        # This is a placeholder implementation
        current_request = ModelRequest(
            request=model_request.request,
            modelID=model.modelID,
            sessionID=model_request.sessionID
        )
        response = await self.httpx_client.post(f"http://{model.hostname}:8000/model/request", json=current_request.model_dump())
        print(response)
        print(response.json())
        response.raise_for_status()
        return ModelAnswer.model_validate(response.json())
