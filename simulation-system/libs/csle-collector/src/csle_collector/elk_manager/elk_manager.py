from typing import Tuple
import logging
import os
import subprocess
from concurrent import futures
import grpc
import socket
import netifaces
import csle_collector.elk_manager.elk_manager_pb2_grpc
import csle_collector.elk_manager.elk_manager_pb2
import csle_collector.constants.constants as constants


class ElkManagerServicer(csle_collector.elk_manager.elk_manager_pb2_grpc.ElkManagerServicer):
    """
    gRPC server for managing an ELK stack. Allows to start/stop the ELK stack remotely and also to query the
    state of the ELK stack.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename=f"{constants.LOG_FILES.ELK_MANAGER_LOG_DIR}"
                                     f"{constants.LOG_FILES.ELK_MANAGER_LOG_FILE}", level=logging.INFO)
        self.hostname = socket.gethostname()
        try:
            self.ip = netifaces.ifaddresses(constants.INTERFACES.ETH0)[netifaces.AF_INET][0][constants.INTERFACES.ADDR]
        except Exception:
            self.ip = socket.gethostbyname(self.hostname)
        logging.info(f"Setting up ElkManager hostname: {self.hostname} ip: {self.ip}")

    def _get_elk_status(self) -> Tuple[bool, bool, bool]:
        """
        Utility method to get the status of the ELK stack

        :return: status of elastic, status of kibana, status of logstash
        """
        status_output = subprocess.run(constants.ELK.ELASTICSEARCH_STATUS.split(" "),
                                       capture_output=True, text=True).stdout
        elasticsearch_running = not ("not" in status_output)
        status_output = subprocess.run(constants.ELK.KIBANA_STATUS.split(" "),
                                       capture_output=True, text=True).stdout
        kibana_running = not ("not" in status_output)
        status_output = subprocess.run(constants.ELK.LOGSTASH_STATUS.split(" "),
                                       capture_output=True, text=True).stdout
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
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(elasticRunning=elasticsearch_running,
                                                                    kibanaRunning=kibana_running,
                                                                    logstashRunning=logstash_running)
        return elk_dto

    def stopElk(self, request: csle_collector.elk_manager.elk_manager_pb2.StopElkMsg, context: grpc.ServicerContext) \
            -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
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
        return csle_collector.elk_manager.elk_manager_pb2.ElkDTO(elasticRunning=False, kibanaRunning=False,
                                                                 logstashRunning=False)

    def startElk(self, request: csle_collector.elk_manager.elk_manager_pb2.StartElkMsg,
                 context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Starts the ELK stack

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info("Starting ELK")
        os.system(constants.ELK.ELK_START)
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(elasticRunning=True, kibanaRunning=True,
                                                                    logstashRunning=True)
        return elk_dto

    def startElastic(self, request: csle_collector.elk_manager.elk_manager_pb2.StartElasticMsg,
                     context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Starts elasticsearch

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info("Starting Elasticsearch")
        os.system(constants.ELK.ELASTICSEARCH_START)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(elasticRunning=True, kibanaRunning=kibana_running,
                                                                    logstashRunning=logstash_running)
        return elk_dto

    def startKibana(self, request: csle_collector.elk_manager.elk_manager_pb2.StartKibanaMsg,
                    context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Starts Kibana

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info("Starting Kibana")
        os.system(constants.ELK.KIBANA_START)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(elasticRunning=elasticsearch_running,
                                                                    kibanaRunning=True,
                                                                    logstashRunning=logstash_running)
        return elk_dto

    def startLogstash(self, request: csle_collector.elk_manager.elk_manager_pb2.StartLogstashMsg,
                      context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Starts Logstash

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info("Starting Logstash")
        os.system(constants.ELK.LOGSTASH_START)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(elasticRunning=elasticsearch_running,
                                                                    kibanaRunning=kibana_running,
                                                                    logstashRunning=True)
        return elk_dto

    def stopElastic(self, request: csle_collector.elk_manager.elk_manager_pb2.StartElasticMsg,
                    context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Stops elasticsearch

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info("Stops Elasticsearch")
        os.system(constants.ELK.ELASTICSEARCH_STOP)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(elasticRunning=False, kibanaRunning=kibana_running,
                                                                    logstashRunning=logstash_running)
        return elk_dto

    def stopKibana(self, request: csle_collector.elk_manager.elk_manager_pb2.StopKibanaMsg,
                   context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Stops Kibana

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info("Stops Kibana")
        os.system(constants.ELK.KIBANA_STOP)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(elasticRunning=elasticsearch_running,
                                                                    kibanaRunning=False,
                                                                    logstashRunning=logstash_running)
        return elk_dto

    def stopLogstash(self, request: csle_collector.elk_manager.elk_manager_pb2.StopLogstashMsg,
                     context: grpc.ServicerContext) -> csle_collector.elk_manager.elk_manager_pb2.ElkDTO:
        """
        Stops Logstash

        :param request: the gRPC request
        :param context: the gRPC context
        :return: an ElkDTO with the state of the ELK server
        """
        logging.info("Stopping Logstash")
        os.system(constants.ELK.LOGSTASH_STOP)
        elasticsearch_running, kibana_running, logstash_running = self._get_elk_status()
        elk_dto = csle_collector.elk_manager.elk_manager_pb2.ElkDTO(elasticRunning=elasticsearch_running,
                                                                    kibanaRunning=kibana_running,
                                                                    logstashRunning=False)
        return elk_dto


def serve(port: int = 50045, log_dir: str = "/", max_workers: int = 10,
          log_file_name: str = "elk_manager.log") -> None:
    """
    Starts the gRPC server for managing the ELK stack

    :param port: the port that the server will listen to
    :param log_dir: the directory to write the log file
    :param log_file_name: the file name of the log
    :param max_workers: the maximum number of GRPC workers
    :return: None
    """
    constants.LOG_FILES.ELK_MANAGER_LOG_DIR = log_dir
    constants.LOG_FILES.ELK_MANAGER_LOG_FILE = log_file_name
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    csle_collector.elk_manager.elk_manager_pb2_grpc.add_ElkManagerServicer_to_server(
        ElkManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"ElkManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve()
