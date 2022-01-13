"""
Network configuration of a container in the emulation
"""
from csle_common.dao.container_config.packet_loss_type import PacketLossType
from csle_common.dao.container_config.packet_delay_distribution_type import PacketDelayDistributionType


class NodeNetworkConfig:
    """
    A DTO object representing the network configuration of a specific container in an emulation environment
    """

    def __init__(self, limit_packets_queue: int, transmission_delay_ms: float,
                 transmission_delay_jitter_ms: float,
                 transmission_delay_correlation_percentage: float,
                 transmission_delay_distribution: PacketDelayDistributionType, packet_loss_type : PacketLossType,
                 packet_loss_rate_random_percentage: float,
                 packet_loss_random_correlation_percentage: float,
                 loss_state_markov_chain_p13: float, loss_state_markov_chain_p31: float,
                 loss_state_markov_chain_p32: float, loss_state_markov_chain_p23: float,
                 loss_state_markov_chain_p14: float, loss_gemodel_p: float, loss_gemodel_r: float,
                 loss_gemodel_h: float, loss_gemodel_k: float,
                 packet_corrupt_percentage: float, packet_corrupt_correlation_percentage: float,
                 packet_duplicate_percentage: float, packet_duplicate_correlation_percentage: float,
                 packet_reorder_percentage: float, packet_reorder_correlation_percentage: float,
                 ingress_rate_limit_mbit: float,
                 ingress_packet_overhead_bytes: int, ingress_cell_overhead_bytes: int):
        """
        Initializes the DTO

        :param limit_packets_queue: Maximum number of packets that the output queue (queueing discpline) stores
                                    Note that to be able to rate limit at relatively high speeds, this queue must be
                                    quite large (FIFO by default)
        :param transmission_delay_ms: a delay that is added to outgoing packets (specified in ms)
        :param transmission_delay_jitter_ms: the jitter of the dealy added to outgoing packets (specified in ms)
        :param transmission_delay_correlation_percentage: the amount of correlation in delay of outgoing packets (specified in %)
                                               for example delay 100ms jitter=10ms correlation=25% causes delay to be
                                               100ms +- 10ms with successive packets depending 25% on each other
        :param transmission_delay_distribution: the delay distribution, defaults to Gaussian, but can also be uniform,
                                                normal, pareto, or paretonormal
        :param packet_loss_type: the type of packet loss (random, state, or gemodel)
        :param packet_loss_rate_random_percentage: The packet loss percent when using the random packet loss type
        :param packet_loss_random_correlation_percentage: The packet loss correlation when using the random packet loss type
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
        :param ingress_rate_limit_mbit: The bandwidth limit on ingress traffic
        :param ingress_packet_overhead_bytes: The emulated packet overhead of ingress traffic
        :param ingress_cell_overhead_bytes: The emulated cell overhead of ingress traffic
        """
        self.limit_packets_queue = limit_packets_queue
        self.transmission_delay = transmission_delay_ms
        self.transmission_delay_jitter = transmission_delay_jitter_ms
        self.transmission_delay_correlation = transmission_delay_correlation_percentage
        self.transmission_delay_distribution = transmission_delay_distribution
        self.packet_loss_type = packet_loss_type
        self.packet_loss_rate = packet_loss_rate_random_percentage
        self.packet_loss_correlation = packet_loss_random_correlation_percentage
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
        self.packet_corrupt_correlation = packet_corrupt_correlation_percentage
        self.packet_duplicate_percentage = packet_duplicate_percentage
        self.packet_duplicate_correlation = packet_duplicate_correlation_percentage
        self.packet_reorder_percentage = packet_reorder_percentage
        self.packet_reorder_correlation = packet_reorder_correlation_percentage
        self.ingress_rate_limit = ingress_rate_limit_mbit
        self.ingress_packet_overhead = ingress_packet_overhead_bytes
        self.ingress_cell_overhead = ingress_cell_overhead_bytes

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"limits_packets_queue:{self.limit_packets_queue}, transmission_delay:{self.transmission_delay}, " \
               f"transmission_delay_jitter:{self.transmission_delay_jitter}, " \
               f"transmission_delay_correlation: {self.transmission_delay_correlation}, " \
               f"transmission_delay_distribution: {self.transmission_delay_distribution}, " \
               f"packet_loss_type:{self.packet_loss_type}, packet_loss_rate: {self.packet_loss_rate}, " \
               f"packet_loss_correlation: {self.packet_loss_correlation}, " \
               f"loss_state_markov_chain_p13: {self.loss_state_markov_chain_p13}, " \
               f"loss_state_markov_chain_p31: {self.loss_state_markov_chain_p31}, " \
               f"loss_state_markov_chain_p32: {self.loss_state_markov_chain_p32}, " \
               f"loss_state_markov_chain_p23: {self.loss_state_markov_chain_p23}, " \
               f"loss_state_markov_chain_p14: {self.loss_state_markov_chain_p14}, " \
               f"loss_gemodel_p:{self.loss_gemodel_p}, loss_gemodel_r: {self.loss_gemodel_r}, " \
               f"loss_gemodel_h:{self.loss_gemodel_h}, loss_gemodel_k:{self.loss_gemodel_k}, " \
               f"packet_corrupt_percentage:{self.packet_corrupt_percentage}, " \
               f"packet_corrupt_correlation:{self.packet_corrupt_correlation}, " \
               f"packet_duplicate_percentage:{self.packet_duplicate_percentage}, " \
               f"packet_duplicate_correlation:{self.packet_duplicate_correlation}, " \
               f"packet_reorder_percentage:{self.packet_reorder_percentage}, " \
               f"packet_reorder_correlation:{self.packet_reorder_correlation}, " \
               f"ingress_rate_limit:{self.ingress_rate_limit}, ingress_packet_overhead:{self.ingress_packet_overhead}," \
               f"ingress_cell_overhead:{self.ingress_cell_overhead}"
