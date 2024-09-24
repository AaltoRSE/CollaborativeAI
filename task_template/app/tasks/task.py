import os

# define the Task
from task_examples import poetry, tangram, gesture


if os.environ.get("TASK_NAME") == "tangram":
    task = tangram.Tangram()
elif os.environ.get("TASK_NAME") == "gesture":
    task = gesture.Gesture()
else:
    task = poetry.Poetry()

