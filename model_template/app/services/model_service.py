
from fastapi import HTTPException
import json

from app.model import ai_model
from app.schemas.api_schemas import ModelRequest, ModelAnswer
from app.schemas.data_models import TaskInput

class ModelService:
    def __init__(self):        
        self.ai_model = ai_model

    async def predict(self, request : ModelRequest) -> ModelAnswer:
        if self.ai_model.get_model_definition().modelID != request.modelID:
            raise HTTPException(status_code=400, detail=f"Wrong model!")
        task_input = TaskInput(messages=json.loads(request.request))
        
        result = await self.ai_model.get_response(task_input)
        model_answer = ModelAnswer(answer=result.model_dump_json(), sessionID=request.sessionID)
        return model_answer