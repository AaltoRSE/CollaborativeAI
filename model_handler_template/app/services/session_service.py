# This is code for a session handling interface using redis for storage.


import logging
from typing import Annotated

import secrets
import string

from redis import Redis
from fastapi import Depends

import app.db.redis as redis_db
from app.schemas.api_schemas import ModelDefinition, ModelRequirements
from app.services.model_service import ModelService


logger = logging.getLogger("app")


class SessionService:
    def __init__(self, model_service: Annotated[ModelService, Depends(ModelService)], exp_time: int = 12 * 3600):  # 12 hours
        self.model_service = model_service
        self.expire_time = exp_time
        self.redis_client: Redis = redis_db.redis_session_client

    async def create_session(            
        self,          
        requirements: ModelRequirements      
    ) -> str:
        """
        Create a new session or update an existing session in Redis.

        Args:            
        Returns:
            str: The session key.
        """
        model = await self.model_service.find_fitting_model(requirements)

        # Should be the case in most instances.
        created_session_key = self.generate_session_key()
        # Make sure, it doesn't exist
        while self.redis_client.exists(created_session_key):
            created_session_key = self.generate_session_key()
        session_key = created_session_key
        assert session_key is not None
      
        self.redis_client.setex(
            session_key, self.expire_time, model.modelID)
        
        return session_key

    async def get_model_for_session(self, session_key: str) -> ModelDefinition:
        """
        Retrieve session data from Redis.

        Args:
            session_key (str): The session key.

        Returns:
            ModelDefinition: The model associated with the session, or None if the session does not exist.
        """
        model = self.redis_client.get(session_key)
        if model is None:
            raise KeyError("Session not found")
        return await self.model_service.get_model(model)

    def generate_session_key(self, length: int = 128):
        """
        Function to generate an API key.

        Parameters:
        - length (int, optional): Length of the generated API key. Defaults to 64.

        Returns:
        - str: The generated API key.
        """
        alphabet = string.ascii_letters + string.digits
        api_key = "".join(secrets.choice(alphabet) for _ in range(length))
        return api_key

    def delete_session(self, session_key: str):
        """
        Delete a session from Redis.

        Args:
            session_key (str): The session key.
        """
        self.redis_client.delete(session_key)