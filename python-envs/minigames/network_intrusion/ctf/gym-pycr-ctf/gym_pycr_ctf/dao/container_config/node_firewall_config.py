from typing import Set


class NodeFirewallConfig:
    """
    A DTO object representing a firewall configuration of a container in an emulation environment
    """

    def __init__(self, ip: str, default_gw: str, output_accept: Set[str], input_accept: Set[str],
                 forward_accept: Set[str], output_drop: Set[str], input_drop: Set[str],
                 forward_drop: Set[str], default_output, default_input, default_forward,
                 routes: Set[str]
                 ):
        self.ip = ip
        self.default_gw = default_gw
        self.output_accept = output_accept
        self.input_accept = input_accept
        self.forward_accept = forward_accept
        self.output_drop = output_drop
        self.input_drop = input_drop
        self.forward_drop = forward_drop
        self.default_output = default_output
        self.default_input = default_input
        self.default_forward = default_forward
        self.routes = routes

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, default_gw:{}, output_accept:{}, input_accept:{}, forward_accept:{}, output_drop:{}, " \
               "input_drop:{}, forward_drop:{}, default_output:{}, default_input:{}, default_forward:{}, " \
               "routers:{}".format(self.ip, self.default_gw, self.output_accept, self.input_accept,
                                   self.forward_accept, self.output_drop, self.input_drop, self.default_output,
                                   self.default_input, self.default_forward, self.routes)
