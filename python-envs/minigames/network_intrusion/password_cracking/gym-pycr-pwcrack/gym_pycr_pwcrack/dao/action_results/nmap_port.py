from gym_pycr_pwcrack.dao.action_results.nmap_port_status import NmapPortStatus

class NmapPort:

    def __init__(self, port_id: int, protocol : str, status: NmapPortStatus = NmapPortStatus.DOWN,
                 service_name : str = "none"):
        self.port_id = port_id
        self.protocol = protocol
        self.status = status
        self.service_name = service_name