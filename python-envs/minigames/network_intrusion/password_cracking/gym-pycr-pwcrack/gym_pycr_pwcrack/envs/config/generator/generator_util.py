
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig


class GeneratorUtil:


    @staticmethod
    def connect_admin(cluster_config: ClusterConfig, ip: str):
        cluster_config.agent_ip = ip
        cluster_config.connect_agent()

    @staticmethod
    def disconnect_admin(cluster_config: ClusterConfig):
        cluster_config.close()