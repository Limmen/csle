import select
import telnetlib
import threading
import time

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

import paramiko

class ForwardServer(SocketServer.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


class Handler(SocketServer.BaseRequestHandler):
    def handle(self):
        chan = self.server.ssh_transport.open_channel(
            "direct-tcpip",
            (self.server.chain_host, self.server.chain_port),
            self.request.getpeername(),
        )
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)

        chan.close()
        self.request.close()


class ForwardTunnelThread(threading.Thread):

    def __init__(self, local_port, remote_host, remote_port, transport):
        super().__init__()
        self.local_port = local_port
        self.remote_host = remote_host
        self.transport = transport
        self.remote_port = remote_port
        self.forward_server = ForwardServer(("", local_port), Handler)
        self.forward_server.ssh_transport = self.transport
        self.forward_server.chain_host = self.remote_host
        self.forward_server.chain_port = self.remote_port
        self.daemon = True

    def run(self):
        self.forward_server.serve_forever()


def main():
    server = ("172.18.1.191",22)
    remote = ("172.18.1.3", 23)
    port = 4000
    password = "agent"
    username = "agent"

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        server[0],
        server[1],
        username=username,
        password=password,
    )
    print("Now forwarding port {} to {}:{}".format(str(port), remote[0], remote[1]))
    server_thread = ForwardTunnelThread(local_port = port, remote_host = remote[0], remote_port = remote[1],
                                        transport = client.get_transport())
    server_thread.start()
    # server_thread = threading.Thread(target=forward_tunnel,
    #                                         argsf=(port, remote[0], remote[1], client.get_transport(),),
    #                                         daemon=True)
    #server_thread.start()
    PROMPT = b':~$'
    time.sleep(2)
    target_conn = telnetlib.Telnet(host="127.0.0.1", port=4000)
    login_prompt = b"login: "
    timeout = 5
    response = target_conn.read_until(login_prompt, timeout)
    print("{}".format(response))
    target_conn.write(b"admin\n")
    response = target_conn.read_until(b"Password: ")
    print("{}".format(response))
    target_conn.write(b"admin\n")
    response = target_conn.read_until(PROMPT, timeout=5)
    print("{}".format(response))
    target_conn.write(b"ls /\n")
    response = target_conn.read_until(PROMPT, timeout=5)
    print("{}".format(response))
    target_conn.write(b"sudo -v \n")
    response = target_conn.read_until(PROMPT, timeout=5)
    print("{}".format(response))
    wait = True
    while(wait):
        print("shutting down the thread?:{}".format(server_thread.is_alive()))
        if not server_thread.is_alive():
            wait = False
        server_thread.forward_server.shutdown()


if __name__ == "__main__":
    main()