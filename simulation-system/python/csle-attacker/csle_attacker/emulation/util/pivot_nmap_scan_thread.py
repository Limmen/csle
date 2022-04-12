import threading
import time
import csle_common.constants.constants as constants
from csle_common.util.emulation_util import EmulationUtil
from csle_common.util.connection_util import ConnectionUtil
from csle_attacker.emulation.util.nmap_util import NmapUtil
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action_result.nmap_scan_result import NmapScanResult
from csle_common.logging.log import Logger


class PivotNMAPScanThread(threading.Thread):

    def __init__(self, machine: EmulationAttackerMachineObservationState, a: EmulationAttackerAction,
                 s: EmulationEnvState):
        threading.Thread.__init__(self)
        self.machine = machine
        self.a = a
        self.s = s
        self.total_time = 0

    def run(self) -> None:
        ssh_connections_alive = []
        for c in self.machine.ssh_connections:
            try:
                EmulationUtil.execute_ssh_cmds(cmds = ["ls"], conn=c.conn)
                ssh_connections_alive.append(c)
            except Exception as e:
                new_conn = ConnectionUtil.reconnect_ssh(c)
                ssh_connections_alive.append(new_conn)
        self.machine.ssh_connections = ssh_connections_alive
        ssh_connections_sorted_by_root = sorted(
            self.machine.ssh_connections,
            key=lambda x: (constants.SSH_BACKDOOR.BACKDOOR_PREFIX in x.credential.username, x.root,
                           x.credential.username),
            reverse=True)
        for c in ssh_connections_sorted_by_root:
            cwd = "/home/" + c.credential.username + "/"
            cmds, file_names = self.a.nmap_cmds(machine_ips=self.machine.ips)
            results = []
            for i in range(constants.ENV_CONSTANTS.NUM_RETRIES):
                try:
                    results = EmulationUtil.execute_ssh_cmds(cmds=cmds, conn=c.conn)
                    break
                except Exception as e:
                    Logger.__call__().get_logger().warning(
                        f"exception execution commands for ip:{c.ip}, "
                        f"username: {c.credential.username}, conn: {c.conn}, "
                        f"transport: {c.conn.get_transport()}, active: {c.conn.get_transport().is_active()},"
                        f"{str(e)}, {repr(e)}")
                    c = ConnectionUtil.reconnect_ssh(c)
            total_time = sum(list(map(lambda x: x[2], results)))
            EmulationUtil.log_measured_action_time(
                total_time=total_time, action=self.a, emulation_env_config=self.s.emulation_env_config)

            # Read result
            scan_result = NmapScanResult(hosts=[], ips=self.machine.ips)
            for file_name in file_names:
                for i in range(constants.ENV_CONSTANTS.NUM_RETRIES):
                    try:
                        xml_data = NmapUtil.parse_nmap_scan(
                            file_name=file_name, emulation_env_config=self.s.emulation_env_config,
                            conn=c.conn, dir=cwd)
                        new_scan_result = NmapUtil.parse_nmap_scan_xml(xml_data, ips=self.machine.ips, action=self.a)
                        scan_result = NmapUtil.merge_nmap_scan_results(scan_result_1=scan_result,
                                                                       scan_result_2=new_scan_result)
                        self.machine.reachable.update(scan_result.reachable)
                    except Exception as e:
                        Logger.__call__().get_logger().warning(
                            f"There was an exception parsing the file:{file_name} on ip:{c.ip}, error:{e}")
                        time.sleep(constants.ENV_CONSTANTS.SLEEP_RETRY)