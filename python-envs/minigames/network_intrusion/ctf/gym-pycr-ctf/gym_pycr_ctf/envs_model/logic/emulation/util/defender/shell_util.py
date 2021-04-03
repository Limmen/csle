from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
import gym_pycr_ctf.constants.constants as constants

class ShellUtil:
    """
    Class containing utility functions for the shell-related of the defender in the emulation
    """

    @staticmethod
    def read_open_connections(emulation_config: EmulationConfig) -> int:
        """
        Measures the number of open connections to the server

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of open connections
        """
        outdata, errdata, total_time = \
            EmulationUtil.execute_ssh_cmd(cmd=constants.DEFENDER.LIST_OPEN_CONNECTIONS_CMD, conn=emulation_config.agent_conn)
        connections_str = outdata.decode()
        parts = connections_str.split("Active UNIX domain sockets", 1)
        if len(parts) > 0:
            parts2 = parts[0].split("State")
            if len(parts2) > 1:
                parts3 = parts2[1].split("\n")
                return len(parts3)-1
        return -1

    @staticmethod
    def read_users(emulation_config: EmulationConfig) -> int:
        """
        Measures the number of user accounts on the server

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of user accounts
        """
        outdata, errdata, total_time = \
            EmulationUtil.execute_ssh_cmd(cmd=constants.DEFENDER.LIST_USER_ACCOUNTS,
                                          conn=emulation_config.agent_conn)
        users_str = outdata.decode()
        users = users_str.split("\n")
        return len(users)

    @staticmethod
    def read_logged_in_users(emulation_config: EmulationConfig) -> int:
        """
        Measures the number of logged-in users on the server

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of logged in users
        """
        outdata, errdata, total_time = \
            EmulationUtil.execute_ssh_cmd(cmd=constants.DEFENDER.LIST_LOGGED_IN_USERS_CMD,
                                          conn=emulation_config.agent_conn)
        users_str = outdata.decode()
        users_str = users_str.replace("\n", "")
        users = users_str.split(" ")
        return len(users)

    @staticmethod
    def read_processes(emulation_config: EmulationConfig) -> int:
        """
        Measures the number of processes on the server

        :param emulation_config: configuration to connect to the node in the emulation
        :return: the number of processes
        """
        try:
            outdata, errdata, total_time = \
                EmulationUtil.execute_ssh_cmd(cmd=constants.DEFENDER.LIST_NUMBER_OF_PROCESSES,
                                              conn=emulation_config.agent_conn)
            processes_str = outdata.decode()
            num_processes = int(processes_str)
        except:
            num_processes = -1
        return num_processes