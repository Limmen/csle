import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig


class GeneratorUtil:
    """
    A Utility Class for generating emulation configurations and interacting with running emulations
    """

    @staticmethod
    def connect_admin(emulation_env_config: EmulationEnvConfig, ip: str) -> None:
        """
        Connects the admin agent

        :param emulation_env_config: the configuration of the emulation to connect to
        :param ip: the ip of the container to connect to
        :return: None
        """
        emulation_env_config.agent_ip = ip
        emulation_env_config.connect(ip=ip, username=constants.CSLE_ADMIN.USER, pw=constants.CSLE_ADMIN.PW)

    @staticmethod
    def disconnect_admin(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Disconnects the admin agent

        :param emulation_env_config: the configuration of the emulation to disconnect the admin of
        :return: None
        """
        emulation_env_config.close()