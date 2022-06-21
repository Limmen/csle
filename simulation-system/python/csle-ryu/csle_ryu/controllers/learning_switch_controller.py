from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from csle_ryu.dao.ryu_controller_type import RYUControllerType
from csle_ryu.monitor.flow_and_port_stats_monitor import FlowAndPortStatsMonitor


class LearningSwitchController(FlowAndPortStatsMonitor):
    """
    RYU Controller implementing a learning L2 switch
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes  the switch

        :param args: RYU arguments
        :param kwargs: RYU arguments
        """
        super(LearningSwitchController, self).__init__(*args, **kwargs)

        # MAC-to-PORT table to be learned
        self.mac_to_port = {}

        # Controller type
        self.controller_type = RYUControllerType.LEARNING_SWITCH

    def add_flow(self, datapath, in_port, dst, src, actions) -> None:
        """
        Utility method for adding a flow to a switch

        :param datapath: the datapath, i.e. abstraction of the link to the switch
        :param in_port: the incoming port for matching the flow
        :param dst: the destination address for matching the flow
        :param src: the source address for matching the flow
        :param actions: the actions to take when the flow is matched, e.g. where to send the packet
        :return: None
        """
        openflow_protocol = datapath.ofproto # Extract the openflow protocol used for communicating with the switch

        # Create a match pattern that the switch should use to match incoming packet headers to flows.
        # The match pattern includes the incoming port, the destination address (MAC or IP),
        # and the source address (MAC or IP)
        match = datapath.ofproto_parser.OFPMatch(in_port=in_port, dl_dst=haddr_to_bin(dst), dl_src=haddr_to_bin(src))

        # Create an OpenFlow Modify-State message to add a new flow
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=openflow_protocol.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=openflow_protocol.OFP_DEFAULT_PRIORITY,
            flags=openflow_protocol.OFPFF_SEND_FLOW_REM, actions=actions)

        # Send the message to the switch
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev) -> None:
        """
        Handler called when the switch has received a packet with an unknown destination and thus forwards
        the packet to the controller

        :param ev: the packet-in-event
        :return: None
        """

        # Extract metadata from the event received from the switch
        msg = ev.msg
        datapath = msg.datapath
        openflow_protocol = datapath.ofproto
        pkt = packet.Packet(msg.data) # Create a Packet object from the event data
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore link-layer discovery protocol (lldp) packet
            return
        dst_mac_address = eth.dst
        src_mac_address = eth.src
        # Each switch is identified by a datapath 64-bit ID (DPID) containing the 48-bit MAC address
        # as well as 16-bit additional ID bits
        datapath_id = datapath.id
        self.mac_to_port.setdefault(datapath_id, {})

        self.logger.info(f"[SDN-Controller {self.controller_type}] received packet in, DPID:{datapath_id}, "
                     f"src_mac_address:{src_mac_address}, dst_mac_address:{dst_mac_address}, port number:{msg.in_port}")

        # learn a mac address to avoid FLOOD next time, i.e. map the port of the switch to the source MAC address
        self.mac_to_port[datapath_id][src_mac_address] = msg.in_port

        if dst_mac_address in self.mac_to_port[datapath_id]:
            # If the destination MAC address already exists in the table, lookup the corresponding port
            out_port = self.mac_to_port[datapath_id][dst_mac_address]
        else:
            # If the destination MAC address does not exist in the table, tell the switch to send a flood message
            out_port = openflow_protocol.OFPP_FLOOD

        # Prepare the actions to be sent to the switch
        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # If the destination MAC already has been learned, install a flow in the switch that tells the switch
        # which outgoing port it should use whenever it receives frames that matches the given source port, source MAC,
        # and destination MAC. This defines a flow. This means that next time a frame of this flow is identified,
        # the switch does not need to flood the LAN, it can just lookup the correct destination port from the
        # flow table.
        if out_port != openflow_protocol.OFPP_FLOOD:
            self.add_flow(datapath, msg.in_port, dst_mac_address, src_mac_address, actions)

        # The switch normally keeps packet it does not know how to forward in a queue/buffer. We extract the
        # buffer id from the openflow event. However if the switch does not use buffering, it will send the complete
        # data message to the controller. In this case, we need to send the data back to the switch, otherwise
        # it will be lost.
        data = None
        if msg.buffer_id == openflow_protocol.OFP_NO_BUFFER:
            data = msg.data

        # Prepare OFP message to send to the switch and instruct it what to do with this packet.
        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions, data=data)

        # Send the message to the Switch
        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def _port_status_handler(self, ev) -> None:
        """
        Handler called when the controller receives a message from the switch which indicates that one of its
        ports has changed

        :param ev: the port-change evnet
        :return: None
        """

        # Extract metadata from the received OpenFlow event
        msg = ev.msg
        reason = msg.reason
        port_no = msg.desc.port_no
        openflow_protocol = msg.datapath.ofproto
        datapath = msg.datapath
        datapath_id = datapath.id

        if reason == openflow_protocol.OFPPR_ADD:
            self.logger.info(f"[SDN-Controller {self.controller_type}] a port {port_no} was added to switch with "
                         f"DPID: {datapath_id}")
        elif reason == openflow_protocol.OFPPR_DELETE:
            self.logger.info(f"[SDN-Controller {self.controller_type}] port {port_no} was removed from switch with "
                         f"DPID: {datapath_id}")
        elif reason == openflow_protocol.OFPPR_MODIFY:
            self.logger.info(f"[SDN-Controller {self.controller_type}] port {port_no} on switch with "
                         f"DPID: {datapath_id} was modified")
        else:
            self.logger.info(f"[SDN-Controller {self.controller_type}] Illegal port state: {port_no}, {reason}")