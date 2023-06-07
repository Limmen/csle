from typing import List
import threading
import time
import subprocess


class ClientThread(threading.Thread):
    """
    Thread representing a client
    """

    def __init__(self, commands: List[str], time_step_len_seconds: float) -> None:
        """
        Initializes the client thread

        :param commands: the sequence of commands that the client will execute
        :param time_step_len_seconds: the length of a time-step in seconds
        """
        threading.Thread.__init__(self)
        self.commands = commands
        self.time_step_len_seconds = time_step_len_seconds

    def run(self) -> None:
        """
        The main function of the client. It executes a sequence of commands and then terminates

        :return: None
        """
        for cmd in self.commands:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            p.communicate()
            p.wait()
            time.sleep(self.time_step_len_seconds)
