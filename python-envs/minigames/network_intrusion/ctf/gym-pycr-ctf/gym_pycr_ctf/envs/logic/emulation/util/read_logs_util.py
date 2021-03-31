from typing import Tuple, List
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.envs.logic.emulation.util.read_logs_util import ReadLogsUtil

class ReadLogsUtil:
    """
    Class containing utility functions for the shell-related functionality to the emulation
    """

    @staticmethod
    def read_logs_util(file_name: str, env_config: EnvConfig) -> List[str]:
        """
        TODO

        :param file_name: name of the file to parse
        :param env_config: environment config
        :return: a list of files
        """
        pass