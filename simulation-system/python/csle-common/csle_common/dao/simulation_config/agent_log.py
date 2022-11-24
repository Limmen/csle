
class AgentLog:
    """
    DTO Representing the Agent Log
    """

    def __init__(self):
        """
        Initializes the log
        """
        self.log = []

    def add_entry(self, msg) -> None:
        """
        Adds an entry to the log

        :param msg: the msg to add to the log
        :return: None
        """
        self.log.append(msg)

    def reset(self) -> None:
        """
        Resets the log

        :return: None
        """
        self.log = []
