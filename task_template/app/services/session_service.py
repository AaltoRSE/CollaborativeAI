
from typing import Annotated
import json
import httpx
from fastapi import Depends, Request
import redis 

from app.schemas.router_models import SessionData
from app.services.completion_service import CompletionService
from app.db.redis import get_history_client
from app.utils.lifecycle import get_httpx_client
from app.schemas.api_schemas import IdMessage

class SessionService:
    def __init__(self, completion_service : Annotated[CompletionService, Depends(CompletionService)],
                 httpx_client : Annotated[httpx.AsyncClient, Depends(get_httpx_client)],
                 history_client: Annotated[redis.StrictRedis, Depends(get_history_client)]):
        self.completion_service = completion_service
        self.httpx_client = httpx_client
        self.history_client = history_client
    
    async def obtain_session_id(self) -> str:
        task_props = self.completion_service.get_requirements()
        response = await self.httpx_client.post("http://model_handler:8000/session/startTask", json=task_props.model_dump())
        response.raise_for_status()
        session_id = IdMessage.model_validate(response.json()).sessionID
        return session_id

    async def init_session(self) -> str:
        session_id = await self.obtain_session_id()
        self.history_client.set(session_id, json.dumps([]))
        return session_id   

    async def get_session(self, request: Request) -> SessionData:
                    
        session_id = request.session["key"] if "key" in request.session else None    
        if session_id is None:
            session_id = await self.init_session()        
        else:        
            recent_history = self.history_client.get(session_id)        
            # This is not a session of ours, so we need a new session
            if recent_history is None:
                session_id = await self.init_session()            
        # Set the session key!
        request.session["key"] = session_id
        history = json.loads(self.history_client.get(session_id))
        session_data = SessionData(history=history, id=session_id)
        return session_data


    def clear_session(self,session_id : str | None):            
        if session_id is None:
            pass
        else:
            self.history_client.delete(session_id)
            return True
