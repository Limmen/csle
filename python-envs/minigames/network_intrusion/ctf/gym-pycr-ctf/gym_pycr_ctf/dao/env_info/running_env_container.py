
class RunningEnvContainer:

    def __init__(self, name: str, status: str, short_id : str, image_short_id : str, image_tags: list, id: str,
                 created: str, ip: str, network_id: str, gateway: str, mac: str, ip_prefix_len: int,
                 minigame : str, name2: str, level: str, hostname: str, image_name : str, net: str,
                 dir: str, containers_config_path : str, users_config_path : str, flags_config_path : str,
                 vulnerabilities_config_path : str, topology_config_path: str):
        self.name = name
        self.status = status
        self.short_id = short_id
        self.image_short_id = image_short_id
        self.image_tags = image_tags
        self.id = id
        self.created = created
        self.ip = ip
        self.network_id = network_id
        self.gateway=gateway
        self.mac = mac
        self.ip_prefix_len = ip_prefix_len
        self.minigame = minigame
        self.name2 = name2
        self.level = level
        self.hostname = hostname
        self.image_name =image_name
        self.net = net
        self.dir=dir
        self.containers_config_path = containers_config_path
        self.users_config_path = users_config_path
        self.flags_config_path = flags_config_path
        self.vulnerabilities_config_path = vulnerabilities_config_path
        self.topology_config_path = topology_config_path

    def to_dict(self):
        d = {}
        d["name"] = self.name
        d["status"] = self.status
        d["short_id"] = self.short_id
        d["image_short_id"] = self.image_short_id
        d["image_tags"] = self.image_tags
        d["id"] = self.id
        d["created"] = self.created
        d["ip"] = self.ip
        d["network_id"] = self.network_id
        d["gateway"] = self.gateway
        d["mac"] = self.mac
        d["ip_prefix_len"] = self.ip_prefix_len
        d["minigame"] = self.minigame
        d["name2"] = self.name2
        d["level"] = self.level
        d["hostname"] = self.hostname
        d["image_name"] = self.image_name
        d["net"] = self.net
        d["containers_config_path"] = self.containers_config_path
        d["users_config_path"] = self.users_config_path
        d["flags_config_path"] = self.flags_config_path
        d["vulnerabilities_config_path"] = self.vulnerabilities_config_path
        d["topology_config_path"] = self.topology_config_path
        return d