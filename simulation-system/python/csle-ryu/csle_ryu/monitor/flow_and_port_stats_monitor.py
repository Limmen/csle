from confluent_kafka import Producer
import json
import socket
from operator import attrgetter
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.lib import hub
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.app.wsgi import ControllerBase
from ryu.app.wsgi import Response
from ryu.app.wsgi import route
from ryu.app.wsgi import WSGIApplication
import csle_ryu.constants.constants as constants


class FlowAndPortStatsMonitor(app_manager.RyuApp):
    """
    Contains general functionality to monitor of flow and port statistics
    """

    # OpenFlow version to use
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Include WSGI context for the northbound API
    # Specifyies Ryu's WSGI-compatible Web server clas to use
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        """
        Initializes the class

        :param args: app arguments
        :param kwargs: app arguments
        """
        super(FlowAndPortStatsMonitor, self).__init__(*args, **kwargs)

        # Dict to keep track of all connected switches
        self.datapaths = {}

        # Thread which will periodically query switches for statistics
        self.monitor_thread = hub.spawn(self._monitor)

        # State
        self.kafka_conf = {}
        self.producer_running = False
        self.producer = None

        # Acquires the the WSGIApplication to register the controller class
        self.logger.info(f"Registering CSLE Northbound REST API Controller")
        wsgi = kwargs['wsgi']
        wsgi.register(NorthBoundRestAPIController, {"controller_app": self})


    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev) -> None:
        """
        Handler called whenever a new switch connects or disconnects from the controller.
        MAIN_DISPATCHER corresponds to the event that a new switch connects and DEAD_DISPATCHER corresponds to the
        event that a switch disconnects

        :param ev: the connection event
        :return: None
        """

        # Extract the datapath (abstraction of the link to the switch) that the event concerns
        datapath = ev.datapath

        if ev.state == MAIN_DISPATCHER:
            # A new switch connected
            if datapath.id not in self.datapaths:
                # If the switch was not already registered, add it to the datapath dict.
                self.logger.info(f"A new switch connection, DPID:{datapath.id}")
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                # Remove the switch from the dict of datapaths since it disconnected.
                self.logger.info(f"Switch with DPID:{datapath.id} disconnected")
                del self.datapaths[datapath.id]

    def _monitor(self) -> None:
        """
        Thread that periodically sends requests to the connected switches to get switch statistics

        :return: None
        """
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(10)

    def _request_stats(self, datapath) -> None:
        """
        Utility function for sending a request to a switch with a qiven datapath to return its flow and port statistics.

        :param datapath: the datapath, i.e. abstraction of the link to the switch
        :return: None
        """
        self.logger.info(f"Sending a request to switch with DPID:{datapath.id} to return its flow and port statistics")

        # Extract the protocol and message parser to use for sending the request
        openflow_protocol = datapath.ofproto
        parser = datapath.ofproto_parser

        # Prepare the request for flow statistics
        statistics_request = parser.OFPFlowStatsRequest(datapath)

        # Send the request to get the flow statistics of the switch
        datapath.send_msg(statistics_request)

        # Prepare the request for port statistics
        statistics_request = parser.OFPPortStatsRequest(datapath, 0, openflow_protocol.OFPP_ANY)

        # Send the request to get the port statistics of the switch
        datapath.send_msg(statistics_request)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev) -> None:
        """
        Handler called when a flow statistics response is received from a switch

        :param ev: the response event
        :return: None
        """

        # Extract the response body
        body = ev.msg.body

        # Log the statistics
        self.logger.info(f"--- Flow statistics for switch with DPID {ev.msg.datapath.id} ---")
        self.logger.info('datapath         '
                         'in-port  eth-dst           '
                         'out-port packets  bytes')
        self.logger.info('---------------- '
                         '-------- ----------------- '
                         '-------- -------- --------')
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            self.logger.info(f"{ev.msg.datapath.id} {stat.match['in_port']} {stat.match['eth_dst']} "
                             f"{stat.instructions[0].actions[0].port} {stat.packet_count} {stat.byte_count}")

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev) -> None:
        """
        Handler called when a port statistics response is received from a switch

        :param ev: the response event
        :return: None
        """

        # Extract the response body
        body = ev.msg.body

        # Log the statistics
        self.logger.info(f"--- Port statistics for switch with DPID {ev.msg.datapath.id} ---")

        self.logger.info('datapath         port     '
                         'rx-pkts  rx-bytes rx-error '
                         'tx-pkts  tx-bytes tx-error')
        self.logger.info('---------------- -------- '
                         '-------- -------- -------- '
                         '-------- -------- --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info(f"{ev.msg.datapath.id} {stat.port_no} {stat.rx_packets} {stat.rx_bytes} {stat.rx_errors} "
                             f"{stat.tx_packets} {stat.tx_bytes} {stat.tx_errors}")


class NorthBoundRestAPIController(ControllerBase):
    """
    Controller class for the Northbound REST API that accepts HTTP requests.

    Example requests:

    curl -X GET http://15.12.252.3:8080/cslenorthboundapi/producer/status
    curl -X PUT -d '{"bootstrap.servers": "test"}' http://15.12.252.3:8080/cslenorthboundapi/producer/start
    curl -X POST http://15.12.252.3:8080/cslenorthboundapi/producer/start
    """

    def __init__(self, req, link, data, **config):
        super(NorthBoundRestAPIController, self).__init__(req, link, data, **config)
        self.controller_app = data["controller_app"] # These names has to match!
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)

    @route('controller_app', "/cslenorthboundapi/producer/status", methods=['GET'])
    def producer_status(self, req, **kwargs):
        """
        Gets the status of the Kafka producer

        :param req: the REST API request
        :param kwargs: the WSGI arguments
        :return: the REST API response
        """
        response_body = json.dumps({"kafka_conf": self.controller_app.kafka_conf,
                                    "producer_running": self.controller_app.producer_running})
        return Response(content_type='application/json', text=response_body)

    @route('controller_app', "/cslenorthboundapi/producer/start", methods=['PUT'])
    def start_producer(self, req, **kwargs) -> None:
        """
        Starts the Kafka producer that sends flow and port statistics

        :param req: the REST API request
        :param kwargs: WSGI arguments
        :return: the REST API response
        """
        try:
            kafka_conf = req.json if req.body else {}
        except ValueError:
            raise Response(status=400)
        if constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY in kafka_conf:
            self.controller_app.kafka_conf = {
                constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: kafka_conf[constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY],
                constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
            self.controller_app.logger.info(f"Starting Kafka producer with conf: {self.controller_app.kafka_conf}")
            self.controller_app.producer_running = True
            self.controller_app.producer = Producer(**self.controller_app.kafka_conf)
            body = json.dumps(self.controller_app.kafka_conf)
            return Response(content_type='application/json', text=body, status=200)
        else:
            return Response(status=500)

    @route('controller_app', "/cslenorthboundapi/producer/stop", methods=['POST'])
    def stop_producer(self, req, **kwargs):
        """
        Stops the Kafka producer that sends flow and port statistics

        :param req: the REST API request
        :param kwargs: WSGI arguments
        :return: The REST response
        """
        self.controller_app.logger.info(f"Stopping Kafka producer")
        self.controller_app.kafka_conf = {}
        self.controller_app.producer_running = False
        self.controller_app.producer = None
        response_body = json.dumps({"kafka_conf": self.controller_app.kafka_conf,
                                    "producer_running": self.controller_app.producer_running})
        return Response(content_type='application/json', text=response_body, status=200)