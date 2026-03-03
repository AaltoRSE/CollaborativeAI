import json
import os
from typing import Annotated
from datetime import datetime

import pymongo.collection
from pytz import timezone
from fastapi import APIRouter, status, Depends, HTTPException
from app.db.atlas import get_atlas_collection
from app.schemas.api_schemas import IdMessage, ModelRequirements, TaskMetrics, ModelInfo
from app.services.session_service import SessionService


router = APIRouter(prefix="/session", tags=["session"]) 


@router.post("/startTask", status_code=status.HTTP_200_OK)
async def start_task(
	requirements: ModelRequirements,
	session_service: Annotated[SessionService, Depends(SessionService)]
) -> IdMessage:
	"""Create a new session for the given model requirements and return the session ID."""
	session_id = await session_service.create_session(requirements)
	return IdMessage(sessionID=session_id)


@router.post("/endTask", response_model=ModelInfo, status_code=status.HTTP_200_OK)
async def end_task(
	metrics: TaskMetrics,
	session_service: Annotated[SessionService, Depends(SessionService)],
	rating_collection: Annotated[pymongo.collection.Collection, Depends(get_atlas_collection)]
):
	"""Finish a task: retrieve the assigned model, delete the session, and return model info."""	
	# This would happen if "finish task" is called before "start task"
	# At this point no model was selected, since nothing has happened yet..
	# There is no point in storing the metrics in the db, since there was no model...
	try:
		model = await session_service.get_model_for_session(metrics.sessionID)
	except KeyError:
		raise HTTPException(status_code=404, detail="Session not found")
	modelID = model.modelID
	# Metrics	
	parsedMetrics = json.loads(metrics.metrics.replace("'", '"'))

	rating = parsedMetrics["rating"]
	task_name = parsedMetrics["task_name"]

	# Time stamp
	tz = timezone("Europe/Helsinki")
	submitted_time = datetime.now(tz)

	# Store the metrics to the db
	new_metric = {
		"task_name": task_name,
		"model": modelID,
		"timeStamp": submitted_time,
		"collaboration_metric": rating["collaboration_metric"],
		"ai_performance_metric": rating["ai_performance_metric"],
		"coordination_metric": rating["coordination_metric"],
		"efficiency_metric": rating["efficiency_metric"],
	}

	if not os.environ.get("ATLAS_URI", None) == None:
		rating_collection.insert_one(new_metric)

	# Break the model assignment after sending the metrics
	session_service.delete_session(metrics.sessionID)
	return 	ModelInfo(model_name=modelID, sessionID=metrics.sessionID)
