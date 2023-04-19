import logging
import threading
import time
from typing import List
from scipy.stats import poisson
from client_thread_new import ClientThreadNew

from client_type import ClientType
from service import Service


class ArrivalThreadNew(threading.Thread):
    """
    Thread that generates client threads accoriding to a time-varying Poisson process with a custom arrival rate function.
    """
    def __init__(self, time_step_len_seconds: float, client_type: ClientType, services: List[Service]) -> None:
        """
        Initializes a new arrival thread.

        :param rate_function: A function that returns the arrival rate at a given time.
        :param time_step_len_seconds: The time step length in seconds.
        :param commands: A list of commands to be executed by the client.
        """
        threading.Thread.__init__(self)
        self.t = 0
        self.client_threads = []
        self.stopped = False
        self.rate_function = client_type.arrival_process.rate_f
        self.time_step_len_seconds = time_step_len_seconds
        self.client_type = client_type
        self.services = services

    def run(self) -> None:
        """
        Runs the arrival generator.
        The arrival generator generates client threads according to a time-varying Poisson process with a custom arrival rate function.
        A sequence of commands is generated for each client thread according to its workflow distribution.
        """
        while not self.stopped:
            self.t += 1
            new_client_threads = []

            # Add alive client threads to the list of new client threads
            for client_thread in self.client_threads:
                if client_thread.is_alive():
                    new_client_threads.append(client_thread)

            # Generate new client threads
            arrival_rate = self.rate_function(self.t)
            logging.info("t: " + str(self.t) + ", arrival_rate: " + str(arrival_rate))
            if arrival_rate > 0:
                num_new_clients = poisson.rvs(arrival_rate, size=1)[0]
                for _ in range(num_new_clients):
                    new_client_thread = ClientThreadNew(self.client_type.generate_commands(self.services), self.time_step_len_seconds)
                    new_client_thread.start()
                    self.client_threads.append(new_client_thread)
                    
            time.sleep(self.time_step_len_seconds)

