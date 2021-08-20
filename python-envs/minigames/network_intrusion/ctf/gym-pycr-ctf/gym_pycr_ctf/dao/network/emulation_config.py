from typing import List
import paramiko
import time
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.dao.action_results.action_costs import ActionCosts
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.dao.action_results.action_alerts import ActionAlerts


class EmulationConfig:
    """
    DTO with data for connecting to the emulation and executing commands
    """

    def __init__(self, agent_ip : str,  agent_username: str, agent_pw : str,
                 server_ip: str = None,
                 server_connection : bool = False,
                 server_private_key_file : str = None, server_username : str = None,
                 warmup = False, warmup_iterations :int = 500, port_forward_next_port : int = 4000,
                 save_dynamics_model_dir : str = None, skip_exploration : bool = False,
                 save_dynamics_model_file: str = None, save_netconf_file: str = None,
                 save_trajectories_file : str = None, save_system_id_logs_file :str = None,
                 static_attacker_strategy : List[int] = None):
        """
        Initializes the emulation configuration

        :param agent_ip: the ip of the Kali container of the attacker in the emulation
        :param agent_username: the username of the login to the Kali container
        :param agent_pw: the password of the login to the Kali container
        :param server_ip: the ip of the server where the emulation is running
        :param server_connection: whether a jumphost needs to be established to server-ip before connecting
                                  to the emulation
        :param server_private_key_file: path the private key file to use for establishing the jumphost connection
        :param server_username: the username for the jumphost connection
        :param warmup: whether to run a warmup run first to test some actions in the emulation
        :param warmup_iterations: how many iterations to run for the warmup
        :param port_forward_next_port: the port to use for port-forwarding when setting up tunnels
        :param save_dynamics_model_dir: the directory to save/load dynamics models
        :param skip_exploration: boolean flag whether to skip the exploration phase
        :param save_dynamics_model_file: name of the file to save the dynamics model
        :param save_netconf_file: name of the file to save the netconf model
        :param save_trajectories_file: name of the file to save the stored trajectories from the emulation
        :param save_system_id_logs_file: name of the file to save the system-id logs
        :param static_attacker_strategy: if training only the defender, a static attacker strategy
        """
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
        self.emulation_services = []
        self.emulation_cves = []
        self.warmup = warmup
        self.warmup_iterations = warmup_iterations
        self.port_forward_next_port = port_forward_next_port
        self.ids_router = False
        self.ids_router_ip = ""
        self.router_conn = None
        self.skip_exploration = skip_exploration
        self.save_dynamics_model_dir = save_dynamics_model_dir
        self.save_dynamics_model_file = save_dynamics_model_file
        self.save_netconf_file = save_netconf_file
        self.save_trajectories_file = save_trajectories_file
        self.save_system_id_logs_file = save_system_id_logs_file
        self.static_attacker_strategy = static_attacker_strategy

    def connect_server(self) -> None:
        """
        Creates a connection to a server that can work as a jumphost

        :return: None
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

    def connect_router(self) -> None:
        """
        Connects to the router of the emulation

        :return: None
        """
        print("Connecting to router host..")
        agent_addr = (self.agent_ip, 22)
        target_addr = (self.ids_router_ip, 22)
        agent_transport = self.agent_conn.get_transport()
        relay_channel = agent_transport.open_channel(constants.SSH.DIRECT_CHANNEL, target_addr, agent_addr,
                                                     timeout=3)
        router_conn = paramiko.SSHClient()
        router_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        router_conn.connect(self.ids_router_ip, username="pycr_admin", password="pycr@admin-pw_191",
                            sock=relay_channel, timeout=3)
        self.router_conn = router_conn
        print("Router host connected successfully")

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

        if self.ids_router and self.ids_router_ip != "":
            self.connect_router()

        # self._su_root()
        #
        # print("Root access")

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

    def download_emulation_services(self) -> None:
        """
        Downloads a list of services from the server to populate the lookup table

        :return: None
        """
        print("Downloading emulation services...")
        sftp_client = self.agent_conn.open_sftp()
        remote_file = sftp_client.open(constants.COMMON.SERVICES_FILE)
        emulation_services = []
        try:
            for line in remote_file:
                if not line.startswith("#"):
                    service = line.split(" ", 1)[0]
                    service = service.split("\t", 1)[0]
                    emulation_services.append(service)
        finally:
            remote_file.close()
        self.emulation_services = emulation_services
        print("{} services downloaded successfully".format(len(self.emulation_services)))

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
        self.emulation_cves = cves
        print("{} cves downloaded successfully in {}s".format(len(self.emulation_cves), end - start))

    def close(self) -> None:
        """
        Closes the emulation connection

        :return: None
        """
        if self.agent_conn is not None:
            self.agent_conn.close()
            self.agent_conn = None
        if self.relay_channel is not None:
            self.relay_channel.close()
            self.relay_channel = None
        if self.server_conn is not None:
            self.server_conn.close()
            self.server_conn = None

    def load_action_costs(self, actions: List[AttackerAction], dir: str, nmap_ids: List[AttackerActionId],
                          network_service_ids: List[AttackerActionId], shell_ids: List[AttackerActionId],
                          nikto_ids: List[AttackerActionId], masscan_ids: List[AttackerActionId],
                          action_lookup_d_val: dict) -> ActionCosts:
        """
        Loads measured action costs from the emulation

        :param actions: list of actions
        :param nmap_ids: list of ids of nmap actions
        :param network_service_ids: list of ids of network service actions
        :param shell_ids: list of ids of shell actions
        :param nikto_ids: list of ids of nikto actions
        :param masscan_ids: list of ids of masscan actions
        :param action_lookup_d_val: dict for converting action id to action
        :return: action costs
        """
        print("Loading action costs from emulation..")
        action_costs = ActionCosts()
        sftp_client = self.agent_conn.open_sftp()

        # Load Nmap costs
        cmd = constants.COMMANDS.LIST_CACHE + dir + " | grep _cost"
        stdin, stdout, stderr = self.agent_conn.exec_command(cmd)
        file_list = []
        for line in stdout:
            line_str = line.replace("\n", "")
            file_list.append(line_str)

        nmap_id_values = list(map(lambda x: x.value, nmap_ids))
        masscan_id_values = list(map(lambda x: x.value, masscan_ids))
        nikto_id_values = list(map(lambda x: x.value, nikto_ids))
        nmap_id_values = nmap_id_values+masscan_id_values+nikto_ids
        network_service_actions_id_values = list(map(lambda x: x.value, network_service_ids))
        remote_file = None
        for file in file_list:
            parts = file.split("_")
            id = int(parts[0])
            if id in nmap_id_values:
                try:
                    idx = parts[1]
                    a = action_lookup_d_val[(int(id), int(idx))]
                    ip = parts[2]
                    remote_file = sftp_client.open(file, mode="r")
                    cost_str = remote_file.read()
                    cost = round(float(cost_str), 1)
                    action_costs.add_cost(action_id=a.id, ip=ip, cost=cost)
                    a.cost = cost
                except Exception as e:
                    print("{}".format(str(e)))
                finally:
                    if remote_file is not None:
                        remote_file.close()

            elif id in network_service_actions_id_values:
                try:
                    idx = parts[1]
                    a = action_lookup_d_val[(int(id), int(idx))]
                    ip = parts[2]
                    remote_file = None
                    remote_file = sftp_client.open(file, mode="r")
                    cost_str = remote_file.read()
                    cost = round(float(cost_str),1)
                    action_costs.service_add_cost(action_id=a.id, ip=a.ip, cost=cost)
                    a.cost = cost
                except Exception as e:
                    print("{}".format(str(e)))
                finally:
                    if remote_file is not None:
                        remote_file.close()

        # Load shell action costs which are user and service specific
        shell_actions = list(filter(lambda x: x.id in shell_ids, actions))
        shell_id_values = list(map(lambda x: x.value, shell_ids))
        cmd = constants.COMMANDS.LIST_CACHE + dir + " | grep _cost"
        stdin, stdout, stderr = self.agent_conn.exec_command(cmd)
        file_list = []
        for line in stdout:
            line_str = line.replace("\n", "")
            if "_cost" in line_str:
                file_list.append(line_str)
        for file in file_list:
            parts = file.split("_")
            id = int(parts[0])
            if id in shell_id_values:
                try:
                    parts = file.split("_")
                    idx = parts[1]
                    ip = parts[2]
                    service = parts[3]
                    user = EmulationConfig.extract_username(parts=parts, idx=4, terminal_key="_cost")
                    remote_file = None
                    remote_file = sftp_client.open(file, mode="r")
                    cost_str = remote_file.read()
                    cost = round(float(cost_str), 1)
                    a = action_lookup_d_val[(int(id), int(idx))]
                    action_costs.find_add_cost(action_id=a.id, ip=ip, cost=cost, user=user, service=service)
                    a.cost = cost
                except Exception as e:
                    print("{}".format(str(e)))
                finally:
                    if remote_file is not None:
                        remote_file.close()

        # Load user command action costs which are user specific
        cmd = constants.COMMANDS.LIST_CACHE + dir + " | grep _cost"
        stdin, stdout, stderr = self.agent_conn.exec_command(cmd)
        file_list = []
        for line in stdout:
            line_str = line.replace("\n", "")
            if "_cost" in line_str:
                file_list.append(line_str)
        for file in file_list:
            parts = file.split("_")
            id = int(parts[0])
            if id in shell_id_values:
                try:
                    parts = file.split("_")
                    idx = parts[1]
                    ip = parts[2]
                    service = parts[3]
                    user = EmulationConfig.extract_username(parts=parts, idx=4, terminal_key="_cost")
                    remote_file = None
                    remote_file = sftp_client.open(file, mode="r")
                    cost_str = remote_file.read()
                    cost = round(float(cost_str), 1)
                    action_costs.install_add_cost(action_id=id, ip=ip, cost=cost, user=user)
                    a.cost = cost
                except Exception as e:
                    print("{}".format(str(e)))
                finally:
                    if remote_file is not None:
                        remote_file.close()

        print("Successfully loaded {} action costs from emulation".format(len(action_costs.costs) +
                                                                        len(action_costs.find_costs) +
                                                                        len(action_costs.service_costs) +
                                                                        len(action_costs.install_costs) +
                                                                        len(action_costs.pivot_scan_costs)))
        return action_costs

    def load_action_alerts(self, actions: List[AttackerAction], dir: str, action_ids: List[AttackerActionId],
                           shell_ids: List[AttackerActionId],
                           action_lookup_d_val: dict) -> ActionCosts:
        """
        Load stored action-alerts from the Emulation

        :param actions: the list of attacker actions
        :param dir: the directory to load from
        :param action_ids: a list of the attacker action ids
        :param shell_ids: a list of the shell command action ids
        :param action_lookup_d_val: a dict for looking up action ids and index to find the corresponding id
        :return: An object with the loaded action costs
        """
        print("Loading action alerts from emulation..")
        action_alerts = ActionAlerts()
        sftp_client = self.agent_conn.open_sftp()

        # Load alerts
        cmd = constants.COMMANDS.LIST_CACHE + dir + " | grep _alerts"
        stdin, stdout, stderr = self.agent_conn.exec_command(cmd)
        file_list = []
        for line in stdout:
            line_str = line.replace("\n", "")
            file_list.append(line_str)

        action_ids = list(filter(lambda x: x not in shell_ids, action_ids))
        action_id_values = list(map(lambda x: x.value, action_ids))
        shell_id_values = list(map(lambda x: x.value, shell_ids))
        remote_file = None
        for file in file_list:
            parts = file.split("_")
            id = int(parts[0])
            if id in action_id_values:
                try:
                    idx = parts[1]
                    a = action_lookup_d_val[(int(id), int(idx))]
                    ip = parts[2]
                    if ip == "alerts.txt":
                        ip = a.ip
                    remote_file = sftp_client.open(file, mode="r")
                    alerts_str = remote_file.read().decode()
                    alerts_parts = alerts_str.split(",")
                    sum_priorities = int(alerts_parts[0])
                    num_alerts = int(alerts_parts[1])
                    action_alerts.add_alert(action_id=a.id, ip=ip, alert = (sum_priorities, num_alerts))
                    a.alerts = (sum_priorities, num_alerts)
                except Exception as e:
                    print("{}".format(str(e)))
                finally:
                    if remote_file is not None:
                        remote_file.close()

        # Load shell action costs which are user and service specific
        shell_actions = list(filter(lambda x: x.id in shell_ids, actions))
        shell_id_values = list(map(lambda x: x.value, shell_ids))

        cmd = constants.COMMANDS.LIST_CACHE + dir + " | grep _alerts"
        stdin, stdout, stderr = self.agent_conn.exec_command(cmd)
        file_list = []
        for line in stdout:
            line_str = line.replace("\n", "")
            if "_alerts" in line_str:
                file_list.append(line_str)
        for file in file_list:
            parts = file.split("_")
            id = int(parts[0])
            if id in shell_id_values:
                try:
                    parts = file.split("_")
                    idx = parts[1]
                    ip = parts[2]
                    service = parts[3]
                    user = EmulationConfig.extract_username(parts=parts, idx=4, terminal_key="_alerts")
                    remote_file = None
                    remote_file = sftp_client.open(file, mode="r")
                    alerts_str = remote_file.read().decode()
                    alerts_parts = alerts_str.split(",")
                    sum_priorities = int(alerts_parts[0])
                    num_alerts = int(alerts_parts[1])
                    alert = (sum_priorities, num_alerts)
                    a = action_lookup_d_val[(int(id), int(idx))]
                    action_alerts.user_ip_add_alert(action_id=a.id, ip=ip, alert=alert, user=user, service=service)
                    a.alerts = alert
                except Exception as e:
                    print("{}".format(str(e)))
                finally:
                    if remote_file is not None:
                        remote_file.close()

        print("Successfully loaded {} action alerts from emulation".format(len(action_alerts.alerts) +
                                                                        len(action_alerts.user_ip_alerts) +
                                                                        len(action_alerts.pivot_scan_alerts)))

        return action_alerts

    @staticmethod
    def extract_username(parts : List[str], idx :int, terminal_key: str) -> str:
        """
        Utility funciton for extracting usernames from a set of strings

        :param parts: the strings
        :param idx: the idx
        :param terminal_key: the terminal key when the usernames end
        :return: the usernames
        """
        rest = "_".join(parts[idx:])
        parts2 = rest.split(terminal_key)
        return parts2[0]

    def copy(self, ip: str, username: str, pw: str) -> "EmulationConfig":
        """
        Creates a copy of the emulation config

        :param ip: the ip of the agent in the copy
        :param username: the username of the agent in the copy
        :param pw: the pw of the agent in the copy
        :return: the copy
        """
        c = EmulationConfig(agent_ip=ip, agent_username=username, agent_pw=pw, server_ip=self.server_ip,
                            server_connection=self.server_connection, server_private_key_file=self.server_private_key_file,
                            server_username=self.server_username, warmup=self.warmup,
                            warmup_iterations=self.warmup_iterations,
                            port_forward_next_port=self.port_forward_next_port)
        c.save_dynamics_model_dir = self.save_dynamics_model_dir
        c.save_dynamics_model_file = self.save_dynamics_model_file
        c.save_netconf_file = self.save_netconf_file
        c.save_trajectories_file = self.save_trajectories_file
        c.save_system_id_logs_file = self.save_system_id_logs_file
        c.static_attacker_strategy = self.static_attacker_strategy
        return c


    def __str__(self):
        """
        :return: a string representation of the object.
        """
        return f"agent_ip:{self.agent_ip}, agent_username: {self.agent_username}, agent_pw: {self.agent_pw}, " \
               f"server_ip: {self.server_ip}, sever_connection: {str(self.server_connection)}, " \
               f"private_key_file: {self.server_private_key_file}, server_username: {self.server_username}, " \
               f"warmup: {self.warmup}, warmup_iterations: {self.warmup_iterations}, " \
               f"port_forward_next_port: {self.port_forward_next_port}, " \
               f"save_dynamics_model_dir: {self.save_dynamics_model_dir}, skip_exploration: {self.skip_exploration}," \
               f"save_dynamics_model_file: {self.save_dynamics_model_file}, save_netconf_file: {self.save_netconf_file}, " \
               f"save_trajectories_file: {self.save_trajectories_file}, " \
               f"save_system_id_logs_file: {self.save_system_id_logs_file}, " \
               f"static_attacker_strategy: {self.static_attacker_strategy}"