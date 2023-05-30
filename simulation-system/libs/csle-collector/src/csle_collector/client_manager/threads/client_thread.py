from typing import List
import threading
import time
import subprocess


class ClientThread(threading.Thread):
    """
    Thread representing a client
    """

    def __init__(self, commands: List[str], time_step_len_seconds: float, service_time: float = -1) -> None:
        """
        Initializes the client

        :param service_time: the service time of the client
        """
        threading.Thread.__init__(self)
        self.service_time = service_time
        self.commands = commands
        self.time_step_len_seconds = time_step_len_seconds

    def run(self) -> None:
        """
        The main function of the client

        :return: None
        """
        start = time.time()
        done = False
        cmd_index = 0
        while not done:
            cmd = self.commands[cmd_index]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            p.communicate()
            p.wait()
            time.sleep(self.time_step_len_seconds)
            time_lapsed = time.time() - start
            if self.service_time != -1 and time_lapsed >= self.service_time:
                done = True
            elif self.service_time == -1 and cmd_index == len(self.commands):
                done = True
            else:
                if cmd_index < len(self.commands) - 1:
                    cmd_index += 1
                else:
                    cmd_index = 0