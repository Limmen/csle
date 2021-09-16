import os
from scp import SCPClient
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.dao.container_config.containers_config import ContainersConfig
from pycr_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil


class GeneratorUtil:


    @staticmethod
    def connect_admin(emulation_config: EmulationConfig, ip: str):
        emulation_config.agent_ip = ip
        emulation_config.connect_agent()

    @staticmethod
    def disconnect_admin(emulation_config: EmulationConfig):
        emulation_config.close()

    @staticmethod
    def clean_filesystem_cache(containers_config: ContainersConfig):
        for c in containers_config.containers:
            emulation_config = EmulationConfig(agent_ip=c.ip, agent_username="pycr_admin",
                                             agent_pw="pycr@admin-pw_191", server_connection=False)
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=c.ip)
            outdata, errdata, total_time = EmulationUtil.execute_ssh_cmd(cmd="ls /home/", conn=emulation_config.agent_conn)
            home_dirs = outdata.decode("utf-8").split("\n")
            home_dirs = list(filter(lambda x: x != "", home_dirs))
            for hd in home_dirs:
                EmulationUtil.execute_ssh_cmd(cmd="rm -f home/" + hd + "/*.xml", conn=emulation_config.agent_conn)
                EmulationUtil.execute_ssh_cmd(cmd="rm -f home/" + hd + "/*.txt", conn=emulation_config.agent_conn)

    @staticmethod
    def zip_and_download_filesystem_cache(containers_config: ContainersConfig):
        for c in containers_config.containers:
            print("Downloading cache from container:{}".format(c.name))
            emulation_config = EmulationConfig(agent_ip=c.ip, agent_username="pycr_admin",
                                             agent_pw="pycr@admin-pw_191", server_connection=False)
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=c.ip)
            filename = c.name + "_cache.zip"
            o,e, _ = EmulationUtil.execute_ssh_cmd(cmd="zip -r " + filename + " /home/ '*.xml' '*.txt'", conn=emulation_config.agent_conn)
            filepath = "/home/pycr_admin/"+ filename
            scp_client = SCPClient(emulation_config.agent_conn.get_transport())
            scp_client.get(filepath)

    @staticmethod
    def upload_and_unzip_filesystem_cache(containers_config: ContainersConfig):
        for c in containers_config.containers:
            print("Uploading cache for container:{}".format(c.name))
            local_filename = c.name + "_cache.zip"
            if os.path.exists(local_filename):
                emulation_config = EmulationConfig(agent_ip=c.ip, agent_username="pycr_admin",
                                                   agent_pw="pycr@admin-pw_191", server_connection=False)
                GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=c.ip)
                scp_client = SCPClient(emulation_config.agent_conn.get_transport())
                remote_filename = "/home/pycr_admin/" + local_filename
                scp_client.put(local_filename, remote_filename)
                unzip_cmd = "cd /home/pycr_admin/; unzip " + remote_filename
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=unzip_cmd, conn=emulation_config.agent_conn)
                cmd = "ls /home/pycr_admin/home/"
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                users_w_home = o.decode().split("\n")
                users_w_home = list(filter(lambda x: x != '', users_w_home))
                for user in users_w_home:
                    cmd = "cp -f /home/pycr_admin/home/" + user + "/* /home/" + user + "/"
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)