import select
import telnetlib
import threading
import time
import os
import re
from ftplib import FTP
import ftplib

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

def _is_ftp_dir(ftp_handle, name, guess_by_extension=True):
    """ simply determines if an item listed on the ftp server is a valid directory or not """

    # if the name has a "." in the fourth to last position, its probably a file extension
    # this is MUCH faster than trying to set every file to a working directory, and will work 99% of time.
    if guess_by_extension is True:
        if len(name) >= 4:
            if name[-4] == '.':
                return False

    original_cwd = ftp_handle.pwd()  # remember the current working directory
    try:
        ftp_handle.cwd(name)  # try to set directory to new name
        ftp_handle.cwd(original_cwd)  # set it back to what it was
        return True

    except ftplib.error_perm as e:
        print(e)
        return False

    except Exception as e:
        print(e)
        return False


def _make_parent_dir(fpath):
    """ ensures the parent directory of a filepath exists """
    dirname = os.path.dirname(fpath)
    while not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
            print("created {0}".format(dirname))
        except OSError:
            _make_parent_dir(dirname)


def _download_ftp_file(ftp_handle, name, dest, overwrite):
    """ downloads a single file from an ftp server """
    _make_parent_dir(dest.lstrip("/"))
    if not os.path.exists(dest) or overwrite is True:
        try:
            with open(dest, 'wb') as f:
                ftp_handle.retrbinary("RETR {0}".format(name), f.write)
            print("downloaded: {0}".format(dest))
        except FileNotFoundError:
            print("FAILED: {0}".format(dest))
    else:
        print("already exists: {0}".format(dest))


def _file_name_match_patern(pattern, name):
    """ returns True if filename matches the pattern"""
    if pattern is None:
        return True
    else:
        return bool(re.match(pattern, name))


def _mirror_ftp_dir(ftp_handle, name, overwrite, guess_by_extension, pattern):
    """ replicates a directory on an ftp server recursively """
    for item in ftp_handle.nlst(name):
        if _is_ftp_dir(ftp_handle, item, guess_by_extension):
            _mirror_ftp_dir(ftp_handle, item, overwrite, guess_by_extension, pattern)
        else:
            if _file_name_match_patern(pattern, name):
                _download_ftp_file(ftp_handle, item, item, overwrite)
            else:
                # quietly skip the file
                pass


def download_ftp_tree(ftp_handle, path, destination, pattern=None, overwrite=False, guess_by_extension=True):
    """
    Downloads an entire directory tree from an ftp server to the local destination
    :param ftp_handle: an authenticated ftplib.FTP instance
    :param path: the folder on the ftp server to download
    :param destination: the local directory to store the copied folder
    :param pattern: Python regex pattern, only files that match this pattern will be downloaded.
    :param overwrite: set to True to force re-download of all files, even if they appear to exist already
    :param guess_by_extension: It takes a while to explicitly check if every item is a directory or a file.
        if this flag is set to True, it will assume any file ending with a three character extension ".???" is
        a file and not a directory. Set to False if some folders may have a "." in their names -4th position.
    """
    path = path.lstrip("/")
    original_directory = os.getcwd()  # remember working directory before function is executed
    os.chdir(destination)  # change working directory to ftp mirror directory

    _mirror_ftp_dir(
        ftp_handle,
        path,
        pattern=pattern,
        overwrite=overwrite,
        guess_by_extension=guess_by_extension)

    os.chdir(original_directory)  # reset working directory to what it was before function exec


def _file_name_match_patern(pattern, name):
    """ returns True if filename matches the pattern"""
    if pattern is None:
        return True
    else:
        return bool(re.match(pattern, name))


def _recursive_search(ftp_handle, name, pattern):
    """ replicates a directory on an ftp server recursively """
    for item in ftp_handle.nlst(name):
        #print("item?:{}".format(item))
        if _is_ftp_dir(ftp_handle, item):
            _recursive_search(ftp_handle, item, pattern)
        else:
            if _file_name_match_patern(pattern, name):
                print("match")
            else:
                # quietly skip the file
                pass

def ftp_test():
    server = ("172.18.1.191", 22)
    remote = ("172.18.1.79", 21)
    #key = paramiko.RSAKey.from_private_key_file("/Users/kimham/.ssh/pycr_id_rsa")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('172.18.1.191', username='agent', password="agent")
    print("connected")
    shell = client.invoke_shell()

    shell_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

    # clear output
    if shell.recv_ready():
        output = shell.recv(5000)

    #shell.send("lftp ftp://pi:pi@172.18.1.79\n")
    shell.send("lftp ftp://ftp:ftp@172.18.1.79\n")
    time.sleep(0.2)
    if shell.recv_ready():
        output = shell.recv(5000)
        print("output:{}".format(output))

    shell.send("ls -a1\n")
    time.sleep(0.2)
    if shell.recv_ready():
        output = shell.recv(5000)
        output_str = output.decode("utf-8")
        output_str = shell_escape.sub("", output_str)
        output_list = output_str.split('\r\n')
        output_list = output_list[1:-1]  # remove command ([0]) and prompt ([-1])
        print("output:{}".format(output_list))

    shell.send("find / | grep 'flag*'\n")
    output = b""
    print("recv ready:{}".format(shell.recv_ready()))
    # # clear output
    # if shell.recv_ready():
    #     shell.recv(5000)
    command_complete = False
    max_timeouts = 3
    timeouts = 0
    while not command_complete:
        while not shell.recv_ready():
            time.sleep(0.5)
            #print("timeouts:{}".format(timeouts))
            # if timeouts > max_timeouts:
            #     break
            timeouts += 1
        # if shell.recv_ready():
        #     output += shell.recv(10000000000)
        #     timeouts = 0
        # else:
        #     break
        output += shell.recv(10000000000)
        if ":~>" in output.decode():
            command_complete = True

    output_str = output.decode("utf-8")
    output_str = shell_escape.sub("", output_str)
    output_list = output_str.split('\r\n')
    output_list = output_list[1:-1]  # remove command ([0]) and prompt ([-1])
    output_list = list(filter(lambda x: not "Access failed" in x, output_list))
    print("output:{}".format(output_list))




if __name__ == "__main__":
    ftp_test()
    #main()