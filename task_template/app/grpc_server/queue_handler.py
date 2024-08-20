import queue


class QueueHandler:
    def __init__(self):
        self.start_queue = queue.Queue()
        self.task_queue = queue.Queue()
        self.finish_queue = queue.Queue()
        self.response_queues = {}
        self.responses = {}

    def add_answer(self, sessionID, messageID, answer):
        self.responses[sessionID][messageID] = answer

    def get_answer(self, sessionID, messageID):
        if not messageID in self.responses[sessionID]:
            return None
        else:
            answer = self.responses[sessionID][messageID]
            self.responses[sessionID].pop(messageID)
            return answer
    def process_queue(self, session_id):
        queue = self.get_response_queue(session_id)
        try:
            if not queue.empty():
                response = queue.get()
                self.add_answer(session_id, response.messageID, response)
        except:
            #TODO: Handle this properly with a lock on the queue....
            print("Error processing queue, possibly got consumed by a different thread")
        
    def add_response_queue(self, sessionID):
        if sessionID not in self.response_queues:
            self.response_queues[sessionID] = queue.Queue()
            self.responses[sessionID] = {}
    def get_response_queue(self, sessionID) -> queue.Queue:
        if sessionID not in self.response_queues:
            self.response_queues[sessionID] = queue.Queue()
        return self.response_queues[sessionID]

    def remove_response_queue(self, sessionID):
        if sessionID in self.response_queues:
            self.response_queues.pop(sessionID)
            self.responses.pop(sessionID)

queue_handler = QueueHandler()
