import threading
import logging
import subprocess
import requests
import time
import json
import csle_collector.constants.constants as constants


class FailureDetector(threading.Thread):
    """
    Thread representing a client
    """

    def __init__(self, sleep_time: int, ip: str, ryu_web_port: int, ryu_port: int, controller: str, kafka_ip: str,
                 kafka_port: int, time_step_len: int) -> None:
        """
        Initializes the failure detector

        :param sleep_time: the period to check  for failures
        :param ip: the ip of the host
        :param ryu_web_port: the Ryu web port
        :param ryu_port: the Ryu port
        :param controller: the Ryu controller module
        :param kafka_ip: the Kafka IP
        :param kafka_port: the Kafka port
        :param time_step_len: the time-step length for Kafka logging
        """
        threading.Thread.__init__(self)
        self.sleep_time = sleep_time
        self.ip = ip
        self.ryu_web_port = ryu_web_port
        self.ryu_port = ryu_port
        self.controller = controller
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.time_step_len = time_step_len
        self.done = False

    def run(self) -> None:
        """
        The failure detector loop

        :return: None
        """
        self.done = False
        while not self.done:
            status_url = f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{self.ip}:{self.ryu_web_port}" \
                         f"{constants.RYU.STATUS_PRODUCER_HTTP_RESOURCE}"
            try:
                requests.get(status_url, timeout=constants.RYU.REQUEST_TIMEOUT_S)
            except Exception:
                logging.info("Restarting Ryu..")
                cmd = constants.RYU.STOP_RYU_CONTROLLER
                logging.info(f"Stopping ryu with command: {cmd}")
                result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
                logging.info(f"Stdout: {result.stdout}, stderr: {result.stderr}")
                cmd = constants.RYU.STOP_RYU_CONTROLLER_MANAGER
                logging.info(f"Stopping ryu with command: {cmd}")
                result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
                logging.info(f"Stdout: {result.stdout}, stderr: {result.stderr}")
                cmd = constants.RYU.START_RYU_CONTROLLER.format(self.ryu_port, self.ryu_web_port, self.controller)
                logging.info(f"Starting RYU controller with command: {cmd}")
                subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                time.sleep(5)
                start_url = f"{constants.HTTP.HTTP_PROTOCOL_PREFIX}{self.ip}:{self.ryu_web_port}" \
                            f"{constants.RYU.START_PRODUCER_HTTP_RESOURCE}"
                logging.info(f"Starting the RYU monitor by sending a PUT request to: {start_url}")
                requests.put(start_url, data=json.dumps({constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: self.kafka_ip,
                                                         constants.RYU.TIME_STEP_LEN_SECONDS: self.time_step_len}),
                             timeout=constants.RYU.REQUEST_TIMEOUT_S)
                logging.info("RYU monitor started")
            time.sleep(self.sleep_time)
