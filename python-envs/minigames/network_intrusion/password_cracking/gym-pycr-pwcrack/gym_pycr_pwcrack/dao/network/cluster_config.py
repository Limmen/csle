from typing import List
import paramiko
import time
import gym_pycr_pwcrack.constants.constants as constants
from gym_pycr_pwcrack.dao.action_results.action_costs import ActionCosts
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_id import ActionId

class ClusterConfig:
    """
    DTO with data for connecting to the cluster and executing commands
    """

    def __init__(self, agent_ip : str, agent_username: str, agent_pw : str,
                 server_ip: str = None,
                 server_connection : bool = False,
                 server_private_key_file : str = None, server_username : str = None):
        self.agent_ip = agent_ip
        self.agent_username = agent_username
        self.agent_pw = agent_pw
        self.server_ip = server_ip
        self.server_connection = server_connection
        self.server_private_key_file = server_private_key_file
        self.server_username = server_username
        self.server_conn = None
        self.agent_conn = None
        self.relay_channel = None
        self.cluster_services = []
        self.cluster_cves = []

    def connect_server(self):
        """
        Creates a connection to a server that can work as a jumphost

        :return:
        """
        if not self.server_connection:
            raise ValueError("Server connection not enabled, cannot connect to server")
        if self.server_private_key_file is None:
            raise ValueError("Server private key file is not specified, cannot connect to server")
        if self.server_ip is None:
            raise ValueError("Server ip not specified, cannot connect to server")
        if self.server_username is None:
            raise ValueError("Server username not specified, cannot connect to server")
        key = paramiko.RSAKey.from_private_key_file(self.server_private_key_file)
        server_conn = paramiko.SSHClient()
        server_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        server_conn.connect(self.server_ip, username=self.server_username, pkey=key)
        self.server_conn = server_conn

    def connect_agent(self):
        """
        Connects to the agent's host with SSH, either directly or through a jumphost

        :return: None
        """
        print("Connecting to agent host..")

        # Connect to agent using server as a jumphost
        if self.server_connection:
            if self.server_conn is None:
                self.connect_server()
            server_transport = self.server_conn.get_transport()
            agent_addr = (self.agent_ip, 22)
            server_addr = (self.server_ip, 22)

            relay_channel = server_transport.open_channel(constants.SSH.DIRECT_CHANNEL, agent_addr, server_addr)
            self.relay_channel = relay_channel
            agent_conn = paramiko.SSHClient()
            agent_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            agent_conn.connect(self.agent_ip, username=self.agent_username, password=self.agent_pw, sock=relay_channel)
            self.agent_conn = agent_conn
            self.agent_channel = self.agent_conn.invoke_shell()


        # Connect directly to agent with ssh
        else:
            agent_conn = paramiko.SSHClient()
            agent_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            agent_conn.connect(self.agent_ip, username=self.agent_username, password=self.agent_pw)
            self.agent_conn = agent_conn
            self.agent_channel = self.agent_conn.invoke_shell()

        print("Agent host connected successfully")

        self._su_root()

        print("Root access")


    def _su_root(self) -> None:
        """
        Uses an interactive channel to change to root account

        :return: None
        """

        # clear output
        if self.agent_channel.recv_ready():
            output = self.agent_channel.recv(constants.COMMON.DEFAULT_RECV_SIZE)

        self.agent_channel.send(constants.COMMANDS.CHANNEL_SU_ROOT)
        time.sleep(0.2)
        self.agent_channel.send(constants.COMMANDS.CHANNEL_ROOT)
        time.sleep(0.2)

        # clear output
        if self.agent_channel.recv_ready():
            output = self.agent_channel.recv(constants.COMMON.DEFAULT_RECV_SIZE)

        self.agent_channel.send(constants.COMMANDS.CHANNEL_WHOAMI)
        time.sleep(0.2)
        if self.agent_channel.recv_ready():
            output = self.agent_channel.recv(constants.COMMON.DEFAULT_RECV_SIZE)
            output_str = output.decode("utf-8")
            assert "root" in output_str


    def download_cluster_services(self) -> None:
        """
        Downloads a list of services from the server to populate the lookup table

        :return: None
        """
        print("Downloading cluster services...")
        sftp_client = self.agent_conn.open_sftp()
        remote_file = sftp_client.open(constants.COMMON.SERVICES_FILE)
        cluster_services = []
        try:
            for line in remote_file:
                if not line.startswith("#"):
                    service = line.split(" ", 1)[0]
                    service = service.split("\t", 1)[0]
                    cluster_services.append(service)
        finally:
            remote_file.close()
        self.cluster_services = cluster_services
        print("{} services downloaded successfully".format(len(self.cluster_services)))


    def download_cves(self) -> None:
        """
        Downloads a list of CVEs from the server to populate the lookup table

        :return: None
        """
        print("Downloading CVEs...")
        sftp_client = self.agent_conn.open_sftp()
        remote_file = sftp_client.open(constants.COMMON.CVE_FILE, "r")
        cves = []
        try:
            start = time.time()
            for line in remote_file:
                cves.append(line.replace("\n",""))
            end = time.time()
        finally:
            remote_file.close()
        self.cluster_cves = cves
        print("{} cves downloaded successfully in {}s".format(len(self.cluster_cves), end - start))


    def close(self) -> None:
        """
        Closes the cluster connection

        :return: None
        """
        self.agent_conn.close()
        self.relay_channel.close()
        self.server_conn.close()


    def load_action_costs(self, actions: List[Action], dir: str, nmap_ids: List[ActionId],
                          network_service_ids: List[ActionId], shell_ids: List[ActionId]) -> ActionCosts:
        """
        Loads measured action costs from the cluster

        :param actions: list of actions
        :param nmap_ids: list of ids of nmap actions
        :param network_service_ids: list of ids of network service actions
        :param shell_ids: list of ids of shell actions
        :return: action costs
        """
        print("Loading action costs from cluster..")
        action_costs = ActionCosts()
        sftp_client = self.agent_conn.open_sftp()

        # Load Nmap costs
        nmap_actions = list(filter(lambda x: x.id in nmap_ids, actions))
        for a in nmap_actions:
            file_name = dir + str(a.id.value)
            if not a.subnet and a.ip is not None:
                file_name = file_name + "_" + a.ip
            file_name = file_name + "_cost.txt"
            remote_file = None
            try:
                remote_file = sftp_client.open(file_name, mode="r")
                cost_str = remote_file.read()
                cost = float(cost_str)
                action_costs.add_cost(action_id=a.id, ip=a.ip, cost=cost)
                a.cost = cost
            except:
                pass
            finally:
                if remote_file is not None:
                    remote_file.close()

        # Load network service actions costs
        network_service_actions = list(filter(lambda x: x.id in network_service_ids, actions))
        for a in network_service_actions:
            file_name = dir + str(a.id.value)
            file_name = file_name + "_" + a.ip
            file_name = file_name + "_cost.txt"
            remote_file = None
            try:
                remote_file = sftp_client.open(file_name, mode="r")
                cost_str = remote_file.read()
                cost = float(cost_str)
                action_costs.service_add_cost(action_id=a.id, ip=a.ip, cost=cost)
                a.cost = cost
            except:
                pass
            finally:
                if remote_file is not None:
                    remote_file.close()

        # Load shell action costs which are user and service specific
        shell_actions = list(filter(lambda x: x.id in shell_ids, actions))
        for a in shell_actions:
            id = a.id
            cmd = constants.COMMANDS.LIST_CACHE + dir + " | grep " + str(id.value) + "_"
            stdin, stdout, stderr = self.agent_conn.exec_command(cmd)
            file_list = []
            for line in stdout:
                line_str = line.replace("\n", "")
                if "_cost" in line_str:
                    file_list.append(line_str)
            for file in file_list:
                parts = file.split("_")
                ip = parts[1]
                service = parts[2]
                user = parts[3]
                remote_file = None
                try:
                    remote_file = sftp_client.open(file, mode="r")
                    cost_str = remote_file.read()
                    cost = float(cost_str)
                    action_costs.find_add_cost(action_id=id, ip=ip, cost=cost, user=user, service=service)
                    a.cost = cost
                except Exception as e:
                    print("{}".format(str(e)))
                finally:
                    if remote_file is not None:
                        remote_file.close()

        print("Successfully loaded {} action costs from cluster".format(len(action_costs.costs)))
        return action_costs