
class DockerContainerMetadata:
    """
    DTO Object representing a running or stopped Docker container
    """

    def __init__(self, name: str, status: str, short_id : str, image_short_id : str, image_tags: list, id: str,
                 created: str, ip: str, network_id: str, gateway: str, mac: str, ip_prefix_len: int,
                 name2: str, level: str, hostname: str, image_name : str, net: str,
                 dir: str, config_path : str, container_handle, emulation: str, log_sink: str):
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
        :param name2: the name2 of the container
        :param level: the level of the container
        :param hostname: the hostname of the container
        :param image_name: the image name of the container
        :param net: the network of the container
        :param dir: the directory of the container
        :param config_path: the container configuration ṕath of the container
        :param container_handle: the py-docker container handle
        :param emulation: the emulation name
        :param log_sink: the log_sink name
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
        self.name2 = name2
        self.level = level
        self.hostname = hostname
        self.image_name =image_name
        self.net = net
        self.dir=dir
        self.config_path = config_path
        self.container_handle = container_handle
        self.emulation = emulation
        self.log_sink = log_sink

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
        d["name2"] = self.name2
        d["level"] = self.level
        d["hostname"] = self.hostname
        d["image_name"] = self.image_name
        d["net"] = self.net
        d["config_path"] = self.config_path
        d["emulation"] = self.emulation
        d["log_sink"] = self.log_sink
        return d


    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"name: {self.name}, status: {self.status}, short_id: {self.short_id}, " \
               f"image_short_id: {self.image_short_id}, image_tags: {self.image_tags}, id: {self.id}, " \
               f"created: {self.created}, ip: {self.ip}, network_id: {self.network_id}, gateway: {self.gateway}," \
               f"mac: {self.mac}, ip_prefix_len: {self.ip_prefix_len}, name2: {self.name2}," \
               f"level: {self.level}, hostname: {self.hostname}, image_name: {self.image_name}, net: {self.net}, " \
               f"dir: {self.dir}, config_path: {self.config_path}, emulation: {self.emulation}, log_sink:{self.log_sink}"