from typing import List
import subprocess
import threading
import time
import logging
import random
import math
from scipy.stats import poisson
from scipy.stats import expon
from concurrent import futures
import socket
import netifaces
from confluent_kafka import Producer
import grpc
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.constants.constants as constants


class ClientThread(threading.Thread):
    """
    Thread representing a client
    """

    def __init__(self, service_time: float, commands: List[str], time_step_len_seconds: float) -> None:
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
            if time_lapsed >= self.service_time:
                done = True
            else:
                if cmd_index < len(self.commands) - 1:
                    cmd_index += 1
                else:
                    cmd_index = 0


class ArrivalThread(threading.Thread):
    """
    Thread that generates client arrivals (starts client threads according to a Poisson process)
    """

    def __init__(self, commands: List[str], time_step_len_seconds: float = 1, lamb: float = 10, mu: float = 0.1,
                 num_commands: int = 2, sine_modulated: bool = False,
                 time_scaling_factor: float = 0.01, period_scaling_factor: float = 20,
                 exponents: List[float] = None, factors: List[float] = None, spiking: bool = False,
                 piece_wise_constant: bool = False, breakpoints: List[float] = None, breakvalues: List[float] = None):
        """
        Initializes the arrival thread

        :param commands: the list of commands that clients can use
        :param time_step_len_seconds: the number of seconds that one time-unit of the Poisson process corresponds to
        :param lamb: the lambda parameter of the Poisson process for arrivals
        :param mu: the mu parameter of the service times of the clients
        :param num_commands: the number of commands per client
        :param sine_modulated: boolean flag whether the rate of the arrival process is sine-modulated or not
        :param time_scaling_factor: parameter for sine-modulated rate
        :param period_scaling_factor: parameter for sine-modulated rate
        :param exponents: parameters for spiking rate
        :param factors: parameters for spiking rate
        :param spiking: boolean flag indicating whether spiking rate should be used
        :param piece_wise_constant: boolean flag indicating whether spiking piece-wise constant rate should be used.
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
        self.sine_modulated = sine_modulated
        self.rate = self.lamb
        self.time_scaling_factor = time_scaling_factor
        self.period_scaling_factor = period_scaling_factor
        self.exponents = exponents
        self.factors = factors
        self.spiking = spiking
        self.piece_wise_constant = piece_wise_constant
        self.breakpoints = breakpoints
        self.breakvalues = breakvalues
        logging.info(f"Starting arrival thread, lambda:{lamb}, mu:{mu}, num_commands:{num_commands}, "
                     f"commands:{commands}, sine_modulated: {sine_modulated}, "
                     f"time_scaling_factor: {time_scaling_factor}, period_scaling_factor: {period_scaling_factor},"
                     f"spiking: {spiking}, exponents: {exponents}, factors: {factors}, breakpoints: {breakpoints}, "
                     f"breakvalues: {breakvalues}, piece_wise_constant: {piece_wise_constant}")

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
            if self.sine_modulated:
                rate = self.sine_modulated_poisson_rate(self.t)
                self.rate = rate
                new_clients = poisson.rvs(rate, size=1)[0]
            else:
                new_clients = poisson.rvs(self.lamb, size=1)[0]
            for nc in range(new_clients):
                commands = random.sample(self.commands, self.num_commands)
                service_time = expon.rvs(scale=(self.mu * self.time_step_len_seconds), loc=0, size=1)[0]
                thread = ClientThread(service_time=service_time, commands=commands,
                                      time_step_len_seconds=self.time_step_len_seconds)
                thread.start()
                self.client_threads.append(thread)
            time.sleep(self.time_step_len_seconds)


class ProducerThread(threading.Thread):
    """
    Thread that pushes statistics to Kafka
    """

    def __init__(self, arrival_thread, time_step_len_seconds: int, ip: str, port: int):
        """
        Initializes the thread

        :param arrival_thread: the thread that manages the client arrivals, used to extract statistics
        :param time_step_len_seconds: the length between pushing statistics to Kafka
        :param ip: the ip of the Kafka server
        :param port: the port of the Kafka server
        """
        threading.Thread.__init__(self)
        self.arrival_thread = arrival_thread
        self.time_step_len_seconds = time_step_len_seconds
        self.stopped = False
        self.kafka_ip = ip
        self.port = port
        self.hostname = socket.gethostname()
        try:
            self.ip = netifaces.ifaddresses(constants.INTERFACES.ETH0)[netifaces.AF_INET][0][constants.INTERFACES.ADDR]
        except Exception:
            self.ip = socket.gethostbyname(self.hostname)
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.port}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**self.conf)
        logging.info(f"Starting producer thread, ip:{self.ip}, kafka port:{self.port}, "
                     f"time_step_len:{self.time_step_len_seconds}, kafka_ip:{self.kafka_ip}")

    def run(self) -> None:
        """
        Main loop of the thread, pushes data to Kafka periodically

        :return: None
        """
        while not self.stopped and self.arrival_thread is not None:
            time.sleep(self.time_step_len_seconds)
            if self.arrival_thread is not None:
                ts = time.time()
                num_clients = len(self.arrival_thread.client_threads)
                rate = self.arrival_thread.rate
                mu = self.arrival_thread.mu
                self.producer.produce(constants.KAFKA_CONFIG.CLIENT_POPULATION_TOPIC_NAME,
                                      f"{ts},{self.ip},{num_clients},{rate},{mu}")
                self.producer.poll(0)


class ClientManagerServicer(csle_collector.client_manager.client_manager_pb2_grpc.ClientManagerServicer):
    """
    gRPC server for managing the running clients. Allows to start/stop clients remotely and also to query the
    state of the clients.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        self.arrival_thread = None
        self.producer_thread = None
        logging.basicConfig(filename=f"{constants.LOG_FILES.CLIENT_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.CLIENT_MANAGER_LOG_FILE}", level=logging.INFO)

    def getClients(self, request: csle_collector.client_manager.client_manager_pb2.GetClientsMsg,
                   context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Gets the state of the clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        num_clients = 0
        clients_time_step_len_seconds = 0
        producer_time_step_len_seconds = 0

        client_process_active = False
        if self.arrival_thread is not None:
            num_clients = len(self.arrival_thread.client_threads)
            client_process_active = True
            clients_time_step_len_seconds = self.arrival_thread.time_step_len_seconds

        producer_active = False
        if self.producer_thread is not None:
            producer_active = True
            producer_time_step_len_seconds = self.producer_thread.time_step_len_seconds

        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=num_clients, client_process_active=client_process_active, producer_active=producer_active,
            clients_time_step_len_seconds=clients_time_step_len_seconds,
            producer_time_step_len_seconds=producer_time_step_len_seconds)
        return clients_dto

    def stopClients(self, request: csle_collector.client_manager.client_manager_pb2.StopClientsMsg,
                    context: grpc.ServicerContext):
        """
        Stops the Poisson-process that generates new clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info("Stopping clients")

        clients_time_step_len_seconds = 0
        producer_time_step_len_seconds = 0

        if self.arrival_thread is not None:
            self.arrival_thread.stopped = True
            time.sleep(1)
        self.arrival_thread = None

        producer_active = False
        if self.producer_thread is not None:
            producer_active = True
            producer_time_step_len_seconds = self.producer_thread.time_step_len_seconds

        return csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=0, client_process_active=False, producer_active=producer_active,
            clients_time_step_len_seconds=clients_time_step_len_seconds,
            producer_time_step_len_seconds=producer_time_step_len_seconds)

    def startClients(self, request: csle_collector.client_manager.client_manager_pb2.StartClientsMsg,
                     context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Starts/Restarts the Poisson process that generates clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info(f"Starting clients, commands:{request.commands}, lamb: {request.lamb}, mu: {request.mu}, "
                     f"sine_modulated: {request.sine_modulated}, "
                     f"time_scaling_factor: {request.time_scaling_factor}, "
                     f"period_scaling_factor: {request.period_scaling_factor}, spiking: {request.spiking}, "
                     f"piece_wise_constant: {request.piece_wise_constant}, exponents: {request.exponents}, "
                     f"factors: {request.factors}, breakvalues: {request.breakvalues}, "
                     f"breakpoints: {request.breakpoints}")

        producer_time_step_len_seconds = 0

        if self.arrival_thread is not None:
            self.arrival_thread.stopped = True
            time.sleep(1)

        if request.time_step_len_seconds <= 0:
            request.time_step_len_seconds = 1

        arrival_thread = ArrivalThread(commands=request.commands, time_step_len_seconds=request.time_step_len_seconds,
                                       lamb=request.lamb, mu=request.mu, sine_modulated=request.sine_modulated,
                                       time_scaling_factor=request.time_scaling_factor,
                                       period_scaling_factor=request.period_scaling_factor,
                                       piece_wise_constant=request.piece_wise_constant, breakvalues=request.breakvalues,
                                       breakpoints=request.breakpoints, factors=request.factors,
                                       exponents=request.exponents, spiking=request.spiking)
        arrival_thread.start()
        self.arrival_thread = arrival_thread
        clients_time_step_len_seconds = self.arrival_thread.time_step_len_seconds

        producer_active = False
        if self.producer_thread is not None:
            producer_active = True
            producer_time_step_len_seconds = self.producer_thread.time_step_len_seconds

        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=len(self.arrival_thread.client_threads), client_process_active=True,
            producer_active=producer_active, clients_time_step_len_seconds=clients_time_step_len_seconds,
            producer_time_step_len_seconds=producer_time_step_len_seconds)
        return clients_dto

    def startProducer(self, request: csle_collector.client_manager.client_manager_pb2.StartProducerMsg,
                      context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Starts/Restarts the producer thread that pushes data to Kafka

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info(f"Starting producer, time-step:{request.time_step_len_seconds}")

        clients_time_step_len_seconds = 0
        time.sleep(5)

        if self.producer_thread is not None:
            self.producer_thread.stopped = True
            time.sleep(1)

        if request.time_step_len_seconds <= 0:
            request.time_step_len_seconds = 1
        producer_thread = ProducerThread(arrival_thread=self.arrival_thread,
                                         time_step_len_seconds=request.time_step_len_seconds,
                                         ip=request.ip, port=request.port)
        producer_thread.start()
        self.producer_thread = producer_thread

        client_process_active = False
        num_clients = 0
        if self.arrival_thread is not None:
            num_clients = len(self.arrival_thread.client_threads)
            client_process_active = True
            clients_time_step_len_seconds = self.arrival_thread.time_step_len_seconds

        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=num_clients, client_process_active=client_process_active, producer_active=True,
            clients_time_step_len_seconds=clients_time_step_len_seconds,
            producer_time_step_len_seconds=request.time_step_len_seconds)
        return clients_dto

    def stopProducer(self, request: csle_collector.client_manager.client_manager_pb2.StopProducerMsg,
                     context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Stops the producer thread that pushes data to Kafka

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info("Stopping producer")

        clients_time_step_len_seconds = 0

        if self.producer_thread is not None:
            self.producer_thread.stopped = True
            time.sleep(1)
        self.producer_thread = None

        client_process_active = False
        num_clients = 0
        if self.arrival_thread is not None:
            num_clients = len(self.arrival_thread.client_threads)
            client_process_active = True
            clients_time_step_len_seconds = self.arrival_thread.time_step_len_seconds

        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients=num_clients, client_process_active=client_process_active, producer_active=False,
            clients_time_step_len_seconds=clients_time_step_len_seconds, producer_time_step_len_seconds=0)
        return clients_dto


def serve(port: int = 50044, log_dir: str = "/", log_file_name: str = "client_manager.log",
          max_workers: int = 10) -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.CLIENT_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.CLIENT_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.client_manager.client_manager_pb2_grpc.add_ClientManagerServicer_to_server(
        ClientManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"ClientManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
