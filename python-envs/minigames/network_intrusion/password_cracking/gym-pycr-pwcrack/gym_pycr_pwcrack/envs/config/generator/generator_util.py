from scp import SCPClient, SCPException
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.container_config.containers_config import ContainersConfig
from gym_pycr_pwcrack.envs.logic.cluster.util.cluster_util import ClusterUtil


class GeneratorUtil:


    @staticmethod
    def connect_admin(cluster_config: ClusterConfig, ip: str):
        cluster_config.agent_ip = ip
        cluster_config.connect_agent()

    @staticmethod
    def disconnect_admin(cluster_config: ClusterConfig):
        cluster_config.close()

    @staticmethod
    def clean_filesystem_cache(containers_config: ContainersConfig):
        for c in containers_config.containers:
            cluster_config = ClusterConfig(agent_ip=c.ip, agent_username="pycr_admin",
                                           agent_pw="pycr@admin-pw_191", server_connection=False)
            GeneratorUtil.connect_admin(cluster_config=cluster_config, ip=c.ip)
            outdata, errdata, total_time = ClusterUtil.execute_ssh_cmd(cmd="ls /home/", conn=cluster_config.agent_conn)
            home_dirs = outdata.decode("utf-8").split("\n")
            home_dirs = list(filter(lambda x: x != "", home_dirs))
            for hd in home_dirs:
                ClusterUtil.execute_ssh_cmd(cmd="rm -f home/" + hd + "/*.xml", conn=cluster_config.agent_conn)
                ClusterUtil.execute_ssh_cmd(cmd="rm -f home/" + hd + "/*.txt", conn=cluster_config.agent_conn)

    @staticmethod
    def zip_and_download_filesystem_cache(containers_config: ContainersConfig):
        for c in containers_config.containers:
            cluster_config = ClusterConfig(agent_ip=c.ip, agent_username="pycr_admin",
                                           agent_pw="pycr@admin-pw_191", server_connection=False)
            GeneratorUtil.connect_admin(cluster_config=cluster_config, ip=c.ip)
            filename = c.name + "_cache.zip"
            ClusterUtil.execute_ssh_cmd(cmd="zip -r " + filename + " /home/ '*.xml' '*.txt'", conn=cluster_config.agent_conn)
            filepath = "/home/pycr_admin/"+ filename
            scp_client = SCPClient(cluster_config.agent_conn.get_transport())
            scp_client.get(filepath)