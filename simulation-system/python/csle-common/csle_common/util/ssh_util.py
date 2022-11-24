from typing import List, Tuple
import time


class SSHUtil:
    """
    Class containing utility functions for SSH connections
    """

    @staticmethod
    def execute_ssh_cmds(cmds: List[str], conn, wait_for_completion: bool = True) -> List[Tuple[bytes, bytes, float]]:
        """
        Executes a list of commands over an ssh connection to the emulation

        :param cmds: the list of commands
        :param conn: the ssh connection
        :param wait_for_completion: whether to wait for completion of the commands or not
        :return: List of tuples (outdata, errdata, total_time)
        """
        results = []
        for cmd in cmds:
            res = SSHUtil.execute_ssh_cmd(cmd=cmd, conn=conn, wait_for_completion=wait_for_completion)
            results.append(res)
        return results

    @staticmethod
    def execute_ssh_cmd(cmd: str, conn, wait_for_completion: bool = True, retries: int = 2) \
            -> Tuple[bytes, bytes, float]:
        """
        Executes an action on the emulation over a ssh connection,
        this is a synchronous operation that waits for the completion of the action before returning

        :param cmd: the command to execute
        :param conn: the ssh connection
        :param wait_for_completion: boolean flag whether to wait for completion or not
        :param retries: number of retries
        :return: outdata, errdata, total_time
        """
        exp = None
        for i in range(retries):
            try:
                transport_conn = conn.get_transport()
                session = transport_conn.open_session(timeout=128)
                start = time.time()
                session.exec_command(cmd)
                outdata, errdata = b'', b''
                # Wait for completion
                while True:
                    # Reading from output streams
                    while session.recv_ready():
                        outdata += session.recv(1000)
                    while session.recv_stderr_ready():
                        errdata += session.recv_stderr(1000)

                    # Check for completion
                    if session.exit_status_ready() or not wait_for_completion:
                        break
                end = time.time()
                total_time = end - start
                return outdata, errdata, total_time
            except Exception as e:
                exp = e
                time.sleep(10)
        raise ConnectionError(f"Connection failed: {str(exp)} {repr(exp)}")
