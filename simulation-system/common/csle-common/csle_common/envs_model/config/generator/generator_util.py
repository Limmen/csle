import os
from scp import SCPClient
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
import csle_common.constants.constants as constants


class GeneratorUtil:
    """
    A Utility Class for generating emulation configurations and interacting with running emulations
    """

    @staticmethod
    def connect_admin(emulation_config: EmulationConfig, ip: str) -> None:
        """
        Connects the admin agent

        :param emulation_config: the configuration of the emulation to connect to
        :param ip: the ip of the container to connect to
        :return: None
        """
        emulation_config.agent_ip = ip
        emulation_config.connect_agent()

    @staticmethod
    def disconnect_admin(emulation_config: EmulationConfig) -> None:
        """
        Disconnects the admin agent

        :param emulation_config: the configuration of the emulation to disconnect the admin of
        :return: None
        """
        emulation_config.close()

    @staticmethod
    def clean_filesystem_cache(containers_config: ContainersConfig) -> None:
        """
        Cleans the file system cache of a running emulation

        :param containers_config: the configuration of the containers in the emulation
        :return: None
        """
        for c in containers_config.containers:
            emulation_config = EmulationConfig(agent_ip=c.ip, agent_username=constants.CSLE_ADMIN.USER,
                                               agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=c.ip)
            outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd=constants.COMMANDS.LS_HOME, conn=emulation_config.agent_conn)
            home_dirs = outdata.decode("utf-8").split("\n")
            home_dirs = list(filter(lambda x: x != "", home_dirs))
            for hd in home_dirs:
                EmulationUtil.execute_ssh_cmd(cmd=constants.COMMANDS.RM_F_HOME + hd + constants.COMMANDS.SLASH_DELIM
                                                  + constants.COMMANDS.STAR_DELIM + constants.COMMANDS.XML_FILE_SUFFIX,
                                              conn=emulation_config.agent_conn)
                EmulationUtil.execute_ssh_cmd(cmd=constants.COMMANDS.RM_F_HOME + hd + constants.COMMANDS.SLASH_DELIM +
                                                  constants.COMMANDS.STAR_DELIM
                                                  + constants.FILE_PATTERNS.TXT_FILE_SUFFIX,
                                              conn=emulation_config.agent_conn)

    @staticmethod
    def zip_and_download_filesystem_cache(containers_config: ContainersConfig) -> None:
        """
        Zips the files to cache and downloads them from the emulation

        :param containers_config: the configuration of the containers in the emulation to cache
        :return: None
        """
        for c in containers_config.containers:
            print("Downloading cache from container:{}".format(c.name))
            emulation_config = EmulationConfig(agent_ip=c.ip, agent_username=constants.CSLE_ADMIN.USER,
                                               agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=c.ip)
            filename = c.name + "_cache.zip"
            o,e, _ = EmulationUtil.execute_ssh_cmd(cmd="zip -r " + filename + " /home/ '*.xml' '*.txt'", conn=emulation_config.agent_conn)
            filepath = "/home/csle_admin/"+ filename
            scp_client = SCPClient(emulation_config.agent_conn.get_transport())
            scp_client.get(filepath)

    @staticmethod
    def upload_and_unzip_filesystem_cache(containers_config: ContainersConfig) -> None:
        """
        Uploads and unzips a cache of the filesystem to containers in a running emulation

        :param containers_config: configuraiton of the containers in the emulation
        :return: None
        """
        for c in containers_config.containers:
            print("Uploading cache for container:{}".format(c.name))
            local_filename = c.name + "_cache.zip"
            if os.path.exists(local_filename):
                emulation_config = EmulationConfig(agent_ip=c.ip, agent_username=constants.CSLE_ADMIN.USER,
                                                   agent_pw=constants.CSLE_ADMIN.PW, server_connection=False)
                GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=c.ip)
                scp_client = SCPClient(emulation_config.agent_conn.get_transport())
                remote_filename = "/home/csle_admin/" + local_filename
                scp_client.put(local_filename, remote_filename)
                unzip_cmd = "cd /home/csle_admin/; unzip " + remote_filename
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=unzip_cmd, conn=emulation_config.agent_conn)
                cmd = "ls /home/csle_admin/home/"
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                users_w_home = o.decode().split("\n")
                users_w_home = list(filter(lambda x: x != '', users_w_home))
                for user in users_w_home:
                    cmd = "cp -f /home/csle_admin/home/" + user + "/* /home/" + user + "/"
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)