# Task template for use with the Collaborative AI Arena

This module serves as a template task ( and as a suggestion on how to set up communication pathes)
The aim of this template is to allow concurrent processing of requests and implement the flow for the Task component as detailed in the following diagram:

![A diagram showing the flow of messages from the model perspective](docs/model-flow.svg)

## Task Messages

There are four types of messages, a task will receive or send, which are all defined by the `tasks.proto` file.
The messages along with their fields are:

- Incoming Messages
  - `modelAnswer`:
    - `answer` : A string represnting a json object with the following fields: 
      - `text` : The text of the answer of the model 
      - `image`: a base64 encoded image.
    - `sessionID`: An ID of the session that this response is for
- Outgoing Messages:  
  - `taskRequest`
    - `request` : A string represnting a json object with the following fields:
      - `text` : An array of messages with a syntax resembling OpenAI messages. Each message has a field `role` and a field `content` where role can be either `"assistant"` or `"user"`
      - `image`: a base64 encoded image.
      - `system`: A String representing a system message to the model (i.e. the task description)    
    - `sessionID`: An ID of the session that generated this resource
  - `taskMetrics`:
    - `metrics`: A String that is alredy formatted and just needs to be put into the models log, so that it can be interpreted by AIBuilder for the leaderboard
    - `sessionID`: The session for which these metrics were generated
  - `modelRequirements`: A message that indicates, what the model needs to be able to handle for this session of this task
    - `needs_text`: A Bool indicating whether the model needs text for processing
    - `needs_image`: A Bool indicating whether the model needs an image for processing
    - `sessionID`: The ID for these requirements

## Task Services

The task will need to implement the four services detailed in the tasks.proto file.
Those contain:

- `startTask` : A Service which is called with an empty request on startup and needs to inform the model handler, whenever a new session is generated by the task (i.e. for each new run of a task). The message needs to define the `modelRequirements` containing the `sessionID`, which will allow the model handler to select one model for this session. This definition indicates the capabilities of the model required to fullfil the task (i.e. it needs to specify whether the model needs to be able to handle text and images to work with this task).
- `runTask`:  This is again a service with an empty request, which needs to provide a sstream of `taskRequest` messages, which will be allocated to the correct model by the model handler. 
- `finishTask`: Again a service that needs to provide a stream of `taskMetrics` messages upon completion of the task by the user. 
- `getModelResponse`: This service receives the responses by the model, and needs to be able to handle them and assign them to the web-requests that caused their generation. 

The logic of the processing is as follows:
When a user sends a request that they want to start the task, the `startTask` service should emit a `modelRequirements` message. This message is used by the model handler to select a model for the indicated session.
After this message, the `runTask` service can emit several `taskRequest` messages, which will be processed and forwarded by the model handler to the appropriate model.
Finally, when a session (i.e. running one task) ends, the task needs to emit one `taskMetrics` message from the `finishTask` service to indicate, that this session is over, and that the association can be removed. After that it can emit a new `modelReqirements` message from the `startTask` service, if a new session was started etc..

## Implementation

We provide a sample implementation of a Task Server in the `model_server.py` class.
The `main.py` file further implements a FastAPI server which can serve a ready to serve front-end along with three end-points that can be used as a basis and implementation example for tasks and the communication logic.
Finally, the `model.py` file 

### Models:

For simplicty, we have defined three pydantic models, that we use for interaction between the model server and the actual model implementation in the data_models class:

- `TaskMessage`, a class with two fields:
  - `role` : A String indicating the role that generated the element (either "user" for the participant or "assistant" for the ai )
  - `content`: the content of the message
- `TaskInput`, a class defining the input to a task

  - `text` : a List of `TaskMessage` objects (representing the textual history)
  - `image` : a string base64 encoded image
  - `system` : The system message describing the task to solve

- `TaskOutput`, a class defining the input to a task
  - `text` : a String with the model answer
  - `image` : a string base64 encoded image of the model answer (can be None)

### Interface

This server handles most interactions and relies on the `model.py` file to provide the following methods and fields:

- Methods:
  - publish_metrics(metrics_json: str):
    - A Method that publishes (i.e. prints) the given metrics to the container log
  - async get_response(message: TaskInput) -> TaskOutput:
    - A asynchronous method that performs the handling of the input, processing it by the actual model and returning a TaskOutput that can then be sent on.