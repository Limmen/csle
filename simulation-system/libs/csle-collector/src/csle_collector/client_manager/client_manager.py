from typing import List
import time
import logging
import grpc
from concurrent import futures
from csle_collector.client_manager.client_type import ClientType
from csle_collector.client_manager.threads.arrival_thread import ArrivalThread
from csle_collector.client_manager.threads.producer_thread import ProducerThread
from csle_collector.client_manager.workflows.workflow_distribution import WorkflowDistribution
from csle_collector.client_manager.workflows.workflow import Workflow
from csle_collector.client_manager.services.service import Service
from csle_collector.client_manager.threads.arrival_thread_new import ArrivalThreadNew
from csle_collector.client_manager.eptmp_rate_function import EPTMPRateFunction
from csle_collector.client_manager.client_arrival_type import ClientArrivalType
import csle_collector.client_manager.client_manager_pb2_grpc
import csle_collector.client_manager.client_manager_pb2
import csle_collector.constants.constants as constants


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
                     f"client_arrival_type: {request.client_arrival_type}, "
                     f"time_scaling_factor: {request.time_scaling_factor}, "
                     f"period_scaling_factor: {request.period_scaling_factor},"
                     f"exponents: {request.exponents}, "
                     f"factors: {request.factors}, breakvalues: {request.breakvalues}, "
                     f"breakpoints: {request.breakpoints}")
        producer_time_step_len_seconds = 0
        if self.arrival_thread is not None:
            self.arrival_thread.stopped = True
            time.sleep(1)
        if request.time_step_len_seconds <= 0:
            request.time_step_len_seconds = 1
        client_arrival_type = ClientArrivalType(request.client_arrival_type)
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
    
    def startClientsNew(self, request: csle_collector.client_manager.client_manager_pb2.StartClientsMsg,
                     context: grpc.ServicerContext) -> csle_collector.client_manager.client_manager_pb2.ClientsDTO:
        """
        Starts/Restarts the Poisson process that generates clients using the new generator

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the clients
        """
        logging.info(f"Starting clients, time_step_len_seconds: {request.time_step_len_seconds}, "
             f"client_types: {request.client_types},"
             f"services: {request.services}")
        
        producer_time_step_len_seconds = 0

        if self.arrival_thread is not None:
            self.arrival_thread.stopped = True
            time.sleep(1)
        self.arrival_thread = None

        if request.time_step_len_seconds <= 0:
            request.time_step_len_seconds = 1
        
        # Unpack messages from gRPC request into the correct objects
        client_types = [
            ClientType(
                EPTMPRateFunction(client_type.eptmp_rate_function.thetas,
                                  client_type.eptmp_rate_function.gammas,
                                  client_type.eptmp_rate_function.phis,
                                  client_type.eptmp_rate_function.omegas),
                WorkflowDistribution([
                    (workflowTuple.probability, Workflow(
                        [row.probabilities for row in workflowTuple.workflow.rows],
                        workflowTuple.workflow.initial_state))
                    for workflowTuple in client_type.workflow_distribution.outcomes
                ])
            ) 
            for client_type in request.client_types
        ]

        services = [
            Service(service.commands) for service in request.services
        ]
        
        arrival_thread = ArrivalThreadNew(time_step_len_seconds=request.time_step_len_seconds,
                                          client_types=client_types, services=services)
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
        logging.info(f"Starting producer, time-step:{request.time_step_len_seconds}, "
                     f"arrival_thread: {self.arrival_thread}")
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
