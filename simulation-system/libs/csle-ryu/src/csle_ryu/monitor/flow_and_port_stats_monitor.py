from confluent_kafka import Producer
import json
import socket
import time
import requests
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
import csle_collector.constants.constants as collector_constants
import csle_ryu.constants.constants as constants
from csle_ryu.dao.flow_statistic import FlowStatistic
from csle_ryu.dao.port_statistic import PortStatistic
from csle_ryu.dao.avg_flow_statistic import AvgFlowStatistic
from csle_ryu.dao.avg_port_statistic import AvgPortStatistic
from csle_ryu.dao.agg_flow_statistic import AggFlowStatistic


class FlowAndPortStatsMonitor(app_manager.RyuApp):
    """
    Contains general functionality to monitor of flow and port statistics
    """

    # OpenFlow version to use
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Include WSGI context for the northbound API
    # Specifyies Ryu's WSGI-compatible Web server clas to use
    _CONTEXTS = {constants.RYU.WSGI: WSGIApplication}

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
        self.time_step_len_seconds = 30

        # Acquires the the WSGIApplication to register the controller class
        self.logger.info("Registering CSLE Northbound REST API Controller")
        wsgi = kwargs[constants.RYU.WSGI]
        wsgi.register(NorthBoundRestAPIController, {constants.RYU.CONTROLLER_APP: self})

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
            if self.producer_running:
                for dp in self.datapaths.values():
                    self._request_stats(dp)
                    try:
                        response = requests.get(f"{collector_constants.HTTP.HTTP_PROTOCOL_PREFIX}"
                                                f"{collector_constants.HTTP.LOCALHOST}:8080"
                                                f"{constants.RYU.STATS_AGGREGATE_FLOW_RESOURCE}/{dp.id}",
                                                timeout=constants.RYU.TIMEOUT)
                        aggflows = json.loads(response.content)[str(dp.id)][0]
                        agg_flow_stat = AggFlowStatistic(timestamp=time.time(), datapath_id=str(dp.id),
                                                         total_num_bytes=aggflows[constants.RYU.BYTE_COUNT],
                                                         total_num_packets=aggflows[constants.RYU.PACKET_COUNT],
                                                         total_num_flows=aggflows[constants.RYU.FLOW_COUNT])
                        if self.producer is not None and self.producer_running:
                            self.producer.produce(collector_constants.KAFKA_CONFIG.OPENFLOW_AGG_FLOW_STATS_TOPIC_NAME,
                                                  agg_flow_stat.to_kafka_record())
                            self.producer.poll(0)
                    except Exception as e:
                        self.logger.warning(f"There was an error parsing the flow statistics: {str(e)}, {repr(e)}")
            hub.sleep(self.time_step_len_seconds)

    def _request_stats(self, datapath) -> None:
        """
        Utility function for sending a request to a switch with a qiven datapath to return its flow and port statistics.

        :param datapath: the datapath, i.e., abstraction of the link to the switch
        :return: None
        """
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
        ts = time.time()

        # Log the statistics
        flow_stats = []
        for flow in body:
            in_port = ""
            eth_dst = ""
            if constants.RYU.IN_PORT in flow.match:
                in_port = flow.match[constants.RYU.IN_PORT]
            if constants.RYU.ETH_DST in flow.match:
                eth_dst = flow.match[constants.RYU.ETH_DST]
            flow_statistic_dto = FlowStatistic(
                timestamp=ts, datapath_id=str(ev.msg.datapath.id), in_port=in_port,
                out_port=flow.instructions[0].actions[0].port, dst_mac_address=eth_dst,
                num_packets=flow.packet_count,
                num_bytes=flow.byte_count, duration_nanoseconds=flow.duration_nsec,
                duration_seconds=flow.duration_sec,
                hard_timeout=flow.hard_timeout, idle_timeout=flow.idle_timeout, priority=flow.priority,
                cookie=flow.cookie
            )
            if self.producer is not None and self.producer_running:
                self.producer.produce(collector_constants.KAFKA_CONFIG.OPENFLOW_FLOW_STATS_TOPIC_NAME,
                                      flow_statistic_dto.to_kafka_record())
                self.producer.poll(0)
                flow_stats.append(flow_statistic_dto)

        if self.producer is not None and self.producer_running and len(flow_stats) > 0:
            avg_flow_stats = AvgFlowStatistic.average_flow_statistics(
                timestamp=ts, datapath_id=str(flow_stats[0].datapath_id), flow_statistics=flow_stats)
            self.producer.produce(collector_constants.KAFKA_CONFIG.AVERAGE_OPENFLOW_FLOW_STATS_PER_SWITCH_TOPIC_NAME,
                                  avg_flow_stats.to_kafka_record())
            self.producer.poll(0)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev) -> None:
        """
        Handler called when a port statistics response is received from a switch

        :param ev: the response event
        :return: None
        """

        # Extract the response body
        body = ev.msg.body
        ts = time.time()

        port_stats = []

        # Log the statistics
        for port in body:
            port_statistics_dto = PortStatistic(
                timestamp=ts, datapath_id=str(ev.msg.datapath.id), port=port.port_no,
                num_received_packets=port.rx_packets,
                num_received_bytes=port.rx_bytes, num_received_errors=port.rx_errors,
                num_transmitted_packets=port.tx_packets, num_transmitted_bytes=port.tx_bytes,
                num_transmitted_errors=port.tx_errors, num_received_dropped=port.rx_dropped,
                num_transmitted_dropped=port.tx_dropped, num_received_frame_errors=port.rx_frame_err,
                num_received_overrun_errors=port.rx_over_err, num_received_crc_errors=port.rx_crc_err,
                num_collisions=port.collisions, duration_nanoseconds=port.duration_nsec,
                duration_seconds=port.duration_sec
            )
            if self.producer is not None and self.producer_running:
                self.producer.produce(collector_constants.KAFKA_CONFIG.OPENFLOW_PORT_STATS_TOPIC_NAME,
                                      port_statistics_dto.to_kafka_record())
                self.producer.poll(0)
                port_stats.append(port_statistics_dto)

        if self.producer is not None and self.producer_running and len(port_stats) > 0:
            avg_flow_stats = AvgPortStatistic.average_port_statistics(
                timestamp=ts, datapath_id=str(port_stats[0].datapath_id), port_statistics=port_stats)
            self.producer.produce(collector_constants.KAFKA_CONFIG.AVERAGE_OPENFLOW_PORT_STATS_PER_SWITCH_TOPIC_NAME,
                                  avg_flow_stats.to_kafka_record())
            self.producer.poll(0)


class NorthBoundRestAPIController(ControllerBase):
    """
    Controller class for the Northbound REST API that accepts HTTP requests.

    Example requests:

    curl -X GET http://15.12.252.3:8080/cslenorthboundapi/producer/status
    curl -X PUT -d '{"bootstrap.servers": "15.12.253.253", "time_step_len_seconds": 30}'
    http://15.12.252.3:8080/cslenorthboundapi/producer/start
    curl -X POST http://15.12.252.3:8080/cslenorthboundapi/producer/stop
    """

    def __init__(self, req, link, data, **config):
        """
        Initializes the controller

        :param req: the request for the initialization
        :param link: the link on which the controller was started
        :param data: the data
        :param config: configuration parameters
        """
        super(NorthBoundRestAPIController, self).__init__(req, link, data, **config)
        self.controller_app = data[constants.RYU.CONTROLLER_APP]  # These names have to match!
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)

    @route(constants.RYU.CONTROLLER_APP, collector_constants.RYU.STATUS_PRODUCER_HTTP_RESOURCE,
           methods=[collector_constants.HTTP.GET])
    def producer_status(self, req, **kwargs):
        """
        Gets the status of the Kafka producer

        :param req: the REST API request
        :param kwargs: the WSGI arguments
        :return: the REST API response
        """
        response_body = json.dumps({
            constants.RYU.KAFKA_CONF: self.controller_app.kafka_conf,
            constants.RYU.PRODUCER_RUNNING: self.controller_app.producer_running,
            collector_constants.RYU.TIME_STEP_LEN_SECONDS: self.controller_app.time_step_len_seconds})
        return Response(content_type=collector_constants.HTTP.APPLICATION_JSON_TYPE, text=response_body)

    @route(constants.RYU.CONTROLLER_APP, collector_constants.RYU.START_PRODUCER_HTTP_RESOURCE,
           methods=[collector_constants.HTTP.PUT])
    def start_producer(self, req, **kwargs):
        """
        Starts the Kafka producer that sends flow and port statistics

        :param req: the REST API request
        :param kwargs: WSGI arguments
        :return: the REST API response
        """
        try:
            kafka_conf = req.json if req.body else {}
        except ValueError:
            return Response(status=collector_constants.HTTP.BAD_REQUEST_RESPONSE_CODE)
        if collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY in kafka_conf \
                and collector_constants.RYU.TIME_STEP_LEN_SECONDS in kafka_conf:
            self.controller_app.kafka_conf = {
                collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: kafka_conf[
                    collector_constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY],
                collector_constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
            self.controller_app.logger.info(f"Starting Kafka producer with conf: {self.controller_app.kafka_conf}")
            self.controller_app.producer_running = True
            self.controller_app.producer = Producer(**self.controller_app.kafka_conf)
            self.controller_app.time_step_len_seconds = kafka_conf[collector_constants.RYU.TIME_STEP_LEN_SECONDS]
            body = json.dumps(self.controller_app.kafka_conf)
            return Response(content_type=collector_constants.HTTP.APPLICATION_JSON_TYPE, text=body,
                            status=collector_constants.HTTP.OK_RESPONSE_CODE)
        else:
            return Response(status=collector_constants.HTTP.INTERNAL_SERVER_ERROR_RESPONSE_CODE)

    @route(constants.RYU.CONTROLLER_APP, collector_constants.RYU.STOP_PRODUCER_HTTP_RESOURCE,
           methods=[collector_constants.HTTP.POST])
    def stop_producer(self, req, **kwargs):
        """
        Stops the Kafka producer that sends flow and port statistics

        :param req: the REST API request
        :param kwargs: WSGI arguments
        :return: The REST response
        """
        self.controller_app.logger.info("Stopping Kafka producer")
        self.controller_app.kafka_conf = {}
        self.controller_app.producer_running = False
        self.controller_app.producer = None
        response_body = json.dumps({constants.RYU.KAFKA_CONF: self.controller_app.kafka_conf,
                                    constants.RYU.PRODUCER_RUNNING: self.controller_app.producer_running,
                                    collector_constants.RYU.TIME_STEP_LEN_SECONDS:
                                        self.controller_app.time_step_len_seconds})
        return Response(content_type=collector_constants.HTTP.APPLICATION_JSON_TYPE, text=response_body,
                        status=collector_constants.HTTP.OK_RESPONSE_CODE)
