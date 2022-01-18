from typing import Set


class NodeFirewallConfig:
    """
    A DTO object representing a firewall configuration of a container in an emulation environment
    """

    def __init__(self, ip: str, hostname: str, default_internal_gw: str, default_external_gw: str,
                 output_accept: Set[str], input_accept: Set[str],
                 forward_accept: Set[str], output_drop: Set[str], input_drop: Set[str],
                 forward_drop: Set[str], default_internal_output :str, default_internal_input: str,
                 default_internal_forward: str, default_external_output :str, default_external_input: str,
                 default_external_forward: str,
                 routes: Set[str], internal_subnetwork_mask: str, external_subnetwork_mask: str
                 ):
        """
        Intializes the DTO

        :param ip: the ip of the node
        :param hostname: the hostname of the node
        :param default_internal_gw: the default internal gw
        :param default_external_gw: the default external gw
        :param output_accept: the list of ips to accept output
        :param input_accept: the list of ips to accept input
        :param forward_accept: the list of ips to accept forward
        :param output_drop: the list of ips to drop output
        :param input_drop: the list of ips to drop input
        :param forward_drop: the list of ips to drop forward
        :param default_internal_output: the default output policy for the internal network
        :param default_internal_input: the default input policy for the internal network
        :param default_internal_forward: the default forward policy for the internal network
        :param default_external_output: the default output policy for the external network
        :param default_external_input: the default input policy for the external network
        :param default_external_forward: the default forward policy for the external network
        :param routes: the set of custom routes for the routing table
        :param internal_subnetwork_mask: the internal subnetwork mask
        :param external_subnetwork_mask: the external subnetwork mask
        """
        self.ip = ip
        self.hostname = hostname
        self.default_internal_gw = default_internal_gw
        self.default_external_gw = default_external_gw
        self.output_accept = output_accept
        self.input_accept = input_accept
        self.forward_accept = forward_accept
        self.output_drop = output_drop
        self.input_drop = input_drop
        self.forward_drop = forward_drop
        self.default_internal_output = default_internal_output
        self.default_internal_input = default_internal_input
        self.default_internal_forward = default_internal_forward
        self.default_external_output = default_external_output
        self.default_external_input = default_external_input
        self.default_external_forward = default_external_forward
        self.routes = routes
        self.internal_subnetwork_mask = internal_subnetwork_mask
        self.external_subnetwork_mask = external_subnetwork_mask

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, internal_default_gw:{self.default_internal_gw}, " \
               f"external_default_gw:{self.default_external_gw}, " \
               f"output_accept:{self.output_accept}, " \
               f"input_accept:{self.input_accept}, forward_accept:{self.forward_accept}, " \
               f"output_drop:{self.output_drop}, " \
               f"input_drop:{self.input_drop}, forward_drop:{self.forward_drop}, " \
               f"default_internal_output:{self.default_internal_output}, " \
               f"default_internal_input:{self.default_internal_input}, " \
               f"default_internal_forward:{self.default_internal_forward}, " \
               f"default_external_output:{self.default_external_output}, " \
               f"default_external_input:{self.default_external_input}, " \
               f"default_external_forward:{self.default_external_forward}, " \
               f"routers:{self.routes}, hostname: {self.hostname}, " \
               f"internal_subnetwork_mask:{self.internal_subnetwork_mask}, " \
               f"external_subnetwork_mask:{self.external_subnetwork_mask}"
