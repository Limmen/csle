from typing import List
import subprocess
import threading
import time
import logging
import random
from scipy.stats import poisson
from scipy.stats import expon
from concurrent import futures
import grpc
import csle_collector.client_manager_pb2_grpc
import csle_collector.client_manager_pb2


class ClientThread(threading.Thread):
    """
    Thread representing a client
    """

    def __init__(self, service_time: float, commands: List[str]) -> None:
        """
        Initializes the client

        :param service_time: the service time of the client
        """
        threading.Thread.__init__(self)
        self.service_time = service_time
        self.commands = commands

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
                time.sleep(5)
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

    def __init__(self, commands: List[str], time_step_len_seconds: float = 1, lamb: int = 10, mu: float = 0.1,
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
                service_time = expon.rvs(scale=1/(self.mu*(self.time_step_len_seconds)), loc=0, size=1)[0]
                thread = ClientThread(service_time=service_time, commands=commands)
                thread.start()
                self.client_threads.append(thread)
            time.sleep(self.time_step_len_seconds)


class ClientManagerServicer(csle_collector.client_manager_pb2_grpc.ClientManagerServicer):
    """
    gRPC server for managing the running clients. Allows to start/stop clients remotely and also to query the
    state of the clients.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        self.arrival_thread = None
        logging.basicConfig(filename="/client_manager.log", level=logging.INFO)

    def getClients(self, request: csle_collector.client_manager_pb2.GetClientsMsg, context: grpc.ServicerContext) \
            -> csle_collector.client_manager_pb2.ClientsDTO:
        """
        Gets the state of the clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        num_clients = 0
        client_process_active = False
        if self.arrival_thread is not None:
            num_clients = len(self.arrival_thread.client_threads)
            client_process_active = True
        clients_dto = csle_collector.client_manager_pb2.ClientsDTO(
            num_clients = num_clients,
            client_process_active = client_process_active
        )
        return clients_dto

    def stopClients(self, request: csle_collector.client_manager_pb2.StopClientsMsg, context: grpc.ServicerContext):
        """
        Stops the Poisson-process that generates new clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info("Stopping clients")
        if self.arrival_thread is not None:
            self.arrival_thread.stopped = True
            time.sleep(1)
        self.arrival_thread = None

        return csle_collector.client_manager_pb2.ClientsDTO(
            num_clients = 0,
            client_process_active = False
        )

    def startClients(self, request: csle_collector.client_manager_pb2.StartClientsMsg,
                     context: grpc.ServicerContext) -> csle_collector.client_manager_pb2.ClientsDTO:
        """
        Starts/Restarts the Poisson process that generates clients

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info(f"Starting clients, commands:{request.commands}")
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

        clients_dto = csle_collector.client_manager_pb2.ClientsDTO(
            num_clients = len(self.arrival_thread.client_threads),
            client_process_active = True
        )
        return clients_dto


def serve(port : int = 50051) -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    csle_collector.client_manager_pb2_grpc.add_ClientManagerServicer_to_server(
        ClientManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"ClientManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve(port=50051)



