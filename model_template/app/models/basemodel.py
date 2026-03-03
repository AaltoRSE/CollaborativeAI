from app.schemas.data_models import *
from app.schemas.api_schemas import ModelDefinition


class AIModel:
    def get_model_definition(self) -> ModelDefinition:
        raise NotImplementedError()

    def publish_metrics(self, metrics_json: str) -> None:
        raise NotImplementedError()

    async def get_response(self, message: TaskInput) -> TaskOutput:
        raise NotImplementedError()
