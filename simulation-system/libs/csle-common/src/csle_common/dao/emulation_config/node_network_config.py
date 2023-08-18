"""
Network configuration of a container in the emulation
"""
from typing import Dict, Any
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
import csle_common.constants.constants as constants
from csle_base.json_serializable import JSONSerializable


class NodeNetworkConfig(JSONSerializable):
    """
    A DTO object representing the network configuration of a specific container in an emulation environment
    """

    def __init__(self, interface: str = constants.NETWORKING.ETH0,
                 limit_packets_queue: int = 30000, packet_delay_ms: float = 0.1,
                 packet_delay_jitter_ms: float = 0.025,
                 packet_delay_correlation_percentage: float = 25,
                 packet_delay_distribution: PacketDelayDistributionType = PacketDelayDistributionType.PARETO,
                 packet_loss_type: PacketLossType = PacketLossType.GEMODEL,
                 packet_loss_rate_random_percentage: float = 2,
                 packet_loss_random_correlation_percentage: float = 25,
                 loss_state_markov_chain_p13: float = 0.1, loss_state_markov_chain_p31: float = 0.1,
                 loss_state_markov_chain_p32: float = 0.1, loss_state_markov_chain_p23: float = 0.1,
                 loss_state_markov_chain_p14: float = 0.1, loss_gemodel_p: float = 0.0001,
                 loss_gemodel_r: float = 0.999,
                 loss_gemodel_h: float = 0.0001, loss_gemodel_k: float = 0.9999,
                 packet_corrupt_percentage: float = 0.00001, packet_corrupt_correlation_percentage: float = 25,
                 packet_duplicate_percentage: float = 0.00001, packet_duplicate_correlation_percentage: float = 25,
                 packet_reorder_percentage: float = 0.0025, packet_reorder_correlation_percentage: float = 25,
                 packet_reorder_gap: int = 5,
                 rate_limit_mbit: float = 100,
                 packet_overhead_bytes: int = 0, cell_overhead_bytes: int = 0):
        """
        Initializes the DTO

        :param interface: the name of the network interface
        :param limit_packets_queue: Maximum number of packets that the output queue (queueing discpline) stores
                                    Note that to be able to rate limit at relatively high speeds, this queue must be
                                    quite large (FIFO by default)
        :param packet_delay_ms: a delay that is added to outgoing packets (specified in ms)
        :param packet_delay_jitter_ms: the jitter of the dealy added to outgoing packets (specified in ms)
        :param packet_delay_correlation_percentage: the amount of correlation in delay of outgoing packets
                                                   (specified in %)
                                                   for example delay 100ms jitter=10ms correlation=25% causes delay
                                                   to be 100ms +- 10ms with successive packets depending 25%
                                                   on each other
        :param packet_delay_distribution: the delay distribution, defaults to Gaussian, but can also be uniform,
                                                normal, pareto, or paretonormal
        :param packet_loss_type: the type of packet loss (random, state, or gemodel)
        :param packet_loss_rate_random_percentage: The packet loss percent when using the random packet loss type
        :param packet_loss_random_correlation_percentage: The packet loss correlation when using the random
                                                          packet loss type
        :param loss_state_markov_chain_p13: The 1->3 transition probability when using the 2-state Markov
                                            chain state loss type
        :param loss_state_markov_chain_p31: The 3->1 transition probability when using the 2,3,or 4-state
                                            Markov chain state loss type
        :param loss_state_markov_chain_p32: The 3->2 transition probability when using the 3,or 4-state Markov chain
                                            state loss type
        :param loss_state_markov_chain_p23: The 2->3 transition probability when using the 3,or 4-state Markov chain
                                            state loss type
        :param loss_state_markov_chain_p14: The 1->4 transition probability when using the 4-state Markov chain state
                                            loss type
        :param loss_gemodel_p: The p parameter when using the Bernoulli,Simple Gilbert or Gilbert model
                               in the gemodel loss type
        :param loss_gemodel_r: The p parameter when using the Simple Gilbert or Gilbert-Elliot model in the
                               gemodel loss type
        :param loss_gemodel_h: The h parameter when using the Simple Gilbert or Gilbert-Elliot model
                               in the gemodel loss type
        :param loss_gemodel_k: The k parameter when using the Gilbert-Elliot model in the gemodel loss type
        :param packet_corrupt_percentage: The percentage of corrupt outgoing packets
        :param packet_corrupt_correlation_percentage: The correlation of corrupt outgoing packets
        :param packet_duplicate_percentage: The percentage of duplicated outgoing packets
        :param packet_duplicate_correlation_percentage: The correlation of duplicated outgoing packets
        :param packet_reorder_percentage: The percentage of reordered packets
        :param packet_reorder_correlation_percentage: The correlation of reordered packets
        :param packet_reorder_gap: The packet reordering gap
        :param rate_limit_mbit: The bandwidth limit
        :param packet_overhead_bytes: The emulated packet overhead
        :param cell_overhead_bytes: The emulated cell overhead
        """
        self.interface = interface
        self.limit_packets_queue = limit_packets_queue
        self.packet_delay_ms = packet_delay_ms
        self.packet_delay_jitter_ms = packet_delay_jitter_ms
        self.packet_delay_correlation_percentage = packet_delay_correlation_percentage
        self.packet_delay_distribution = packet_delay_distribution
        self.packet_loss_type = packet_loss_type
        self.packet_loss_rate_random_percentage = packet_loss_rate_random_percentage
        self.packet_loss_random_correlation_percentage = packet_loss_random_correlation_percentage
        self.loss_state_markov_chain_p13 = loss_state_markov_chain_p13
        self.loss_state_markov_chain_p31 = loss_state_markov_chain_p31
        self.loss_state_markov_chain_p32 = loss_state_markov_chain_p32
        self.loss_state_markov_chain_p23 = loss_state_markov_chain_p23
        self.loss_state_markov_chain_p14 = loss_state_markov_chain_p14
        self.loss_gemodel_p = loss_gemodel_p
        self.loss_gemodel_r = loss_gemodel_r
        self.loss_gemodel_h = loss_gemodel_h
        self.loss_gemodel_k = loss_gemodel_k
        self.packet_corrupt_percentage = packet_corrupt_percentage
        self.packet_corrupt_correlation_percentage = packet_corrupt_correlation_percentage
        self.packet_duplicate_percentage = packet_duplicate_percentage
        self.packet_duplicate_correlation_percentage = packet_duplicate_correlation_percentage
        self.packet_reorder_percentage = packet_reorder_percentage
        self.packet_reorder_correlation_percentage = packet_reorder_correlation_percentage
        self.packet_reorder_gap = packet_reorder_gap
        self.rate_limit_mbit = rate_limit_mbit
        self.packet_overhead_bytes = packet_overhead_bytes
        self.cell_overhead_bytes = cell_overhead_bytes

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeNetworkConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the converted instance
        """
        obj = NodeNetworkConfig(
            interface=d["interface"],
            limit_packets_queue=d["limit_packets_queue"],
            packet_delay_ms=d["packet_delay_ms"],
            packet_delay_jitter_ms=d["packet_delay_jitter_ms"],
            packet_delay_correlation_percentage=d["packet_delay_correlation_percentage"],
            packet_delay_distribution=d["packet_delay_distribution"],
            packet_loss_type=d["packet_loss_type"],
            packet_loss_rate_random_percentage=d["packet_loss_rate_random_percentage"],
            packet_loss_random_correlation_percentage=d["packet_loss_random_correlation_percentage"],
            loss_state_markov_chain_p13=d["loss_state_markov_chain_p13"],
            loss_state_markov_chain_p31=d["loss_state_markov_chain_p31"],
            loss_state_markov_chain_p32=d["loss_state_markov_chain_p32"],
            loss_state_markov_chain_p23=d["loss_state_markov_chain_p23"],
            loss_state_markov_chain_p14=d["loss_state_markov_chain_p14"],
            loss_gemodel_p=d["loss_gemodel_p"],
            loss_gemodel_r=d["loss_gemodel_r"],
            loss_gemodel_h=d["loss_gemodel_h"],
            loss_gemodel_k=d["loss_gemodel_k"],
            packet_corrupt_percentage=d["packet_corrupt_percentage"],
            packet_corrupt_correlation_percentage=d["packet_corrupt_correlation_percentage"],
            packet_duplicate_percentage=d["packet_duplicate_percentage"],
            packet_duplicate_correlation_percentage=d["packet_duplicate_correlation_percentage"],
            packet_reorder_percentage=d["packet_reorder_percentage"],
            packet_reorder_correlation_percentage=d["packet_reorder_correlation_percentage"],
            packet_reorder_gap=d["packet_reorder_gap"],
            rate_limit_mbit=d["rate_limit_mbit"],
            packet_overhead_bytes=d["packet_overhead_bytes"],
            cell_overhead_bytes=d["cell_overhead_bytes"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["interface"] = self.interface
        d["limit_packets_queue"] = self.limit_packets_queue
        d["packet_delay_ms"] = self.packet_delay_ms
        d["packet_delay_jitter_ms"] = self.packet_delay_jitter_ms
        d["packet_delay_correlation_percentage"] = self.packet_delay_correlation_percentage
        d["packet_delay_distribution"] = self.packet_delay_distribution
        d["packet_loss_type"] = self.packet_loss_type
        d["packet_loss_rate_random_percentage"] = self.packet_loss_rate_random_percentage
        d["packet_loss_random_correlation_percentage"] = self.packet_loss_random_correlation_percentage
        d["loss_state_markov_chain_p13"] = self.loss_state_markov_chain_p13
        d["loss_state_markov_chain_p31"] = self.loss_state_markov_chain_p31
        d["loss_state_markov_chain_p32"] = self.loss_state_markov_chain_p32
        d["loss_state_markov_chain_p23"] = self.loss_state_markov_chain_p23
        d["loss_state_markov_chain_p14"] = self.loss_state_markov_chain_p14
        d["loss_gemodel_p"] = self.loss_gemodel_p
        d["loss_gemodel_r"] = self.loss_gemodel_r
        d["loss_gemodel_h"] = self.loss_gemodel_h
        d["loss_gemodel_k"] = self.loss_gemodel_k
        d["packet_corrupt_percentage"] = self.packet_corrupt_percentage
        d["packet_corrupt_correlation_percentage"] = self.packet_corrupt_correlation_percentage
        d["packet_duplicate_percentage"] = self.packet_duplicate_percentage
        d["packet_duplicate_correlation_percentage"] = self.packet_duplicate_correlation_percentage
        d["packet_reorder_percentage"] = self.packet_reorder_percentage
        d["packet_reorder_correlation_percentage"] = self.packet_reorder_correlation_percentage
        d["packet_reorder_gap"] = self.packet_reorder_gap
        d["rate_limit_mbit"] = self.rate_limit_mbit
        d["packet_overhead_bytes"] = self.packet_overhead_bytes
        d["cell_overhead_bytes"] = self.cell_overhead_bytes
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"limits_packets_queue:{self.limit_packets_queue}, packet_delay_ms:{self.packet_delay_ms}, " \
               f"packet_delay_jitter_ms:{self.packet_delay_jitter_ms}, " \
               f"packet_delay_correlation_percentage: {self.packet_delay_correlation_percentage}, " \
               f"packet_delay_distribution: {self.packet_delay_distribution}, " \
               f"packet_loss_type:{self.packet_loss_type}, " \
               f"packet_loss_rate_random_percentage: {self.packet_loss_rate_random_percentage}, " \
               f"packet_loss_correlation_percentage: {self.packet_loss_random_correlation_percentage}, " \
               f"loss_state_markov_chain_p13: {self.loss_state_markov_chain_p13}, " \
               f"loss_state_markov_chain_p31: {self.loss_state_markov_chain_p31}, " \
               f"loss_state_markov_chain_p32: {self.loss_state_markov_chain_p32}, " \
               f"loss_state_markov_chain_p23: {self.loss_state_markov_chain_p23}, " \
               f"loss_state_markov_chain_p14: {self.loss_state_markov_chain_p14}, " \
               f"loss_gemodel_p:{self.loss_gemodel_p}, loss_gemodel_r: {self.loss_gemodel_r}, " \
               f"loss_gemodel_h:{self.loss_gemodel_h}, loss_gemodel_k:{self.loss_gemodel_k}, " \
               f"packet_corrupt_percentage:{self.packet_corrupt_percentage}, " \
               f"packet_corrupt_correlation_percentage:{self.packet_corrupt_correlation_percentage}, " \
               f"packet_duplicate_percentage:{self.packet_duplicate_percentage}, " \
               f"packet_duplicate_correlation_percentage:{self.packet_duplicate_correlation_percentage}, " \
               f"packet_reorder_percentage:{self.packet_reorder_percentage}, " \
               f"packet_reorder_correlation_percentage:{self.packet_reorder_correlation_percentage}, " \
               f"packet_reorder_gap: {self.packet_reorder_gap}" \
               f"rate_limit_mbit:{self.rate_limit_mbit}, packet_overhead_bytes:{self.packet_overhead_bytes}," \
               f"cell_overhead_bytes:{self.cell_overhead_bytes}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "NodeNetworkConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NodeNetworkConfig.from_dict(json.loads(json_str))

    def copy(self) -> "NodeNetworkConfig":
        """
        :return: a copy of the DTO
        """
        return NodeNetworkConfig.from_dict(self.to_dict())

    @staticmethod
    def schema() -> "NodeNetworkConfig":
        """
        :return: get the schema of the DTO
        """
        return NodeNetworkConfig()
