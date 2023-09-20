from typing import List
import threading
import time
import logging
import math
from scipy.stats import poisson
from csle_collector.client_manager.threads.client_thread import ClientThread
from csle_collector.client_manager.dao.client import Client
from csle_collector.client_manager.dao.workflows_config import WorkflowsConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType
from csle_collector.client_manager.dao.constant_arrival_config import ConstantArrivalConfig
from csle_collector.client_manager.dao.sine_arrival_config import SineArrivalConfig
from csle_collector.client_manager.dao.piece_wise_constant_arrival_config import PieceWiseConstantArrivalConfig
from csle_collector.client_manager.dao.spiking_arrival_config import SpikingArrivalConfig
from csle_collector.client_manager.dao.eptmp_arrival_config import EPTMPArrivalConfig


class ArrivalThread(threading.Thread):
    """
    Thread that generates client arrivals (starts client threads according to a Poisson process)
    """

    def __init__(self, time_step_len_seconds: float, clients: List[Client], workflows_config: WorkflowsConfig):
        """
        Initializes the arrival thread

        :param time_step_len_seconds: the number of seconds that one time-unit of the Poisson process corresponds to
        :param clients: the list of client profiles
        :param workflows_config: the workflow configurations
        """
        threading.Thread.__init__(self)
        self.time_step_len_seconds = time_step_len_seconds
        self.client_threads: List[ClientThread] = []
        self.t = 0
        self.clients = clients
        self.workflows_config = workflows_config
        self.stopped = False
        self.rate = 0.0
        logging.info(f"Starting arrival thread, num client types:{len(self.clients)}, "
                     f"num workflows: {len(self.workflows_config.workflow_markov_chains)}")

    @staticmethod
    def piece_wise_constant_rate(t: int, arrival_config: PieceWiseConstantArrivalConfig) -> float:
        """
        Function that returns the rate of a piece-wise constant Poisson process

        :param t: the time-step
        :param arrival_config: the arrival process configuration
        :return: the rate
        """
        rate = 0.0
        assert len(arrival_config.breakvalues) == len(arrival_config.breakpoints)
        for i in range(len(arrival_config.breakvalues)):
            if t >= arrival_config.breakpoints[i]:
                rate = arrival_config.breakvalues[i]
        return rate

    @staticmethod
    def spiking_poisson_arrival_rate(t: int, arrival_config: SpikingArrivalConfig) -> float:
        """
        Function that returns the rate of a spiking Poisson process

        :param t: the time-step
        :param arrival_config: the arrival process configuration
        :return: the rate
        """
        assert len(arrival_config.exponents) == len(arrival_config.factors)
        rate = 0.0
        for i in range(len(arrival_config.exponents)):
            rate = arrival_config.factors[i] * math.exp(math.pow(-(t - arrival_config.exponents[i]), 2))
        return rate

    @staticmethod
    def sine_modulated_poisson_rate(t: int, arrival_config: SineArrivalConfig) -> float:
        """
        Function that returns the rate of a sine-modulated Poisson process

        :param t: the time-step
        :param arrival_config: the arrival process configuration
        :return: the rate
        """
        return arrival_config.lamb + arrival_config.period_scaling_factor * math.sin(
            arrival_config.time_scaling_factor * math.pi * t)

    @staticmethod
    def constant_poisson_rate(arrival_config: ConstantArrivalConfig) -> float:
        """
        Function that returns the rate of a stationary Poisson process

        :param arrival_config: the arrival process configuration
        :return: the rate
        """
        return arrival_config.lamb

    @staticmethod
    def eptmp_rate(t: int, arrival_config: EPTMPArrivalConfig) -> float:
        """
        Function that returns the rate of a EPTMP Poisson process.

        EPTMP or Exponential-Polynomial-Trigonometric rate function having Multiple Periodicities.
        This class is used for creating a rate function that can exhibit both global trends as well as
        periodic components with individual frequencies and amplitudes.
        (Kuhl and Wilson, 1995)

        :param t: the time-step
        :param arrival_config: the arrival process configuration
        :return: the rate
        """
        theta_sum = 0.0
        for i, theta in enumerate(arrival_config.thetas):
            theta_sum += theta * pow(t, i)
        second_sum = 0.0
        for i, (gamma, phi, omega) in enumerate(zip(arrival_config.gammas, arrival_config.phis, arrival_config.omegas)):
            second_sum += gamma * math.sin(omega * t + phi)
        return math.exp(theta_sum + second_sum)

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
            for c in self.clients:
                try:
                    if c.arrival_config.client_arrival_type.value == ClientArrivalType.SINE_MODULATED.value:
                        self.rate = self.sine_modulated_poisson_rate(t=self.t, arrival_config=c.arrival_config)
                        num_new_clients = poisson.rvs(self.rate, size=1)[0]
                    elif c.arrival_config.client_arrival_type.value == ClientArrivalType.CONSTANT.value:
                        self.rate = self.constant_poisson_rate(arrival_config=c.arrival_config)
                        num_new_clients = poisson.rvs(self.rate, size=1)[0]
                    elif c.arrival_config.client_arrival_type.value == ClientArrivalType.PIECE_WISE_CONSTANT.value:
                        self.rate = self.piece_wise_constant_rate(t=self.t, arrival_config=c.arrival_config)
                        num_new_clients = poisson.rvs(self.rate, size=1)[0]
                    elif c.arrival_config.client_arrival_type.value == ClientArrivalType.EPTMP.value:
                        self.rate = self.eptmp_rate(t=self.t, arrival_config=c.arrival_config)
                        num_new_clients = poisson.rvs(self.rate, size=1)[0]
                    else:
                        raise ValueError(f"Client arrival type: {c.arrival_config.client_arrival_type} not recognized")
                except Exception as e:
                    logging.info(f"There was an error computing the arrival rate: {str(e)}, {repr(e)}")
                try:
                    for nc in range(num_new_clients):
                        commands = c.generate_commands(workflows_config=self.workflows_config)
                        thread = ClientThread(commands=commands, time_step_len_seconds=self.time_step_len_seconds)
                        thread.start()
                        self.client_threads.append(thread)
                except Exception as e:
                    logging.info(f"There was an error starting the client threads: {str(e), repr(e)}")
            time.sleep(self.time_step_len_seconds)
