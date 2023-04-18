import subprocess
import threading
import time
import logging
from typing import List

class ClientThreadNew(threading.Thread):
    """
    A thread for a client. The thread executes a list of commands with a fixed time step length between commands.
    """

    def __init__(self, commands: List[str], time_step_len_seconds: float) -> None:
        """
        Initializes a new thread for a client.
        
        :param commands: A list of commands to be executed by the client.
        :param time_step_len_seconds: The time step length in seconds.
        """
        threading.Thread.__init__(self)
        self.commands = commands
        self.time_step_len_seconds = time_step_len_seconds

    def run(self) -> None:
        """
        Runs the client thread.
        """
        for command in self.commands:
            logging.debug("Executing command: " + str(command))
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            p.communicate() # Execute command and wait for the command to finish
            time.sleep(self.time_step_len_seconds)