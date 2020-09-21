from typing import Union, List
import numpy as np
from gym_pycr_pwcrack.dao.network.env_state import EnvState
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig
from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.network.transport_protocol import TransportProtocol
from gym_pycr_pwcrack.dao.observation.machine_observation_state import MachineObservationState
from gym_pycr_pwcrack.dao.observation.port_observation_state import PortObservationState

class Simulator:

    @staticmethod
    def transition(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        if a.type == ActionType.RECON:
            return Simulator.recon_action(s=s, a=a, env_config=env_config)
        elif a.type == ActionType.EXPLOIT:
            return Simulator.exploit_action(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Action type not recognized")

    @staticmethod
    def recon_action(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        if a.id == ActionId.TCP_SYN_STEALTH_SCAN_SUBNET or a.id == ActionId.TCP_SYN_STEALTH_SCAN_HOST:
            return Simulator.simulate_tcp_syn_stealth_scan(s=s,a=a,env_config=env_config)
        elif a.id == ActionId.PING_SCAN_SUBNET or a.id == ActionId.PING_SCAN_HOST:
            return Simulator.simulate_ping_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.UDP_PORT_SCAN_SUBNET or a.id == ActionId.UDP_PORT_SCAN_HOST:
            return Simulator.simulate_udp_port_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET or a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_HOST:
            return Simulator.simulate_con_non_stealth_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_FIN_SCAN_SUBNET or a.id == ActionId.TCP_FIN_SCAN_HOST:
            return Simulator.simulate_fin_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_NULL_SCAN_SUBNET or a.id == ActionId.TCP_NULL_SCAN_HOST:
            return Simulator.simulate_tcp_null_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_XMAS_TREE_SCAN_HOST or a.id == ActionId.TCP_XMAS_TREE_SCAN_SUBNET:
            return Simulator.simulate_tcp_xmas_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.OS_DETECTION_SCAN_HOST or a.id == ActionId.OS_DETECTION_SCAN_SUBNET:
            return Simulator.simulate_os_detection_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.VULSCAN_HOST or a.id == ActionId.VULSCAN_SUBNET:
            return Simulator.simulate_vulscan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.NMAP_VULNERS_HOST or a.id == ActionId.NMAP_VULNERS_HOST:
            return Simulator.simulate_nmap_vulners(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET:
            return Simulator.simulate_telnet_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET:
            return Simulator.simulate_ssh_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET:
            return Simulator.simulate_ftp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET:
            return Simulator.simulate_cassandra_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET:
            return Simulator.simulate_irc_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET:
            return Simulator.simulate_mongo_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET:
            return Simulator.simulate_mysql_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET:
            return Simulator.simulate_smtp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET:
            return Simulator.simulate_postgres_same_user_dictionary(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Recon action: {} not recognized".format(a.id))

    @staticmethod
    def exploit_action(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_tcp_syn_stealth_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        s_prime = Simulator.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                      miss_p=env_config.syn_stealth_scan_miss_p,
                                                      protocol=TransportProtocol.TCP)
        return s_prime, 0, False

    @staticmethod
    def simulate_ping_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        s_prime = Simulator.simulate_host_scan_helper(s=s,a=a,env_config=env_config, miss_p=env_config.ping_scan_miss_p,
                                                      os=False)
        return s_prime, 0, False

    @staticmethod
    def simulate_udp_port_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        s_prime = Simulator.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                      miss_p=env_config.udp_port_scan_miss_p, protocol=TransportProtocol.UDP)
        return s_prime, 0, False

    @staticmethod
    def simulate_con_non_stealth_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        s_prime = Simulator.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                      miss_p=env_config.syn_stealth_scan_miss_p,
                                                      protocol=TransportProtocol.TCP)
        return s_prime, 0, False

    @staticmethod
    def simulate_fin_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        s_prime = Simulator.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                      miss_p=env_config.syn_stealth_scan_miss_p,
                                                      protocol=TransportProtocol.TCP)
        return s_prime, 0, False

    @staticmethod
    def simulate_tcp_null_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        s_prime = Simulator.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                      miss_p=env_config.syn_stealth_scan_miss_p,
                                                      protocol=TransportProtocol.TCP)
        return s_prime, 0, False

    @staticmethod
    def simulate_tcp_xmas_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        s_prime = Simulator.simulate_port_scan_helper(s=s, a=a, env_config=env_config,
                                                      miss_p=env_config.syn_stealth_scan_miss_p,
                                                      protocol=TransportProtocol.TCP)
        return s_prime, 0, False

    @staticmethod
    def simulate_os_detection_scan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        s_prime = Simulator.simulate_host_scan_helper(s=s, a=a, env_config=env_config,
                                                      miss_p=env_config.os_scan_miss_p, os=True)
        return s_prime, 0, False

    @staticmethod
    def simulate_vulscan(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_nmap_vulners(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_telnet_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_ssh_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_ftp_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_cassandra_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_irc_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_mongo_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_mysql_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_smtp_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def simulate_postgres_same_user_dictionary(s: EnvState, a: Action, env_config: EnvConfig) -> Union[EnvState, int, bool]:
        return s, 0, False

    @staticmethod
    def merge_new_obs_with_old(old_machines_obs: List[MachineObservationState],
                               new_machines_obs: List[MachineObservationState]):
        merged_machines = []
        for o_m in new_machines_obs:
            for n_m in old_machines_obs:
                if n_m.ip == o_m.ip:
                    o_m = Simulator.merge_new_machine_obs_with_old_machine_obs(o_m, n_m)
            merged_machines.append(o_m)
        return merged_machines

    @staticmethod
    def merge_new_machine_obs_with_old_machine_obs(o_m : MachineObservationState, n_m: MachineObservationState):
        if n_m == None:
            return o_m
        merged_ports = n_m.ports
        for o_p in o_m.ports:
            exist = False
            for m_p in merged_ports:
                if o_p.port == m_p.port and o_p.protocol == m_p.protocol:
                    exist = True
            if not exist:
                merged_ports.append(o_p)
        n_m.ports = merged_ports
        return n_m

    @staticmethod
    def simulate_port_scan_helper(s: EnvState, a: Action, env_config: EnvConfig, miss_p : float,
                                  protocol = TransportProtocol.TCP) -> EnvState:
        if not a.subnet:
            new_m_obs = None
            for node in env_config.network_conf.nodes:
                if node.ip == a.ip:
                    new_m_obs = MachineObservationState(ip=node.ip)
                    for service in node.services:
                        if service.protocol == protocol and \
                                not np.random.rand() < miss_p:
                            port_obs = PortObservationState(port=service.port, open=True, service=service.name,
                                                            protocol=protocol)
                            new_m_obs.ports.append(port_obs)
            new_machines_obs = []
            merged = False
            for o_m in s.obs_state.machines:
                if o_m.ip == a.ip:
                    merged_machine_obs = Simulator.merge_new_machine_obs_with_old_machine_obs(s.obs_state.machines,
                                                                                              new_m_obs)
                    new_machines_obs.append(merged_machine_obs)
                    merged = True
                else:
                    new_machines_obs.append(o_m)
            if not merged:
                new_machines_obs.append(new_m_obs)
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs
        else:
            new_m_obs = []
            for node in env_config.network_conf.nodes:
                m_obs = MachineObservationState(ip=node.ip)
                for service in node.services:
                    if service.protocol == protocol and \
                            not np.random.rand() < miss_p:
                        port_obs = PortObservationState(port=service.port, open=True, service=service.name,
                                                        protocol=protocol)
                        m_obs.ports.append(port_obs)
                new_m_obs.append(m_obs)
            new_machines_obs = Simulator.merge_new_obs_with_old(s.obs_state.machines, new_m_obs)
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs
        return s_prime

    @staticmethod
    def simulate_host_scan_helper(s: EnvState, a: Action, env_config: EnvConfig, miss_p: float, os=False) -> EnvState:
        if not a.subnet:
            new_m_obs = None
            for node in env_config.network_conf.nodes:
                if node.ip == a.ip and not np.random.rand() < env_config.os_scan_miss_p:
                    new_m_obs = MachineObservationState(ip=node.ip)
                    if os:
                        new_m_obs.os = node.os
            new_machines_obs = []
            merged = False
            for o_m in s.obs_state.machines:
                if o_m.ip == a.ip:
                    merged_machine_obs = Simulator.merge_new_machine_obs_with_old_machine_obs(s.obs_state.machines,
                                                                                              new_m_obs)
                    new_machines_obs.append(merged_machine_obs)
                    merged = True
                else:
                    new_machines_obs.append(o_m)
            if not merged:
                new_machines_obs.append(new_m_obs)
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs
        else:
            new_m_obs = []
            for node in env_config.network_conf.nodes:
                if not np.random.rand() < env_config.os_scan_miss_p:
                    m_obs = MachineObservationState(ip=node.ip)
                    if os:
                        m_obs.os = node.os
                    new_m_obs.append(m_obs)
            new_machines_obs = Simulator.merge_new_obs_with_old(s.obs_state.machines, new_m_obs)
            s_prime = s
            s_prime.obs_state.machines = new_machines_obs
        return s_prime
