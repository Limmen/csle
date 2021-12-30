
class EnvContainer:
    """
    DTO Object representing a running or stopped Docker container
    """

    def __init__(self, name: str, status: str, short_id : str, image_short_id : str, image_tags: list, id: str,
                 created: str, ip: str, network_id: str, gateway: str, mac: str, ip_prefix_len: int,
                 minigame : str, name2: str, level: str, hostname: str, image_name : str, net: str,
                 dir: str, containers_config_path : str, users_config_path : str, flags_config_path : str,
                 vulnerabilities_config_path : str, topology_config_path: str,
                 traffic_config_path: str, container_handle):
        """
        Intializes the DTO

        :param name: the name of the container
        :param status: the status of the container
        :param short_id: the short id of the container
        :param image_short_id: the short id of the container's image
        :param image_tags: the tags of the container's image
        :param id: the id of the container
        :param created: the time the container was created
        :param ip: the ip of the container
        :param network_id: the network id of the container
        :param gateway: the gateway of the container
        :param mac: the mac address of the container
        :param ip_prefix_len: the ip prefix len of the container
        :param minigame: the minigame of the container
        :param name2: the name2 of the container
        :param level: the level of the container
        :param hostname: the hostname of the container
        :param image_name: the image name of the container
        :param net: the network of the container
        :param dir: the directory of the container
        :param containers_config_path: the container configuration ṕath of the container
        :param users_config_path: the users configuration path of the container
        :param flags_config_path: the flags configuration path of the container
        :param vulnerabilities_config_path: the vulnerabilities configuration path of the container
        :param topology_config_path: the topology configuration path of the container
        :param traffic_config_path: the traffic configuration path of the container
        :param container_handle: the py-docker container handle
        """
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
        self.traffic_config_path = traffic_config_path
        self.container_handle = container_handle

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
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
        d["traffic_config_path"] = self.traffic_config_path
        return d


    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"name: {self.name}, status: {self.status}, short_id: {self.short_id}, " \
               f"image_short_id: {self.image_short_id}, image_tags: {self.image_tags}, id: {self.id}, " \
               f"created: {self.created}, ip: {self.ip}, network_id: {self.network_id}, gateway: {self.gateway}," \
               f"mac: {self.mac}, ip_prefix_len: {self.ip_prefix_len}, minigame: {self.minigame}, name2: {self.name2}," \
               f"level: {self.level}, hostname: {self.hostname}, image_name: {self.image_name}, net: {self.net}, " \
               f"dir: {self.dir}, containers_config_path: {self.containers_config_path}, " \
               f"users_config_path: {self.users_config_path}, flags_config_path: {self.flags_config_path}, " \
               f"vulnerabilities_config_path: {self.vulnerabilities_config_path}, " \
               f"topology_config:path: {self.topology_config_path}, traffic_config_path: {self.traffic_config_path}"