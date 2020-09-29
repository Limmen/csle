import time
from xml.etree.ElementTree import XML, fromstring
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action

class ClusterUtil:
    """
    Class containing utility functions for the cluster-middleware
    """


    @staticmethod
    def execute_cmd(a : Action, env_config : EnvConfig):
        env_config.cluster_config.agent_channel.send(a.cmd[0] + "\n")

    @staticmethod
    def read_result(env_config : EnvConfig) -> str:
        while not env_config.cluster_config.agent_channel.recv_ready():
            time.sleep(env_config.shell_read_wait)
        output = env_config.cluster_config.agent_channel.recv(5000)
        output_str = output.decode("utf-8")
        output_str = env_config.shell_escape.sub("", output_str)
        return output_str


    @staticmethod
    def check_nmap_action_cache(a : Action, env_config : EnvConfig):

        # Clear channel
        if env_config.cluster_config.agent_channel.recv_ready():
            output = env_config.cluster_config.agent_channel.recv(5000)

        # List cache
        env_config.cluster_config.agent_channel.send("ls -1 " + env_config.nmap_cache_dir + "\n")
        result_str = ClusterUtil.read_result(env_config=env_config)
        cache_list = result_str.split('\r\n')
        cache_list = cache_list[1:-1]  # remove command ([0]) and prompt ([-1])

        # Search through cache
        query = str(a.id.value) + ".xml"
        for item in cache_list:
            if item == query:
                return item

        return None

    @staticmethod
    def parse_nmap_xml(file_name : str, env_config : EnvConfig):
        env_config.cluster_config.agent_channel.send("cat " + env_config.nmap_cache_dir + file_name + "\n")
        while not env_config.cluster_config.agent_channel.recv_ready():
            time.sleep(env_config.shell_read_wait)
        output = env_config.cluster_config.agent_channel.recv(env_config.max_nmap_command_output_size)
        output_str = output.decode("utf-8")
        output_str = env_config.shell_escape.sub("", output_str)
        lines = output_str.split('\r\n')
        lines = lines[1:-1]  # remove command ([0]) and prompt ([-1])
        xml_str = "\n".join(lines)
        xml_data = fromstring(xml_str)
        return xml_data
