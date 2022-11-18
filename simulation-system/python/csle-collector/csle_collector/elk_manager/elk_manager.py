from typing import Tuple
import logging
import os
import subprocess
from concurrent import futures
import grpc
import socket
import csle_collector.elk_manager.elk_manager_pb2_grpc
import csle_collector.elk_manager.elk_manager_pb2
import csle_collector.constants.constants as constants


class ElkManagerServicer(csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerServicer):
    """
    gRPC server for managing an ELK stack. Allows to start/stop the ELK stack remotely and also to query the
    state of the ELK stack.
    """

    def __init__(self, ip : str=None, hostname :str = None,) -> None:
        """
        Initializes the server

        :param ip: the ip of the ELK server
        :param hostname: the hostname of the ELK server
        """
        logging.basicConfig(filename=f"/{constants.LOG_FILES.ELK_MANAGER_LOG_FILE}", level=logging.INFO)
        self.ip = ip
        self.hostname = hostname
        if self.hostname is None:
            self.hostname = socket.gethostname()
        if self.ip is None:
            self.ip = socket.gethostbyname(self.hostname)
        logging.info(f"Setting up ElkManager hostname: {self.hostname} ip: {self.ip}")

    def _get_elk_status(self) -> Tuple[bool,bool,bool]:
        """
        Utility method to get the status of the ELK stack

        :return: status of elastic, status of kibana, status of logstash
        """
        p = subprocess.Popen(constants.ELK.ELASTICSEARCH_STATUS, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        status_output = output.decode()
        elasticsearch_running = not ("not" in status_output)
        p = subprocess.Popen(constants.ELK.KIBANA_STATUS, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        status_output = output.decode()
        kibana_running = not ("not" in status_output)
        p = subprocess.Popen(constants.ELK.LOGSTASH_STATUS, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p.wait()
        status_output = output.decode()
        logstash_running = not ("not" in status_output)
        return elasticsearch_running, kibana_running, logstash_running

    def getElkStatus(self, request: csle_collector.elk_manager.elk_manager_pb2.GetElkStatusMsg,
                       context: grpc.ServicerContext) \
            -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Gets the state of the ELK server

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK stack server
        """
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning = elasticsearch_running,
            kibanaRunning = kibana_running, logstashRunning = logstash_running
        )
        return elk_dto

    def stopElk(self, request: csle_collector.elk_manager.elk_manager_pb2.StopElkMsg,
                    context: grpc.ServicerContext):
        """
        Stops the ELK stack

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK stack
        """
        logging.info("Stopping the ELK stack")
        logging.info("Stopping kibana")
        os.system(constants.ELK.KIBANA_STOP)
        logging.info("Stopping logstash")
        os.system(constants.ELK.LOGSTASH_STOP)
        logging.info("Stopping elasticsearch")
        os.system(constants.ELK.ELASTICSEARCH_STOP)
        return csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning = False, kibanaRunning = False, logstashRunning = False
        )

    def startElk(self, request: csle_collector.elk_manager.elk_manager_pb2.StartElkMsg,
                     context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Starts the ELK stack

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info(f"Starting ELK")
        os.system(constants.ELK.ELK_START)
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning = True, kibanaRunning = True, logstashRunning = True)
        return elk_dto

    def startElastic(self, request: csle_collector.elk_manager.elk_manager_pb2.StartElasticMsg,
                 context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Starts elasticsearch

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info(f"Starting Elasticsearch")
        os.system(constants.ELK.ELASTICSEARCH_START)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning = True, kibanaRunning = kibana_running, logstashRunning = logstash_running)
        return elk_dto

    def startKibana(self, request: csle_collector.elk_manager.elk_manager_pb2.StartKibanaMsg,
                     context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Starts Kibana

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info(f"Starting Kibana")
        os.system(constants.ELK.KIBANA_START)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning = elasticsearch_running, kibanaRunning = True, logstashRunning = logstash_running)
        return elk_dto

    def startLogstash(self, request: csle_collector.elk_manager.elk_manager_pb2.StartLogstashMsg,
                    context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Starts Logstash

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info(f"Starting Logstash")
        os.system(constants.ELK.LOGSTASH_START)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning = elasticsearch_running, kibanaRunning = kibana_running, logstashRunning =True)
        return elk_dto

    def stopElastic(self, request: csle_collector.elk_manager.elk_manager_pb2.StartElasticMsg,
                     context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Stops elasticsearch

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info(f"Stops Elasticsearch")
        os.system(constants.ELK.ELASTICSEARCH_STOP)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning = False, kibanaRunning = kibana_running, logstashRunning = logstash_running)
        return elk_dto

    def stopKibana(self, request: csle_collector.elk_manager.elk_manager_pb2.StopKibanaMsg,
                    context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Stops Kibana

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info(f"Stops Kibana")
        os.system(constants.ELK.KIBANA_STOP)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning = elasticsearch_running, kibanaRunning = False, logstashRunning = logstash_running)
        return elk_dto

    def stopLogstash(self, request: csle_collector.elk_manager.elk_manager_pb2.StopLogstashMsg,
                      context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Stops Logstash

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info(f"Stopping Logstash")
        os.system(constants.ELK.LOGSTASH_STOP)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(
            elasticRunning = elasticsearch_running, kibanaRunning = kibana_running, logstashRunning =False)
        return elk_dto

def serve(port : int = 50045, ip=None, hostname=None) -> None:
    """
    Starts the gRPC server for managing the ELK stack

    :param port: the port that the server will listen to
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    csle_collector.elk_manager.elk_manager_pb2_grpc.add_ElkManagerServicer_to_server(
        ElkManagerServicer(hostname=hostname, ip=ip), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"ElkManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve(port=50045)