import os
from app.tasks.task_interface import ArenaTask
# define the Task
from app.task_examples import (
    poetry,
    tangram,
    gesture,
    openai_task,
    mealplan,
    tangram_openai,
    recipe,
    floorplan,
    math_tutor
)

currentTask = os.environ.get("TASK_NAME")

if currentTask == "tangram":
    task : ArenaTask = tangram.Tangram()
elif currentTask == "openai":
    task = openai_task.OpenAITask()
elif currentTask == "gesture":
    task = gesture.Gesture()
elif currentTask == "poetry_openai":
    task = poetry.PoetryOpenAI()
elif currentTask == "mealplan":
    task = mealplan.Mealplan()
elif currentTask == "tangram_openai":
    task = tangram_openai.Tangram()
elif currentTask == "recipe":
    task = recipe.Recipe()
elif currentTask == "floorplan":
    task = floorplan.Floorplan()
elif currentTask == "math_tutor":
    task = math_tutor.MathTutor()
else:
    task = poetry.Poetry()
