from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from csle_ryu.dao.ryu_controller_type import RYUControllerType
from csle_ryu.monitor.flow_and_port_stats_monitor import FlowAndPortStatsMonitor
import csle_ryu.constants.constants as constants
from ryu.lib import stplib


class LearningSwitchSTPController(FlowAndPortStatsMonitor):
    """
    RYU Controller implementing a learning L2 switch for OpenFlow 1.3 with the STP spanning tree protocol

    To avoid the problems associated with redundant links in a switched LAN,
    STP is implemented on switches to monitor the network topology. Every link between switches,
    and in particular redundant links, are catalogued.
    The spanning-tree algorithm then blocks forwarding on redundant links by setting up one preferred link
    between switches in the LAN. This preferred link is used for all Ethernet frames unless it fails,
    in which case a non-preferred redundant link is enabled. When implemented in a network,
    STP designates one layer-2 switch as root bridge. All switches then select their best connection
    towards the root bridge for forwarding and block other redundant links.
    All switches constantly communicate with their neighbors in the LAN using bridge protocol data units (BPDUs)
    """

    # Spanning tree protocol to use
    _CONTEXTS = {'stplib': stplib.Stp}

    def __init__(self, *args, **kwargs):
        """
        Initializes  the switch

        :param args: RYU arguments
        :param kwargs: RYU arguments
        """
        super(LearningSwitchSTPController, self).__init__(*args, **kwargs)

        # MAC-to-PORT table to be learned
        self.mac_to_port = {}

        # The spanning tree protocol version version
        self.stp = kwargs['stplib']

        # Controller type
        self.controller_type = RYUControllerType.LEARNING_SWITCH_STP

    def delete_flow(self, datapath) -> None:
        """
        Utility function for instructing a switch to delete all flows that have been installed

        :param datapath: the datapath, i.e. abstraction of the link to the switch
        :return: None
        """

        # Extract protcol version and OF parser
        openflow_protocol = datapath.ofproto
        parser = datapath.ofproto_parser

        for dst_mac_address in self.mac_to_port[datapath.id].keys():
            # Match all flows with the given MAC address as destination
            match = parser.OFPMatch(eth_dst=dst_mac_address)

            # Create an OpenFlow Modify-State message to remove the flow
            mod = parser.OFPFlowMod(
                datapath, command=openflow_protocol.OFPFC_DELETE,
                out_port=openflow_protocol.OFPP_ANY, out_group=openflow_protocol.OFPG_ANY,
                priority=1, match=match)

            # Send the message to the switch
            datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev) -> None:
        """
        Handler called after OpenFlow handshake with switch completed. It adds teh Table-miss flow entry to
        the flow tables of the switch so that next packet which yield a flow-table-miss will be sent to the
        controller

        :param ev: the handshake complete event
        :return: None
        """
        # the datapath, i.e. abstraction of the link to the switch
        datapath = ev.msg.datapath

        self.logger.info(f"[SDN-Controller {self.controller_type}] OpenFlow handshake with switch DPID:{datapath.id}, "
                         f"completed, adding the default flow-miss entry to the table")

        # Extract version and packet parser
        openflow_protocol = datapath.ofproto
        parser = datapath.ofproto_parser

        # Configure the table-miss flow to install at the table

        # First, setup the matcher that will match packets to flows based on the headers
        # It should match any packet
        match = parser.OFPMatch()

        # Second, define action when flows are matched
        actions = [parser.OFPActionOutput(openflow_protocol.OFPP_CONTROLLER, constants.RYU.PACKET_BUFFER_MAX_LEN)]

        # Third, define the priority, we set the lowest priority so that this flow rule is matched only if no other
        # flow is matched
        priority = 0

        # Send request to the switch to add the flow
        self.add_flow(datapath, priority, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None) -> None:
        """
        Utility method for adding a flow to a switch

        :param datapath: the datapath, i.e. abstraction of the link to the switch
        :param priority: the priority of the flow (higher priority are prioritized)
        :param match: the pattern for matching packets to the flow based on the header
        :param actions: the actions to take when the flow is matched, e.g. where to send the packet
        :param buffer_id: the id of the buffer where packets for this flow are queued if they cannot be sent
        :return: None
        """
        openflow_protocol = datapath.ofproto  # Extract the openflow protocol used for communicating with the switch
        parser = datapath.ofproto_parser  # extract packet parser

        # Define the instruction that the switch should perform if the flow is matched
        instruction = [parser.OFPInstructionActions(openflow_protocol.OFPIT_APPLY_ACTIONS, actions)]

        # Create an OpenFlow Modify-State message to add a new flow
        if buffer_id is not None:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=instruction)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=instruction)

        # Send the message to the switch
        datapath.send_msg(mod)

    @set_ev_cls(stplib.EventPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev) -> None:
        """
        Handler called when the switch has received a packet with an unknown destination and thus forwards
        the packet to the controller. Excludes BPDU (bridge protocol data units) packets that are part of the
        STP protocol.

        :param ev: the packet-in-event
        :return: None
        """

        # Extract metadata from the event received from the switch
        msg = ev.msg
        datapath = msg.datapath

        # Extract message protocol, parser, input port, ethernet protocol, and source and destination MAC addresses
        openflow_protocol = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        dst_mac_address = eth.dst
        src_mac_address = eth.src

        # Each switch is identified by a datapath 64-bit ID (DPID) containing the 48-bit MAC address
        # as well as 16-bit additional ID bits
        datapath_id = datapath.id

        # Initialize empty row in the mac-to-port table
        self.mac_to_port.setdefault(datapath_id, {})

        self.logger.info(f"[SDN-Controller {self.controller_type}] received packet in, DPID:{datapath_id}, "
                         f"src_mac_address:{src_mac_address}, dst_mac_address:{dst_mac_address}, port number:{in_port}")

        # learn a mac address to avoid FLOOD next time, i.e. map the port of the switch to the source MAC address
        self.mac_to_port[datapath_id][src_mac_address] = in_port

        if dst_mac_address in self.mac_to_port[datapath_id]:
            # If the destination MAC address already exists in the table, lookup the corresponding port
            out_port = self.mac_to_port[datapath_id][dst_mac_address]
        else:
            # If the destination MAC address does not exist in the table, tell the switch to send a flood message
            out_port = openflow_protocol.OFPP_FLOOD

        # Prepare the actions to be sent to the switch
        actions = [parser.OFPActionOutput(out_port)]

        # If the destination MAC already has been learned, install a flow in the switch that tells the switch
        # which outgoing port it should use whenever it receives frames that matches the given source port, source MAC,
        # and destination MAC. This defines a flow. This means that next time a frame of this flow is identified,
        # the switch does not need to flood the LAN, it can just lookup the correct destination port from the
        # flow table.
        if out_port != openflow_protocol.OFPP_FLOOD:
            # Create a matcher object which defines how packets are matched to the flow
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst_mac_address)

            # Add the flow to the switch with priority 1.
            self.add_flow(datapath, 1, match, actions)

        # The switch normally keeps packet it does not know how to forward in a queue/buffer. We extract the
        # buffer id from the openflow event. However if the switch does not use buffering, it will send the complete
        # data message to the controller. In this case, we need to send the data back to the switch, otherwise
        # it will be lost.
        data = None
        if msg.buffer_id == openflow_protocol.OFP_NO_BUFFER:
            data = msg.data

        # Prepare OFP message to send to the switch and instruct it what to do with this packet.
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        # Send the message to the Switch
        datapath.send_msg(out)

    @set_ev_cls(stplib.EventTopologyChange, MAIN_DISPATCHER)
    def _topology_change_handler(self, ev) -> None:
        """
        Handler called when a topology change has been detected by the STP protocol

        :param ev: the topology change event
        :return:
        """
        # Extract the datapath (abstraction of the communication link to the switch)
        datapath = ev.dp

        self.logger.info(f"[SDN-Controller {self.controller_type}] received topology change event from "
                         f"DPID:{datapath.id}, "
                         f"flushing the MAC table and deleting installed flows")

        # If we have flows installed for this switch and learned mac-to-port mappings, delete them
        if datapath.id in self.mac_to_port:
            self.delete_flow(datapath)
            del self.mac_to_port[datapath.id]

    @set_ev_cls(stplib.EventPortStateChange, MAIN_DISPATCHER)
    def _port_state_change_handler(self, ev) -> None:
        """
        Handler called when the controller receives a message from the switch which indicates that one of its
        ports has changed

        :param ev: the port-change evnet
        :return: None
        """
        datapath_id = ev.dp.id

        # Extract metadata from the received OpenFlow event
        port_no = ev.port_no

        # Map port state to strings for logging
        openflow_state = {stplib.PORT_STATE_DISABLE: 'DISABLE', stplib.PORT_STATE_BLOCK: 'BLOCK',
                          stplib.PORT_STATE_LISTEN: 'LISTEN', stplib.PORT_STATE_LEARN: 'LEARN',
                          stplib.PORT_STATE_FORWARD: 'FORWARD'}

        self.logger.info(f"[SDN-Controller {self.controller_type}] a port {port_no} was modified on switch with "
                         f"DPID: {datapath_id}. Port state: {openflow_state[ev.port_state]}")
