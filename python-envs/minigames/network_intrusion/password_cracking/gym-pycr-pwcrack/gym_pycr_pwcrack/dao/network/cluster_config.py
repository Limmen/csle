import paramiko
import time

class ClusterConfig:
    """
    DTO with data for connecting to the cluster and executing commands
    """

    def __init__(self, server_ip : str, agent_ip : str, agent_username: str, agent_pw : str,
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

            relay_channel = server_transport.open_channel("direct-tcpip", agent_addr, server_addr)
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
            agent_conn.connect(self.server_ip, username=self.server_username, password=self.agent_pw)
            self.agent_conn = agent_conn
            self.agent_channel = self.agent_conn.invoke_shell()

        print("Agent host connected successfully")

        self._su_root()
        root_conn = paramiko.SSHClient()
        root_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        root_command_channel = root_conn.connect(self.agent_ip, username=self.agent_username, password=self.agent_pw, sock=relay_channel)

        print("Root access")


    def _su_root(self):

        # clear output
        if self.agent_channel.recv_ready():
            output = self.agent_channel.recv(5000)

        self.agent_channel.send("su root\n")
        time.sleep(0.2)
        self.agent_channel.send("root\n")
        time.sleep(0.2)

        # clear output
        if self.agent_channel.recv_ready():
            output = self.agent_channel.recv(5000)

        self.agent_channel.send("whoami\n")
        time.sleep(0.2)
        if self.agent_channel.recv_ready():
            output = self.agent_channel.recv(5000)
            output_str = output.decode("utf-8")
            assert "root" in output_str


    def close(self):
        self.agent_conn.close()
        self.relay_channel.close()
        self.server_conn.close()