
class AgentLog:
    def __init__(self):
        self.log = []


    def add_entry(self, msg):
        self.log.append(msg)

    def reset(self):
        self.log = []
