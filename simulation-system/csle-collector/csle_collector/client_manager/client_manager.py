from typing import List
import subprocess
import threading
import time
import logging
import random
from scipy.stats import poisson
from scipy.stats import expon
from concurrent import futures
import socket
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
            (output, err) = p.communicate()
            p_status = p.wait()
            time_lapsed = time.time() - start
            if time_lapsed >= self.service_time:
                done = True
            else:
                time.sleep(self.time_step_len_seconds)
                time_lapsed = time.time() - start
                if time_lapsed < self.service_time:
                    if cmd_index < len(self.commands)-1:
                        cmd_index += 1
                    else:
                        cmd_index = 0


class ArrivalThread(threading.Thread):
    """
    Thread that generates client arrivals (starts client threads according to a Poisson process)
    """

    def __init__(self, commands: List[str], time_step_len_seconds: float = 1, lamb: float = 10, mu: float = 0.1,
                 num_commands: int = 2):
        """
        Initializes the arrival thread

        :param time_step_len_seconds: the number of seconds that one time-unit of the Poisson process corresponds to
        :param lamb: the lambda parameter of the Poisson process for arrivals
        :param mu: the mu parameter of the service times of the clients
        :param commands: the list of commands that clients can use
        :param num_commands: the number of commands per client
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
        logging.info(f"Starting arrival thread, lambda:{lamb}, mu:{mu}, num:commands:{num_commands}, "
                     f"commands:{commands}")

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
            new_clients = poisson.rvs(self.lamb*self.time_step_len_seconds, size=1)[0]
            for nc in range(new_clients):
                commands = random.sample(self.commands, self.num_commands)
                service_time = expon.rvs(scale=self.time_step_len_seconds/(self.mu), loc=0, size=1)[0]
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
        self.ip = socket.gethostbyname(self.hostname)
        self.conf = {'bootstrap.servers': f"{self.kafka_ip}:{self.port}", 'client.id': self.hostname}
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
                self.producer.produce(constants.LOG_SINK.CLIENT_POPULATION_TOPIC_NAME,
                                      f"{ts},{self.ip},{num_clients}")


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
        logging.basicConfig(filename="/client_manager.log", level=logging.INFO)

    def getClients(self, request: csle_collector.client_manager.client_manager_pb2.GetClientsMsg, context: grpc.ServicerContext) \
            -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
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
            num_clients = num_clients,
            client_process_active = client_process_active,
            producer_active=producer_active,
            clients_time_step_len_seconds = clients_time_step_len_seconds,
            producer_time_step_len_seconds = producer_time_step_len_seconds
        )
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
            num_clients = 0,
            client_process_active = False,
            producer_active = producer_active,
            clients_time_step_len_seconds = clients_time_step_len_seconds,
            producer_time_step_len_seconds = producer_time_step_len_seconds
        )

    def startClients(self, request: csle_collector.client_manager.client_manager_pb2.StartClientsMsg,
                     context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Starts/Restarts the Poisson process that generates clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info(f"Starting clients, commands:{request.commands}")

        clients_time_step_len_seconds = 0
        producer_time_step_len_seconds = 0

        if self.arrival_thread is not None:
            self.arrival_thread.stopped = True
            time.sleep(1)

        if request.time_step_len_seconds <= 0:
            request.time_step_len_seconds = 1

        arrival_thread = ArrivalThread(commands = request.commands,
                                       time_step_len_seconds=request.time_step_len_seconds,
                                       lamb=request.lamb, mu=request.mu)
        arrival_thread.start()
        self.arrival_thread = arrival_thread
        clients_time_step_len_seconds = self.arrival_thread.time_step_len_seconds

        producer_active = False
        if self.producer_thread is not None:
            producer_active = True
            producer_time_step_len_seconds = self.producer_thread.time_step_len_seconds

        clients_dto = csle_collector.client_manager.client_manager_pb2.ClientsDTO(
            num_clients = len(self.arrival_thread.client_threads),
            client_process_active = True,
            producer_active = producer_active,
            clients_time_step_len_seconds = clients_time_step_len_seconds,
            producer_time_step_len_seconds = producer_time_step_len_seconds
        )
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
            num_clients = num_clients,
            client_process_active = client_process_active,
            producer_active = True,
            clients_time_step_len_seconds = clients_time_step_len_seconds,
            producer_time_step_len_seconds = request.time_step_len_seconds
        )
        return clients_dto

    def stopProducer(self, request: csle_collector.client_manager.client_manager_pb2.StopProducerMsg,
                      context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Stops the producer thread that pushes data to Kafka

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info(f"Stopping producer")

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
            num_clients = num_clients,
            client_process_active = client_process_active,
            producer_active = False,
            clients_time_step_len_seconds = clients_time_step_len_seconds,
            producer_time_step_len_seconds = 0
        )
        return clients_dto


def serve(port : int = 50051) -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    csle_collector.client_manager.client_manager_pb2_grpc.add_ClientManagerServicer_to_server(
        ClientManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"ClientManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve(port=50051)



