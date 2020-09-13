import numpy as np
class EnvState:

    def __init__(self, num_servers :int, num_ports:int, num_vuln:int):
        self.num_servers = num_servers
        self.num_ports = num_ports
        self.num_vuln = num_vuln


    def initialize_state(self) -> np.ndarray:
        self.state = np.zeros((num_servers, 2 + num_ports + num_vuln))
        self.port_lookup = np.zeros(num_servers*num_ports, 2)
        self.vuln_lookup = np.zeros(num_servers * num_vuln, 2)
