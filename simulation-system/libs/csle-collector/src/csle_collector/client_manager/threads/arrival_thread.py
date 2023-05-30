from typing import List
import threading
import time
import logging
import math
import random
from scipy.stats import poisson
from scipy.stats import expon
from csle_collector.client_manager.threads.client_thread import ClientThread
from csle_collector.client_manager.client_arrival_type import ClientArrivalType


class ArrivalThread(threading.Thread):
    """
    Thread that generates client arrivals (starts client threads according to a Poisson process)
    """

    def __init__(self, commands: List[str], time_step_len_seconds: float = 1, lamb: float = 10, mu: float = 0.1,
                 num_commands: int = 2, client_arrival_type: ClientArrivalType = ClientArrivalType.POISSON,
                 time_scaling_factor: float = 0.01, period_scaling_factor: float = 20,
                 exponents: List[float] = None, factors: List[float] = None,
                 breakpoints: List[float] = None, breakvalues: List[float] = None):
        """
        Initializes the arrival thread

        :param commands: the list of commands that clients can use
        :param time_step_len_seconds: the number of seconds that one time-unit of the Poisson process corresponds to
        :param lamb: the lambda parameter of the Poisson process for arrivals
        :param mu: the mu parameter of the service times of the clients
        :param num_commands: the number of commands per client
        :param time_scaling_factor: parameter for sine-modulated rate
        :param period_scaling_factor: parameter for sine-modulated rate
        :param exponents: parameters for spiking rate
        :param factors: parameters for spiking rate
        :param client_arrival_type: the type of arrival process
        """
        threading.Thread.__init__(self)
        self.time_step_len_seconds = time_step_len_seconds
        self.client_threads = []
        self.t = 0
        self.lamb = lamb
        self.mu = mu
        self.stopped = False
        self.commands = commands
        self.num_commands = num_commands
        self.client_arrival_type = client_arrival_type
        self.rate = self.lamb
        self.time_scaling_factor = time_scaling_factor
        self.period_scaling_factor = period_scaling_factor
        self.exponents = exponents
        self.factors = factors
        self.breakpoints = breakpoints
        self.breakvalues = breakvalues
        logging.info(f"Starting arrival thread, lambda:{lamb}, mu:{mu}, num_commands:{num_commands}, "
                     f"commands:{commands}, client_arrival_type: {client_arrival_type}, "
                     f"time_scaling_factor: {time_scaling_factor}, period_scaling_factor: {period_scaling_factor},"
                     f"exponents: {exponents}, factors: {factors}, breakpoints: {breakpoints}, "
                     f"breakvalues: {breakvalues}")

    def piece_wise_constant_rate(self, t) -> float:
        """
        Function that returns the rate of a piece-wise constant Poisson process

        :param t: the time-step
        :return: the rate
        """
        rate = 0
        assert len(self.breakvalues) == len(self.breakpoints)
        for i in range(len(self.breakvalues)):
            if t >= self.breakpoints[i]:
                rate = self.breakvalues[i]
        return rate

    def spiking_poisson_arrival_rate(self, t) -> float:
        """
        Function that returns the rate of a spiking Poisson process

        :param t: the time-step
        :return: the rate
        """
        rate = self.lamb
        assert len(self.exponents) == len(self.factors)
        for i in range(len(self.exponents)):
            rate = self.factors[i] * math.exp(math.pow(-(t - self.exponents[i]), 2))
        return rate

    def sine_modulated_poisson_rate(self, t) -> float:
        """
        Function that returns the rate of a sine-modulated Poisson process

        :param t: the time-step
        :return: the rate
        """
        return self.lamb + self.period_scaling_factor * math.sin(self.time_scaling_factor * math.pi * t)

    def run(self) -> None:
        """
        Runs the arrival generator, generates new clients dynamically according to a Poisson process

        :return: None
        """
        while not self.stopped:
            new_client_threads = []
            for ct in self.client_threads:
                if ct.is_alive():
                    new_client_threads.append(ct)
            self.client_threads = new_client_threads
            self.t += 1
            num_new_clients = 0
            if self.client_arrival_type == ClientArrivalType.SINE_MODULATED_POISSON.value:
                self.rate = self.sine_modulated_poisson_rate(t=self.t)
                num_new_clients = poisson.rvs(self.rate, size=1)[0]
            elif self.client_arrival_type == ClientArrivalType.POISSON.value:
                num_new_clients = poisson.rvs(self.lamb, size=1)[0]
            elif self.client_arrival_type == ClientArrivalType.PIECE_WISE_CONSTANT.value:
                self.rate = self.piece_wise_constant_rate(t=self.t)
                num_new_clients = poisson.rvs(self.rate, size=1)[0]
            elif self.client_arrival_type == ClientArrivalType.EPTMP.value:
                pass
            else:
                raise ValueError(f"Client arrival type: {self.client_arrival_type} not recognized")
            for nc in range(num_new_clients):
                commands = random.sample(self.commands, self.num_commands)
                service_time = expon.rvs(scale=(self.mu * self.time_step_len_seconds), loc=0, size=1)[0]
                thread = ClientThread(service_time=service_time, commands=commands,
                                      time_step_len_seconds=self.time_step_len_seconds)
                thread.start()
                self.client_threads.append(thread)
            time.sleep(self.time_step_len_seconds)