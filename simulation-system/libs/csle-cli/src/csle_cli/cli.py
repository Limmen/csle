"""
CSLE runner

To see options, run:
`csle --help`
"""
import logging
from typing import List, Tuple, Union
import click
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.util.cluster_util import ClusterUtil
from csle_common.util.general_util import GeneralUtil
from csle_cluster.cluster_manager.cluster_controller import ClusterController
from csle_cluster.cluster_manager.cluster_manager_pb2 import DockerContainerDTO
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_cluster.cluster_manager.cluster_manager_pb2 import SnortIdsStatusDTO
from csle_cluster.cluster_manager.cluster_manager_pb2 import ContainerImageDTO

ClusterUtil.set_config_parameters_from_config_file()


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def commands() -> None:
    """
    CSLE CLI Tool
    """
    pass


@click.command("init", help="initializes CSLE and sets up management accounts")
def init() -> None:
    """
    Initializes CSLE and sets up management accounts

    :return: None
    """
    from csle_common.util.management_util import ManagementUtil
    import csle_common.constants.constants as constants
    host_ip = GeneralUtil.get_host_ip()
    start_cluster_manager(host_ip=host_ip)
    leader = ClusterUtil.am_i_leader(ip=host_ip, config=constants.CONFIG_FILE.PARSED_CONFIG)
    if leader:
        ManagementUtil.create_default_management_admin_account()
        ManagementUtil.create_default_management_guest_account()


def start_cluster_manager(host_ip: str) -> None:
    """
    Starts the cluster manager on a given host ip

    :param host_ip: the host ip where to start the cluster manager
    :return: None
    """
    import csle_common.constants.constants as constants
    import csle_collector.constants.constants as collector_constants
    import subprocess
    if not ClusterController.is_cluster_manager_running(ip=host_ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT):
        cmd = constants.COMMANDS.START_CLUSTER_MANAGER.format(constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                                              collector_constants.LOG_FILES.CLUSTER_MANAGER_LOG_DIR,
                                                              collector_constants.LOG_FILES.CLUSTER_MANAGER_LOG_FILE,
                                                              10)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()


def attacker_shell(s: "EmulationEnvState") -> None:
    """
    An interactive shell for executing attacker actions in an emulation environment

    :param s: the state of the emulation
    :return: None
    """
    from csle_attacker.attacker import Attacker
    done = False
    while True:
        raw_input = input("> ")
        raw_input = raw_input.strip()
        if raw_input == "help":
            print("Enter an action id to execute the action, "
                  "press R to reset,"
                  "press S to print the state, press A to print the actions, "
                  "press D to check if done"
                  "press H to print the history of actions")
        elif raw_input == "A":
            print("Attacker actions:")
            for i, a in enumerate(s.attacker_action_config.actions):
                print(f"idx:{i}, a:{a}")
        elif raw_input == "S":
            print(s)
        elif raw_input == "D":
            print(done)
        elif raw_input == "R":
            print("Resetting the state")
            s.reset()
        else:
            attacker_action_idx = int(raw_input)
            attacker_action = s.attacker_action_config.actions[attacker_action_idx]
            s = Attacker.attacker_transition(s=s, attacker_action=attacker_action)


def attacker_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completions for the attacker command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    return emulations


@click.command("attacker", help="emulation-name execution-id")
@click.argument('id', default=-1, type=int)
@click.argument('emulation', default="", type=str, shell_complete=attacker_shell_complete)
def attacker(emulation: str, id: int = -1) -> None:
    """
    Opens an attacker shell in the given emulation execution

    :param emulation: the emulation name
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState

    emulation_execution = MetastoreFacade.get_emulation_execution(ip_first_octet=id, emulation_name=emulation)
    if emulation_execution is not None:
        s = EmulationEnvState(emulation_env_config=emulation_execution.emulation_env_config)
        attacker_shell(s=s)
    else:
        click.secho(f"name: {emulation} not recognized", fg="red", bold=True)


def list_csle_gym_envs() -> None:
    """
    Lists the registered OpenAI gym environments

    :return: None
    """
    import gymnasium as gym
    import csle_common.constants.constants as constants

    click.secho("Registered OpenAI gym environments:", fg="magenta", bold=True)
    for env_name, env_obj in gym.registry.items():
        if constants.CSLE.NAME in env_name:
            click.secho(f"{env_name}", bold=False)


def emulation_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completions for the em command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    return emulations + ["emulation", "--host", "--stats", "--kafka", "--clients"]


@click.option('--host', is_flag=True, help='Check the status of the Host managers')
@click.option('--stats', is_flag=True, help='Check the status of the stats manager')
@click.option('--kafka', is_flag=True, help='Check the status of the Kafka manager')
@click.option('--snortids', is_flag=True, help='Check the status of the Snort IDS manager')
@click.option('--clients', is_flag=True, help='Check the number of active clients of the emulation')
@click.option('--executions', is_flag=True, help='Check the executions')
@click.argument('emulation', default="", type=str, shell_complete=emulation_shell_complete)
@click.command("em", help="emulation-name")
def em(emulation: str, clients: bool, snortids: bool, kafka: bool, stats: bool, host: bool, executions: bool) -> None:
    """
    Extracts status information of a given emulation

    :param emulation: the emulation name
    :param clients: if true, print information about the client population
    :param snortids: if true, print information about the Snort ids manager
    :param kafka: if true, print information about the kafka manager
    :param stats: if true, print information about the statsmanager
    :param host: if true, print information about the hostmanagers
    :param executions: if true, print information about executions
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    import csle_common.constants.constants as constants

    emulation_env_config = MetastoreFacade.get_emulation_by_name(name=emulation)
    execs = MetastoreFacade.list_emulation_executions_for_a_given_emulation(
        emulation_name=emulation_env_config.name)
    config = MetastoreFacade.get_config(id=1)
    if emulation_env_config is not None:
        click.secho(f"Executions of: {emulation}", fg="magenta", bold=True)
        for exec in execs:
            click.secho(f"IP ID: {exec.ip_first_octet}, emulation name: {exec.emulation_name}")
        if clients:
            for exec in execs:
                for node in config.cluster_config.cluster_nodes:
                    if node.ip == exec.emulation_env_config.traffic_config.client_population_config.physical_host_ip:
                        clients_dto = ClusterController.get_num_active_clients(
                            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                            emulation=emulation_env_config.name, ip_first_octet=exec.ip_first_octet)
                        click.secho(f"Client population status for execution {exec.ip_first_octet} of {emulation}",
                                    fg="magenta", bold=True)
                        click.secho(f"Active clients: {clients_dto.num_clients}", bold=False)
                        if clients_dto.client_process_active:
                            click.secho("Client process " + f" {click.style('[active]', fg='green')}", bold=False)
                        else:
                            click.secho("Client process " + f" {click.style('[inactive]', fg='red')}", bold=False)
                        if clients_dto.producer_active:
                            click.secho("Producer process " + f" {click.style('[active]', fg='green')}", bold=False)
                        else:
                            click.secho("Producer process " + f" {click.style('[inactive]', fg='red')}", bold=False)
                        click.secho(f"Clients time-step length: "
                                    f"{clients_dto.clients_time_step_len_seconds} seconds", bold=False)
                        click.secho(f"Producer time-step length: "
                                    f"{clients_dto.producer_time_step_len_seconds} seconds", bold=False)
        if snortids:
            for exec in execs:
                statuses: List["SnortIdsStatusDTO"] = []
                for node in config.cluster_config.cluster_nodes:
                    snort_ids_monitors_statuses_dto = ClusterController.get_snort_ids_monitor_thread_statuses(
                        ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                        emulation=emulation_env_config.name, ip_first_octet=exec.ip_first_octet)
                    statuses = statuses + list(snort_ids_monitors_statuses_dto.snortIDSStatuses)
                for snort_ids_monitor_status in statuses:
                    click.secho(f"Snort IDS monitor status for execution {exec.ip_first_octet} of {emulation}",
                                fg="magenta", bold=True)
                    if snort_ids_monitor_status.monitor_running:
                        click.secho("Snort IDS monitor status: "
                                    + f" {click.style('[running]', fg='green')}", bold=False)
                    else:
                        click.secho("Snort IDS monitor status: "
                                    + f" {click.style('[stopped]', fg='red')}", bold=False)
                    if snort_ids_monitor_status.snort_ids_running:
                        click.secho("Snort IDS status: "
                                    + f" {click.style('[running]', fg='green')}", bold=False)
                    else:
                        click.secho("Snort IDS status: "
                                    + f" {click.style('[stopped]', fg='red')}", bold=False)
        if kafka:
            for exec in execs:
                for node in config.cluster_config.cluster_nodes:
                    if node.ip == exec.emulation_env_config.kafka_config.container.physical_host_ip:
                        kafka_dto = ClusterController.get_kafka_status(
                            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                            emulation=emulation_env_config.name, ip_first_octet=exec.ip_first_octet)
                        click.secho(f"Kafka manager status for execution {exec.ip_first_octet} of {emulation}",
                                    fg="magenta", bold=True)
                        if kafka_dto.running:
                            click.secho("Kafka broker status: " + f" {click.style('[running]', fg='green')}",
                                        bold=False)
                        else:
                            click.secho("Kafka broker status: " + f" {click.style('[stopped]', fg='red')}", bold=False)
                        click.secho("Topics:", bold=True)
                        for topic in kafka_dto.topics:
                            click.secho(f"{topic}", bold=False)
        if stats:
            for exec in execs:
                for node in config.cluster_config.cluster_nodes:
                    stats_manager_dto = ClusterController.get_docker_stats_manager_status(
                        ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
                    click.secho(f"Docker stats manager status for IP:{node.ip} and "
                                f" execution: {exec.ip_first_octet} of {emulation}",
                                fg="magenta", bold=True)
                    click.secho(f"Number of active monitors: {stats_manager_dto.num_monitors}", bold=False)
        if host:
            for exec in execs:
                click.secho(f"Host manager statuses for execution {exec.ip_first_octet} of {emulation}",
                            fg="magenta", bold=True)
                for node in config.cluster_config.cluster_nodes:
                    host_manager_dto = ClusterController.get_host_monitor_threads_statuses(
                        ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                        emulation=emulation_env_config.name, ip_first_octet=exec.ip_first_octet
                    )
                    host_manager_statuses = list(host_manager_dto.hostManagerStatuses)
                    for host_manager_status in host_manager_statuses:
                        click.secho(f"Host manager on {host_manager_status.ip}: "
                                    + f" {click.style('[running]', fg='green')}", bold=False)
                        click.secho(f"monitor_running:{host_manager_status.monitor_running}, "
                                    f"filebeat_running:{host_manager_status.filebeat_running}, "
                                    f"packetbeat_running:{host_manager_status.packetbeat_running}, "
                                    f"metricbeat_running:{host_manager_status.metricbeat_running}, "
                                    f"heartbeat_running:{host_manager_status.heartbeat_running}", bold=False)
    else:
        click.secho(f"name: {emulation} not recognized", fg="red", bold=True)


def start_traffic_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completions for the start traffic command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    return emulations + ["--mu", "--lamb", "--t", "--nc"]


@click.argument('id', default=-1, type=int)
@click.argument('emulation', default="", type=str, shell_complete=start_traffic_shell_complete)
@click.command("start_traffic", help="emulation-name execution-id")
def start_traffic(emulation: str, id: int) -> None:
    """
    Starts the traffic and client population on a given emulation

    :param emulation: the emulation to start the traffic of
    :param id: the id of the execution
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    import csle_common.constants.constants as constants
    execution = MetastoreFacade.get_emulation_execution(ip_first_octet=id, emulation_name=emulation)
    if execution is not None:
        emulation_env_config = execution.emulation_env_config
        click.secho(f"Starting client population with "
                    f"config:{emulation_env_config.traffic_config.client_population_config}")
        config = MetastoreFacade.get_config(id=1)
        for node in config.cluster_config.cluster_nodes:
            if node.ip == execution.emulation_env_config.traffic_config.client_population_config.physical_host_ip:
                ClusterController.start_client_population(
                    ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                    emulation=execution.emulation_env_config.name,
                    ip_first_octet=execution.ip_first_octet)
    else:
        click.secho(f"execution {id} of emulation {emulation} not recognized", fg="red", bold=True)


def stop_traffic_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Completion suggestions for the traffic command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    return emulations


@click.argument('id', default=-1, type=int)
@click.argument('emulation', default="", shell_complete=stop_traffic_shell_complete)
@click.command("stop_traffic", help="emulation-name execution-id")
def stop_traffic(emulation: str, id: int) -> None:
    """
    Stops the traffic and client population on a given emulation

    :param emulation: the emulation to start the traffic of
    :param id: the execution id
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    import csle_common.constants.constants as constants
    exec = MetastoreFacade.get_emulation_execution(ip_first_octet=id, emulation_name=emulation)
    if exec is None:
        click.secho(f"execution {id} of emulation {emulation} not recognized", fg="red", bold=True)
        return
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        ClusterController.stop_traffic_generators(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=exec.emulation_env_config.name,
            ip_first_octet=exec.ip_first_octet)
        if node.ip == exec.emulation_env_config.traffic_config.client_population_config.physical_host_ip:
            ClusterController.stop_client_population(
                ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=exec.emulation_env_config.name,
                ip_first_octet=exec.ip_first_octet)


def shell_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Shell completion for the shell command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.controllers.container_controller import ContainerController
    running_containers: List[Tuple[str, str, str]] = ContainerController.list_all_running_containers()
    stopped_containers: List[Tuple[str, str, str]] = ContainerController.list_all_stopped_containers()
    containers: List[Tuple[str, str, str]] = running_containers + stopped_containers
    container_names: List[str] = list(map(lambda x: x[0], containers))
    return container_names


@click.argument('container', default="", shell_complete=shell_shell_complete)
@click.command("shell", help="container-name")
def shell(container: str) -> None:
    """
    Command for opening a shell inside a running container

    :param container: the name of the container
    :return: None
    """
    import socket
    import netifaces
    from csle_common.controllers.container_controller import ContainerController
    import csle_collector.constants.constants as collector_constants
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade

    running_containers = ContainerController.list_all_running_containers()
    container_found = False
    for rc in running_containers:
        if rc[0] == container:
            container_found = True
            break
    if container_found:
        cmd = f"docker exec -it {container} /bin/bash"
        click.secho(f"To open a shell in container:{container}, run: '{cmd}'", bold=False)
    else:
        hostname = socket.gethostname()
        try:
            ip = netifaces.ifaddresses(collector_constants.INTERFACES.ETH0)[netifaces.AF_INET][0][
                collector_constants.INTERFACES.ADDR]
        except Exception:
            ip = socket.gethostbyname(hostname)
        click.secho(f"Container: {container} not found among running containers on the current server "
                    f"with ip: {ip}",
                    fg="red", bold=False)
        config = MetastoreFacade.get_config(id=1)
        for node in config.cluster_config.cluster_nodes:
            running_containers_dto = ClusterController.list_all_running_containers(
                ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
            container_names = list(map(lambda x: x.name, running_containers_dto.runningContainers))
            if container in container_names:
                click.secho(f"Container: {container} found among running containers on server "
                            f"with ip: {node.ip}, to access it with a shell, login to the "
                            f"server with ip {node.ip} and run csle shell {container}'", fg="red", bold=False)


def run_emulation(emulation_env_config: "EmulationEnvConfig", no_traffic: bool, no_clients: bool,
                  no_beats: bool, id: int = -1) -> None:
    """
    Runs an emulation with the given config

    :param emulation_env_config: the config of the emulation to run
    :param id: the id of the execution to create (if not specified the an available id will be automatically assigned)
    :param no_traffic: a boolean parameter that is True if the traffic generators should be skipped
    :param no_clients: a boolean parameter that is True if the client_population should be skipped
    :param no_beats: a boolean parameter that is True if the configuration/starting of beats should be skipped
    :return: None
    """
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    click.secho(f"Starting emulation {emulation_env_config.name}", bold=False)
    ip = GeneralUtil.get_host_ip()
    physical_servers = [ip]
    execution = EmulationEnvController.create_execution(emulation_env_config=emulation_env_config,
                                                        physical_servers=physical_servers, logger=logging.getLogger(),
                                                        id=id)
    ClusterController.run_emulation(execution=execution, no_traffic=no_traffic, no_clients=no_clients,
                                    physical_servers=physical_servers, no_beats=no_beats)


def separate_running_and_stopped_emulations(emulations: List["EmulationEnvConfig"]) -> Tuple[List[str], List[str]]:
    """
    Partitions the set of emulations into a set of running emulations and a set of stopped emulations

    :param emulations: the list of emulations
    :return: running_emulations, stopped_emulations
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    running_emulation_names: List[str] = []
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        running_emulation_names = running_emulation_names + list(ClusterController.list_all_running_emulations(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT).runningEmulations)
    stopped_emulations = []
    running_emulations = []
    for em in emulations:
        if em.name in running_emulation_names:
            running_emulations.append(em.name)
        else:
            stopped_emulations.append(em.name)
    return running_emulations, stopped_emulations


def stop_all_executions_of_emulation(emulation_env_config: "EmulationEnvConfig") -> None:
    """
    Stops the emulation with the given configuration

    :param emulation_env_config: the configuration of the emulation to stop
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    click.secho(f"Stopping all executions of emulation {emulation_env_config.name}", bold=False)
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        ClusterController.stop_all_executions_of_emulation(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation_env_config.name)


def stop_emulation_execution(emulation_env_config: "EmulationEnvConfig", execution_id: int) -> None:
    """
    Stops the emulation with the given configuration

    :param emulation_env_config: the configuration of the emulation to stop
    :param execution_id: id of the execution to stop
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    click.secho(f"Stopping execution {execution_id} of emulation {emulation_env_config.name}", bold=False)
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        ClusterController.stop_execution(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                         emulation=emulation_env_config.name, ip_first_octet=execution_id)


def clean_emulation_statistics() -> None:
    """
    Deletes emulation statistics from the metastore

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    import csle_common.constants.constants as constants

    click.secho("Deleting all emulation statistics from the metastore", bold=False)
    MetastoreFacade.delete_all(constants.METADATA_STORE.EMULATION_STATISTICS_TABLE)


def clean_emulation_executions() -> None:
    """
    Cleans all emulation executions

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    click.secho("Stopping and cleaning all emulation executions", bold=False)
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        ClusterController.clean_all_executions(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_emulation_executions() -> None:
    """
    Stops all emulation executions

    :return: None
    """
    import csle_common.constants.constants as constants

    from csle_common.metastore.metastore_facade import MetastoreFacade
    click.secho("Stopping all emulation executions", bold=False)
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        ClusterController.stop_all_executions(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def clean_emulation_traces() -> None:
    """
    Deletes emulation traces from the metastore

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    import csle_common.constants.constants as constants

    click.secho("Deleting all emulation traces from the metastore", bold=False)
    MetastoreFacade.delete_all(constants.METADATA_STORE.EMULATION_TRACES_TABLE)


def clean_simulation_traces() -> None:
    """
    Deletes simulation traces from the metastore

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    import csle_common.constants.constants as constants

    click.secho("Deleting all simulation traces from the metastore", bold=False)
    MetastoreFacade.delete_all(constants.METADATA_STORE.SIMULATION_TRACES_TABLE)


def clean_all_emulation_executions(emulation_env_config: "EmulationEnvConfig") -> None:
    """
    Cleans the emulation with the given configuration

    :param emulation_env_config: the configuration of the emulation
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    click.secho(f"Cleaning emulation {emulation_env_config.name}", bold=False)
    config = MetastoreFacade.get_config(id=1)
    leader = None
    for node in config.cluster_config.cluster_nodes:
        if not node.leader:
            click.secho(f"Cleaning containers of emulation {emulation_env_config.name} on server {node.ip}", bold=False)
            ClusterController.clean_all_executions_of_emulation(
                ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation_env_config.name)
        else:
            leader = node
    if leader is not None:
        # Clean the leader last since it will remove the overlay networks
        click.secho(f"Cleaning containers of emulation {emulation_env_config.name} on server {leader.ip}", bold=False)
        ClusterController.clean_all_executions_of_emulation(
            ip=leader.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation_env_config.name)

    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(
        emulation_name=emulation_env_config.name)
    for exec in executions:
        MetastoreFacade.remove_emulation_execution(emulation_execution=exec)


def clean_emulation_execution(emulation_env_config: "EmulationEnvConfig", execution_id: int) -> None:
    """
    Cleans an execution of an emulation

    :param execution_id: the id of the execution to clean
    :param emulation_env_config: the configuration of the emulation
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    click.secho(f"Cleaning execution {execution_id} of emulation {emulation_env_config.name}", bold=False)
    config = MetastoreFacade.get_config(id=1)
    leader = None
    for node in config.cluster_config.cluster_nodes:
        if not node.leader:
            click.secho(f"Cleaning containers of emulation {emulation_env_config.name} and execution id:{execution_id} "
                        f"on server {node.ip}", bold=False)
            ClusterController.clean_execution(
                ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation_env_config.name,
                ip_first_octet=execution_id)
        else:
            leader = node
    if leader is not None:
        # Clean the leader last since it will remove the overlay networks
        click.secho(f"Cleaning containers of emulation {emulation_env_config.name} and execution id:{execution_id} "
                    f"on server {leader.ip}", bold=False)
        ClusterController.clean_execution(
            ip=leader.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, emulation=emulation_env_config.name,
            ip_first_octet=execution_id)
    execution = MetastoreFacade.get_emulation_execution(ip_first_octet=execution_id,
                                                        emulation_name=emulation_env_config.name)
    if execution is not None:
        MetastoreFacade.remove_emulation_execution(emulation_execution=execution)


def stop_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completions for the stop command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    running_emulations, stopped_emulations = separate_running_and_stopped_emulations(
        emulations=MetastoreFacade.list_emulations())
    emulations: List[str] = running_emulations
    running_containers = ContainerController.list_all_running_containers()
    containers: List[Tuple[str, str, str]] = running_containers
    container_names: List[str] = list(map(lambda x: x[0], containers))
    return ["prometheus", "node_exporter", "cadvisor", "pgadmin", "grafana", "flask",
            "statsmanager", "all", "emulation_executions"] + emulations + container_names


@click.option('--ip', default="", type=str)
@click.argument('id', default=-1)
@click.argument('entity', default="", shell_complete=stop_shell_complete)
@click.command("stop", help="prometheus | node_exporter | cadvisor | grafana | flask | container-name | "
                            "emulation-name | statsmanager | emulation_executions | pgadmin | all | nginx | postgresql "
                            "| docker | clustermanager")
def stop(entity: str, id: int = -1, ip: str = "") -> None:
    """
    Stops an entity

    :param entity: the name of the container to stop or "all"
    :param id: id when stopping a specific emulation execution
    :param ip: ip when stopping a service on a specific physical server (empty ip means all servers)
    :return: None
    """
    from csle_common.controllers.management_system_controller import ManagementSystemController
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)

    if entity == "all":
        for node in config.cluster_config.cluster_nodes:
            ClusterController.stop_all_running_containers(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        for emulation in MetastoreFacade.list_emulations():
            stop_all_executions_of_emulation(emulation_env_config=emulation)
    elif entity == "node_exporter":
        stop_node_exporter(ip=ip)
    elif entity == "clustermanager":
        ManagementSystemController.stop_cluster_manager()
    elif entity == "prometheus":
        stop_prometheus(ip=ip)
    elif entity == "cadvisor":
        stop_cadvisor(ip=ip)
    elif entity == "pgadmin":
        stop_pgadmin(ip=ip)
    elif entity == "grafana":
        stop_grafana(ip=ip)
    elif entity == "flask":
        stop_flask(ip=ip)
    elif entity == "docker":
        stop_docker_engine(ip=ip)
    elif entity == "nginx":
        stop_nginx(ip=ip)
    elif entity == "postgresql":
        stop_postgresql(ip=ip)
    elif entity == "statsmanager":
        stop_statsmanager(ip=ip)
    elif entity == "emulation_executions":
        stop_emulation_executions()
    else:
        container_stopped = False
        for node in config.cluster_config.cluster_nodes:
            outcome_dto = ClusterController.stop_container(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                                           container_name=entity)
            if outcome_dto.outcome:
                container_stopped = True
        if not container_stopped:
            emulation = MetastoreFacade.get_emulation_by_name(name=entity)
            if emulation is not None:
                if id == -1:
                    stop_all_executions_of_emulation(emulation)
                else:
                    stop_emulation_execution(emulation_env_config=emulation, execution_id=id)
                emulation_stopped = True
            else:
                emulation_stopped = False
            if not emulation_stopped:
                click.secho(f"name: {entity} not recognized", fg="red", bold=True)


def stop_nginx(ip: str) -> None:
    """
    Utility function for stopping nginx

    :param ip: the ip of the node to stop nginx
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_nginx(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_docker_engine(ip: str) -> None:
    """
    Utility function for stopping the docker engine

    :param ip: the ip of the node to stop the docker engine
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_docker_engine(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_postgresql(ip: str) -> None:
    """
    Utility function for stopping PostgreSQL

    :param ip: the ip of the node to stop PostgreSQL
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_postgresql(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_node_exporter(ip: str) -> None:
    """
    Utility function for stopping node exporter

    :param ip: the ip of the node to stop node exporter
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_node_exporter(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_prometheus(ip: str) -> None:
    """
    Utility function for stopping Prometheus

    :param ip: the ip of the node to stop Prometheus
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_prometheus(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_cadvisor(ip: str) -> None:
    """
    Utility function for stopping cAdvisor

    :param ip: the ip of the node to stop cAdvisor
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_cadvisor(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_pgadmin(ip: str) -> None:
    """
    Utility function for stopping pgAdmin

    :param ip: the ip of the node to stop pgAdmin
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_pgadmin(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_grafana(ip: str) -> None:
    """
    Utility function for stopping grafana

    :param ip: the ip of the node to stop grafana
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_grafana(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_flask(ip: str) -> None:
    """
    Utility function for stopping flask

    :param ip: the ip of the node to stop flask
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_flask(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def stop_statsmanager(ip: str) -> None:
    """
    Utility function for stopping the Docker statsmanager

    :param ip: the ip of the node to stop the Docker statsmanager
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.stop_docker_statsmanager(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


@click.argument('max_workers', default=10, type=int)
@click.argument('log_file', default="docker_statsmanager.log", type=str)
@click.argument('log_dir', default="/var/log/csle", type=str)
@click.argument('port', default=50046, type=int)
@click.command("statsmanager", help="port")
def statsmanager(port: int, log_file: str, log_dir: str, max_workers: int) -> None:
    """
    Starts the statsmanager locally

    :param port: the port that the statsmanager will listen to
    :param log_file: extra parameter for starting the docker stats manager
    :param log_dir: extra parameter for starting the docker stats manager
    :param max_workers: extra parameter for starting the docker stats manager
    :return: None
    """
    import csle_collector.docker_stats_manager.docker_stats_manager as docker_stats_manager
    docker_stats_manager.serve(port=port, log_file_name=log_file, log_dir=log_dir, max_workers=max_workers)


@click.argument('max_workers', default=10, type=int)
@click.argument('log_file', default="cluster_manager.log", type=str)
@click.argument('log_dir', default="/var/log/csle", type=str)
@click.argument('port', default=50041, type=int)
@click.command("clustermanager", help="port")
def clustermanager(port: int, log_file: str, log_dir: str, max_workers: int) -> None:
    """
    Starts the clustermanager locally

    :param port: the port that the clustermanager will listen to
    :param log_file: extra parameter for starting the docker stats manager
    :param log_dir: extra parameter for starting the docker stats manager
    :param max_workers: extra parameter for starting the docker stats manager
    :return: None
    """
    import csle_cluster.cluster_manager.cluster_manager as cluster_manager
    cluster_manager.serve(port=port, log_file_name=log_file, log_dir=log_dir, max_workers=max_workers)


def trainingjob_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completion for the training job command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    training_jobs = MetastoreFacade.list_training_jobs()
    training_jobs_ids = list(map(lambda x: x.id, training_jobs))
    return training_jobs_ids


@click.argument('id', default=None, type=int, shell_complete=trainingjob_shell_complete)
@click.command("trainingjob", help="id")
def trainingjob(id: int) -> None:
    """
    Starts a training job with the given id

    :param id: the id of the training job to start
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_agents.job_controllers.training_job_manager import TrainingJobManager

    training_job = MetastoreFacade.get_training_job_config(id=id)
    TrainingJobManager.run_training_job(job_config=training_job)


def systemidentificationjob_shell_complete(ctx, param, incomplete):
    """
    Gets the ids for the shell completion of the system identification jobs

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    sys_id_jobs = MetastoreFacade.list_system_identification_jobs()
    sys_id_jobs_ids = list(map(lambda x: x.id, sys_id_jobs))
    return sys_id_jobs_ids


@click.argument('id', default=None, type=int, shell_complete=systemidentificationjob_shell_complete)
@click.command("systemidentificationjob", help="id")
def systemidentificationjob(id: int) -> None:
    """
    Starts a system identification job with the given id

    :param id: the id of the training job to start
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_system_identification.job_controllers.system_identification_job_manager \
        import SystemIdentificationJobManager

    sys_id_job = MetastoreFacade.get_system_identification_job_config(id=id)
    SystemIdentificationJobManager.run_system_identification_job(job_config=sys_id_job)


def datacollectionjob_shell_complete(ctx, param, incomplete):
    """
    Gets the ids for the completion of the data collection jobs

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    data_collection_jobs = MetastoreFacade.list_data_collection_jobs()
    data_collection_jobs_ids = list(map(lambda x: x.id, data_collection_jobs))
    return data_collection_jobs_ids


@click.argument('id', default=None, type=int, shell_complete=datacollectionjob_shell_complete)
@click.command("datacollectionjob", help="id")
def datacollectionjob(id: int) -> None:
    """
    Starts a data collection job with the given id

    :param id: the id of the training job to start
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_system_identification.job_controllers.data_collection_job_manager \
        import DataCollectionJobManager

    data_collection_job = MetastoreFacade.get_data_collection_job_config(id=id)
    DataCollectionJobManager.run_data_collection_job(job_config=data_collection_job)


def start_docker_stats_manager(port: int = 50046, log_file: str = "docker_stats_manager.log",
                               log_dir: str = "/var/log/csle", max_workers: int = 10) -> None:
    """
    Starts the stats manager as a daemon

    :param port: the port that the docker stats manager will listen to
    :param log_file: log file of the docker stats manager
    :param log_dir: log dir of the docker stats manager
    :param max_workers: max workers of the docker stats manager
    :return: None
    """
    from csle_common.controllers.management_system_controller import ManagementSystemController
    started = ManagementSystemController.start_docker_stats_manager(port=port, log_file=log_file, log_dir=log_dir,
                                                                    max_workers=max_workers)
    if started:
        click.secho(f"Starting docker stats manager on port:{port}, log_file: {log_file}, log_dir: {log_dir}, "
                    f"max_workers: {max_workers}", bold=False)
    else:
        click.secho(f"Docker stats manager is already running on port:{port}", bold=False)


def start_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completion for the start command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """

    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    running_emulations, stopped_emulations = separate_running_and_stopped_emulations(
        emulations=MetastoreFacade.list_emulations())
    emulations = stopped_emulations
    stopped_containers = ContainerController.list_all_stopped_containers()
    containers: List[Tuple[str, str, str]] = stopped_containers
    container_names: List[str] = list(map(lambda x: x[0], containers))
    images: List[Tuple[str, str, str, str, str]] = ContainerController.list_all_images()
    image_names: List[str] = list(map(lambda x: x[0], images))
    return (["prometheus", "node_exporter", "grafana", "cadvisor", "pgadmin", "flask", "all",
             "statsmanager", "training_job", "system_id_job", "--id", "--no_traffic"]
            + emulations + container_names + image_names)


@click.option('--ip', default="", type=str)
@click.option('--id', default=None, type=int)
@click.option('--no_clients', is_flag=True, help='skip starting the client population')
@click.option('--no_traffic', is_flag=True, help='skip starting the traffic generators')
@click.option('--no_network', is_flag=True, help='skip creating network when starting individual container')
@click.option('--no_beats', is_flag=True, help='skip starting and configuring beats')
@click.argument('name', default="", type=str)
@click.argument('entity', default="", type=str, shell_complete=start_shell_complete)
@click.command("start", help="prometheus | node_exporter | grafana | cadvisor | flask | pgadmin | "
                             "container-name | emulation-name | all | statsmanager | training_job "
                             "| system_id_job | nginx | postgresql | docker | clustermanager")
def start(entity: str, no_traffic: bool, name: str, id: int, no_clients: bool, no_network: bool, ip: str,
          no_beats: bool) -> None:
    """
    Starts an entity, e.g., a container or the management system

    :param entity: the container or emulation to start or "all"
    :param name: extra parameter for running a Docker image
    :param no_traffic: a boolean parameter that is True if the traffic generators should be skipped
    :param no_clients: a boolean parameter that is True if the client population should be skipped
    :param no_beats: a boolean parameter that is True if the configuration/starting of beats should be skipped
    :param no_network: a boolean parameter that is True if the network should be skipped when creating a container
    :param id: (optional) an id parameter to identify the entity to start
    :param ip: ip when stopping a service on a specific physical server (empty ip means all servers)
    :return: None
    """
    from csle_agents.job_controllers.training_job_manager import TrainingJobManager
    from csle_system_identification.job_controllers.data_collection_job_manager import DataCollectionJobManager
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade

    config = MetastoreFacade.get_config(id=1)
    if entity == "all":
        for node in config.cluster_config.cluster_nodes:
            ClusterController.start_all_stopped_containers(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    elif entity == "statsmanager":
        start_statsmanager(ip=ip)
    elif entity == "clustermanager":
        start_cluster_manager(host_ip=ip)
    elif entity == "node_exporter":
        start_node_exporter(ip=ip)
    elif entity == "prometheus":
        start_prometheus(ip=ip)
    elif entity == "cadvisor":
        start_cadvisor(ip=ip)
    elif entity == "pgadmin":
        start_pgadmin(ip=ip)
    elif entity == "nginx":
        start_nginx(ip=ip)
    elif entity == "docker":
        start_docker_engine(ip=ip)
    elif entity == "postgresql":
        start_postgresql(ip=ip)
    elif entity == "grafana":
        start_grafana(ip=ip)
    elif entity == "training_job":
        training_job = MetastoreFacade.get_training_job_config(id=id)
        TrainingJobManager.start_training_job_in_background(training_job=training_job)
    elif entity == "system_id_job":
        system_id_job = MetastoreFacade.get_data_collection_job_config(id=id)
        DataCollectionJobManager.start_data_collection_job_in_background(
            data_collection_job=system_id_job)
    elif entity == "flask":
        start_flask(ip=ip)
    else:
        container_started = False
        for node in config.cluster_config.cluster_nodes:
            outcome_dto = ClusterController.start_container(ip=node.ip,
                                                            port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                                            container_name=entity)
            if outcome_dto.outcome:
                container_started = True
        if not container_started:
            emulation_env_config = MetastoreFacade.get_emulation_by_name(name=entity)
            if emulation_env_config is not None:
                run_emulation(emulation_env_config, no_traffic=no_traffic, no_clients=no_clients, id=id,
                              no_beats=no_beats)
                emulation_started = True
            else:
                emulation_started = False
            if not emulation_started:
                image_started = run_image(image=entity, name=name, create_network=(not no_network))
                if not image_started:
                    click.secho(f"name: {entity} not recognized", fg="red", bold=True)


def start_nginx(ip: str) -> None:
    """
    Utility function for starting nginx

    :param ip: the ip of the node to start nginx
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_nginx(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def start_docker_engine(ip: str) -> None:
    """
    Utility function for starting the docker engine

    :param ip: the ip of the node to start the docker engine
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_docker_engine(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def start_postgresql(ip: str) -> None:
    """
    Utility function for starting PostgreSQL

    :param ip: the ip of the node to start PostgreSQL
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_postgresql(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def start_node_exporter(ip: str) -> None:
    """
    Utility function for starting node exporter

    :param ip: the ip of the node to start node exporter
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_node_exporter(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def start_prometheus(ip: str) -> None:
    """
    Utility function for starting Prometheus

    :param ip: the ip of the node to start Prometheus
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_prometheus(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def start_cadvisor(ip: str) -> None:
    """
    Utility function for starting cAdvisor

    :param ip: the ip of the node to start cAdvisor
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade

    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_cadvisor(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def start_pgadmin(ip: str) -> None:
    """
    Utility function for starting pgAdmin

    :param ip: the ip of the node to start pgAdmin
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_pgadmin(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def start_grafana(ip: str) -> None:
    """
    Utility function for starting grafana

    :param ip: the ip of the node to start grafana
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_grafana(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def start_flask(ip: str) -> None:
    """
    Utility function for starting flask

    :param ip: the ip of the node to start flask
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_flask(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def start_statsmanager(ip: str) -> None:
    """
    Utility function for starting the Docker statsmanager

    :param ip: the ip of the node to start the Docker statsmanager
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        if node.ip == ip or ip == "":
            ClusterController.start_docker_statsmanager(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)


def run_image(image: str, name: str, create_network: bool = True, version: str = "0.0.1") -> bool:
    """
    Runs a container with a given image

    :param image: the image of the container
    :param name: the name that the container will be assigned
    :param create_network: whether to create a virtual network or not
    :param version: the version tag
    :return: True if it was started successfully, False otherwise
    """
    from csle_common.controllers.emulation_env_controller import EmulationEnvController
    try:
        EmulationEnvController.run_container(image=image, name=name, create_network=create_network, version=version)
        return True
    except Exception:
        return False


def rm_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completion for the rm command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    running_containers = ContainerController.list_all_running_containers()
    stopped_containers = ContainerController.list_all_stopped_containers()
    containers: List[Tuple[str, str, str]] = running_containers + stopped_containers
    container_names: List[str] = list(map(lambda x: x[0], containers))
    images: List[Tuple[str, str, str, str, str]] = ContainerController.list_all_images()
    image_names: List[str] = list(map(lambda x: x[0], images))
    return (["network-name", "container-name", "image-name", "networks", "images", "containers"] +
            emulations + container_names + image_names)


@click.argument('entity', default="", shell_complete=rm_shell_complete)
@click.command("rm", help="network-name | container-name | image-name | networks | images | containers")
def rm(entity: str) -> None:
    """
    Removes a container, a network, an image, all networks, all images, or all containers

    :param entity: the container(s), network(s), or images(s) to remove
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)

    if entity == "containers":
        for node in config.cluster_config.cluster_nodes:
            ClusterController.remove_all_stopped_containers(ip=node.ip,
                                                            port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    elif entity == "images":
        for node in config.cluster_config.cluster_nodes:
            ClusterController.remove_all_container_images(ip=node.ip,
                                                          port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    elif entity == "networks":
        for node in config.cluster_config.cluster_nodes:
            ClusterController.remove_all_docker_networks(ip=node.ip,
                                                         port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    else:
        rm_name(name=entity)


def clean_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completion for the clean command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    running_containers: List[Tuple[str, str, str]] = ContainerController.list_all_running_containers()
    stopped_containers: List[Tuple[str, str, str]] = ContainerController.list_all_stopped_containers()
    containers: List[Tuple[str, str, str]] = running_containers + stopped_containers
    container_names: List[str] = list(map(lambda x: x[0], containers))
    return ["all", "containers", "emulations", "emulation_traces", "simulation_traces", "emulation_statistics",
            "name", "emulation_executions"] + emulations + container_names


@click.argument('id', default=-1)
@click.argument('entity', default="", shell_complete=clean_shell_complete)
@click.command("clean", help="all | containers | emulations | emulation_traces | simulation_traces "
                             "| emulation_statistics | emulation_executions | name")
def clean(entity: str, id: int = -1) -> None:
    """
    Removes a container, a network, an image, all networks, all images, all containers, all traces, or all statistics

    :param entity: the container(s), network(s), or images(s) to remove
    :param id: if cleaning a specific emulation execution
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)
    if entity == "all":
        for node in config.cluster_config.cluster_nodes:
            ClusterController.stop_all_running_containers(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
            ClusterController.remove_all_stopped_containers(ip=node.ip,
                                                            port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        for emulation in MetastoreFacade.list_emulations():
            clean_all_emulation_executions(emulation_env_config=emulation)
    elif entity == "containers":
        for node in config.cluster_config.cluster_nodes:
            ClusterController.stop_all_running_containers(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
            ClusterController.remove_all_stopped_containers(ip=node.ip,
                                                            port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
    elif entity == "emulations":
        for emulation in MetastoreFacade.list_emulations():
            clean_all_emulation_executions(emulation_env_config=emulation)
    elif entity == "emulation_traces":
        clean_emulation_traces()
    elif entity == "simulation_traces":
        clean_simulation_traces()
    elif entity == "emulation_statistics":
        clean_emulation_statistics()
    elif entity == "emulation_executions":
        clean_emulation_executions()
    else:
        clean_name(name=entity, id=id)


def install_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completion for the install command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    simulations = list(map(lambda x: x.name, MetastoreFacade.list_simulations()))
    images: List[Tuple[str, str, str, str, str]] = ContainerController.list_all_images()
    image_names: List[str] = list(map(lambda x: x[0], images))
    return ["emulations", "simulations", "derived_images",
            "base_images", "metastore", "all"] + emulations + image_names + simulations


@click.argument('entity', default="", shell_complete=install_shell_complete)
@click.command("install", help="emulations | simulations | <emulation_name> | <simulation_name> | derived_images | "
                               "base_images | metastore | all")
def install(entity: str) -> None:
    """
    Installs emulations and simulations in the metastore and creates Docker images

    :param entity: entity to install
    :return: None
    """
    from csle_common.controllers.installation_controller import InstallationController

    if entity == "emulations":
        click.secho("Installing emulations in the metastore", bold=False)
        InstallationController.install_all_emulations()
    elif entity == "simulations":
        click.secho("Installing simulations in the metastore", bold=False)
        InstallationController.install_all_simulations()
    elif entity == "derived_images":
        click.secho("Installing derived Docker images", bold=False)
        InstallationController.install_derived_images()
    elif entity == "base_images":
        click.secho("Installing base Docker images", bold=False)
        InstallationController.install_base_images()
    elif entity == "metastore":
        click.secho("Installing metastore", bold=False)
        InstallationController.install_metastore()
    elif entity == "all":
        click.secho("Installing base Docker images", bold=False)
        InstallationController.install_base_images()
        click.secho("Installing derived Docker images", bold=False)
        InstallationController.install_derived_images()
        click.secho("Installing emulations in the metastore", bold=False)
        InstallationController.install_all_emulations()
        click.secho("Installing simulations in the metastore", bold=False)
        InstallationController.install_all_simulations()
    else:
        click.secho(f"Installing {entity}", bold=False)
        InstallationController.install_emulation(emulation_name=entity)
        InstallationController.install_simulation(simulation_name=entity)
        InstallationController.install_derived_image(image_name=entity)
        InstallationController.install_base_image(image_name=entity)


def uninstall_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Shell completion for the uninstall command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    simulations = list(map(lambda x: x.name, MetastoreFacade.list_simulations()))
    images: List[Tuple[str, str, str, str, str]] = ContainerController.list_all_images()
    image_names: List[str] = list(map(lambda x: x[0], images))
    return ["emulations", "simulations", "derived_images", "base_images",
            "metastore", "all"] + emulations + image_names + simulations


@click.argument('entity', default="", shell_complete=uninstall_shell_complete)
@click.command("uninstall", help="emulations | simulations | <emulation_name> | <simulation_name> | "
                                 "derived_images | base_images | metastore | all")
def uninstall(entity: str) -> None:
    """
    Uninstall emulations and simulations from the metastore and removes Docker images

    :param entity: the entity to uninstall
    :return: None
    """
    from csle_common.controllers.installation_controller import InstallationController

    if entity == "emulations":
        click.secho("Uninstalling emulations in the metastore", bold=False)
        InstallationController.uninstall_all_emulations()
    elif entity == "simulations":
        click.secho("Uninstalling simulations in the metastore", bold=False)
        InstallationController.uninstall_all_simulations()
    elif entity == "derived_images":
        click.secho("Uninstalling derived Docker images", bold=False)
        InstallationController.uninstall_derived_images()
    elif entity == "base_images":
        click.secho("Uninstalling base Docker images", bold=False)
        InstallationController.uninstall_base_images()
    elif entity == "metastore":
        click.secho("Uninstalling metastore", bold=False)
        InstallationController.uninstall_metastore()
    elif entity == "all":
        click.secho("Uninstalling simulations in the metastore", bold=False)
        InstallationController.uninstall_all_simulations()
        click.secho("Uninstalling emulations in the metastore", bold=False)
        InstallationController.uninstall_all_emulations()
        click.secho("Uninstalling derived Docker images", bold=False)
        InstallationController.uninstall_derived_images()
        click.secho("Uninstalling base Docker images", bold=False)
        InstallationController.uninstall_base_images()
        click.secho("Uninstalling metastore", bold=False)
        InstallationController.uninstall_metastore()
    else:
        click.secho(f"Uninstalling {entity}", bold=False)
        InstallationController.uninstall_emulation(emulation_name=entity)
        InstallationController.uninstall_simulation(simulation_name=entity)
        InstallationController.uninstall_derived_image(image_name=entity)
        InstallationController.uninstall_base_image(image_name=entity)


def ls_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Command completion for the ls command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    emulations: List[str] = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    simulations: List[str] = list(map(lambda x: x.name, MetastoreFacade.list_simulations()))
    running_containers = ContainerController.list_all_running_containers()
    stopped_containers = ContainerController.list_all_stopped_containers()
    containers: List[Tuple[str, str, str]] = running_containers + stopped_containers
    container_names: List[str] = list(map(lambda x: x[0], containers))
    images: List[Tuple[str, str, str, str, str]] = ContainerController.list_all_images()
    image_names: List[str] = list(map(lambda x: x[0], images))
    active_networks_names: List[str] = ContainerController.list_all_networks()
    return (["containers", "networks", "images", "emulations", "all", "environments", "prometheus", "node_exporter",
             "cadvisor", "pgadmin", "flask", "statsmanager", "--all", "--running", "--stopped"] + emulations
            + container_names + image_names + active_networks_names + simulations)


@click.command("ls", help="containers | networks | images | emulations | all | environments | prometheus "
                          "| node_exporter | cadvisor | pgadmin | statsmanager | flask | "
                          "simulations | emulation_executions | cluster | nginx | postgresql | docker")
@click.argument('entity', default='all', type=str, shell_complete=ls_shell_complete)
@click.option('--all', is_flag=True, help='list all')
@click.option('--running', is_flag=True, help='list running only (default)')
@click.option('--stopped', is_flag=True, help='list stopped only')
def ls(entity: str, all: bool, running: bool, stopped: bool) -> None:
    """
    Lists the set of containers, networks, images, or emulations, or all

    :param entity: either containers, networks, images, emulations, or all
    :param all: flag that indicates whether all containers/emulations should be listed
    :param running: flag that indicates whether running containers/emulations should be listed (default)
    :param stopped: flag that indicates whether stopped containers/emulations should be listed
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)

    if entity == "all":
        list_all(all=all, running=running, stopped=stopped)
    elif entity == "networks":
        list_networks()
    elif entity == "cluster":
        list_cluster()
    elif entity == "containers":
        if all:
            list_all_containers()
        elif stopped:
            list_stopped_containers()
        else:
            list_running_containers()
    elif entity == "images":
        list_images()
    elif entity == "emulations":
        list_emulations(all=all, stopped=stopped)
    elif entity == "environments":
        list_csle_gym_envs()
    elif entity == "prometheus":
        list_prometheus()
    elif entity == "node_exporter":
        list_node_exporter()
    elif entity == "cadvisor":
        list_cadvisor()
    elif entity == "nginx":
        list_nginx()
    elif entity == "postgresql":
        list_postgresql()
    elif entity == "docker":
        list_docker_engine()
    elif entity == "pgadmin":
        list_pgadmin()
    elif entity == "grafana":
        list_grafana()
    elif entity == "flask":
        list_flask()
    elif entity == "statsmanager":
        list_statsmanager()
    elif entity == "simulations":
        list_simulations()
    elif entity == "emulation_executions":
        list_emulation_executions()
    else:
        container = get_running_container(name=entity)
        if container is not None:
            print_running_container(container=container)
        else:
            container = get_stopped_container(name=entity)
            if container is not None:
                print_stopped_container(container=container)
            else:
                emulation_env_config = MetastoreFacade.get_emulation_by_name(name=entity)
                if emulation_env_config is not None:
                    print_emulation_config(emulation_env_config=emulation_env_config)
                else:
                    net = get_network(name=entity)
                    if net is not None:
                        active_networks_names: List[str] = []
                        for node in config.cluster_config.cluster_nodes:
                            docker_networks_dto = ClusterController.list_all_docker_networks(
                                ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
                            active_networks_names = active_networks_names + list(docker_networks_dto.networks)
                        active = net.name in active_networks_names
                        print_network(net=net, active=active)
                    else:
                        img = get_image(name=entity)
                        if img is not None:
                            print_img(img=img)
                        else:
                            simulation_env_config = MetastoreFacade.get_simulation_by_name(name=entity)
                            if simulation_env_config is not None:
                                print_simulation_config(simulation_config=simulation_env_config)
                            else:
                                click.secho(f"entity: {entity} is not recognized", fg="red", bold=True)


def print_running_container(container: DockerContainerDTO) -> None:
    """
    Utility function for printing information about a running container

    :param container: the container to print
    :return: None
    """
    click.secho(container.name + f" image:{container.image}, ip: {container.ip} {click.style('[running]', fg='green')}",
                bold=False)


def print_stopped_container(container: DockerContainerDTO) -> None:
    """
    Utiltiy function for printing information about a stopped container

    :param container: the stopped container to print
    :return: None
    """
    click.secho(container.name + f" image:{container.image}, ip: {container.ip} {click.style('[stopped]', fg='red')}",
                bold=False)


def print_network(net: "ContainerNetwork", active: bool = False) -> None:
    """
    Utility function for printing a given network

    :param net: the network to print
    :param active: boolean flag whether the network is active or not
    :return: None
    """
    if active:
        click.secho(f"name:{net.name}, subnet_mask:{net.subnet_mask}, subnet_prefix:{net.subnet_prefix} "
                    f"{click.style('[active]', fg='green')}", bold=False)
    else:
        click.secho(f"name:{net.name}, subnet_mask:{net.subnet_mask}, subnet_prefix:{net.subnet_prefix} "
                    f"{click.style('[inactive]', fg='red')}", bold=False)


def print_img(img: ContainerImageDTO) -> None:
    """
    Utility function for printing a given Docker image

    :param img: the image to print
    :return: None
    """
    click.secho(f"name:{img.repoTags}, size:{img.size}B", bold=False)


def list_all(all: bool = False, running: bool = True, stopped: bool = False) -> None:
    """
    Lists all containers, images, networks, and emulations

    :param all: boolean flag whether all containers/emulations should be listed
    :param running: boolean flag whether running containers/emulations should be listed (default)
    :param stopped: boolean flag whether stopped containers/emulations should be listed
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade

    list_cluster()
    list_networks()
    list_all_containers()
    list_images()
    list_emulations(all=all, stopped=stopped, running=running)
    list_emulation_executions()
    list_simulations()
    list_csle_gym_envs()
    click.secho("CSLE management system:", fg="magenta", bold=True)
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.prometheusRunning:
            click.secho("Prometheus status: " + f" {click.style('[running]', fg='green')} "
                                                f"ip: {node.ip}, port:{constants.COMMANDS.PROMETHEUS_PORT}", bold=False)
        else:
            click.secho("Prometheus status: " + f" {click.style('[stopped]', fg='red')} ip: {node.ip}", bold=False)
        if node_status.nodeExporterRunning:
            click.secho("Node exporter status: " + f" {click.style('[running]', fg='green')} "
                                                   f"ip:{node.ip}, port:{constants.COMMANDS.NODE_EXPORTER_PORT}",
                        bold=False)
        else:
            click.secho("Node exporter status: " + f" {click.style('[stopped],', fg='red')} ip:{node.ip}",
                        bold=False)
        if node_status.cAdvisorRunning:
            click.secho("cAdvisor status: " + f" {click.style('[running]', fg='green')} "
                                              f"ip:{node.ip}, port:{constants.COMMANDS.CADVISOR_PORT}", bold=False)
        else:
            click.secho("cAdvisor status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)
        if node_status.pgAdminRunning:
            click.secho("pgAdmin status: " + f" {click.style('[running]', fg='green')} "
                                             f"ip:{node.ip}, port:{constants.COMMANDS.PGADMIN_PORT}", bold=False)
        else:
            click.secho("pgAdmin status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)
        if node_status.grafanaRunning:
            click.secho("Grafana status: " + f" {click.style('[running]', fg='green')} "
                                             f"ip:{node.ip}, port:{constants.COMMANDS.GRAFANA_PORT}", bold=False)
        else:
            click.secho("Grafana status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)
        if node_status.flaskRunning:
            click.secho("REST API (Flask) status: " + f" {click.style('[running]', fg='green')} "
                                                      f"ip:{node.ip}, "
                                                      f"port:{constants.COMMANDS.MANAGEMENT_SYSTEM_PORT}", bold=False)
        else:
            click.secho("REST API (Flask) status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)
        if node_status.nginxRunning:
            click.secho("Nginx status: " + f" {click.style('[running]', fg='green')} "
                                           f"ip:{node.ip}", bold=False)
        else:
            click.secho("Nginx status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)
        if node_status.dockerEngineRunning:
            click.secho("Docker engine status: " + f" {click.style('[running]', fg='green')} "
                                                   f"ip:{node.ip}, port:{constants.COMMANDS.DOCKER_ENGINE_PORT}",
                        bold=False)
        else:
            click.secho("Docker engine status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)
        if node_status.postgreSQLRunning:
            click.secho("PostgreSQL status: " + f" {click.style('[running]', fg='green')} "
                                                f"ip:{node.ip}, port:{constants.CITUS.COORDINATOR_PORT}", bold=False)
        else:
            click.secho("PostgreSQL status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)
    list_statsmanager()


def list_statsmanager() -> None:
    """
    List status of the docker host manager

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    config = MetastoreFacade.get_config(id=1)

    emulations = MetastoreFacade.list_emulations()
    running_emulations, stopped_emulations = separate_running_and_stopped_emulations(emulations=emulations)
    docker_stats_monitor_statuses = []
    for em in emulations:
        if em.name in running_emulations:
            for node in config.cluster_config.cluster_nodes:
                stats_manager_status_dto = ClusterController.get_docker_stats_manager_status(
                    ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT
                )
                docker_stats_monitor_statuses.append((stats_manager_status_dto, node.ip))
            break
    for status_ip in docker_stats_monitor_statuses:
        status, ip = status_ip
        active_monitor_threads = 0
        active_emulations = []
        if status is not None:
            active_monitor_threads = status.num_monitors
            active_emulations = list(status.emulations)

        click.secho("Docker statsmanager status: " + f"{click.style('[running]', fg='green')} "
                                                     f"ip: {ip}, "
                                                     f"port:{constants.GRPC_SERVERS.DOCKER_STATS_MANAGER_PORT}, "
                                                     f"num active monitor threads: "
                                                     f"{active_monitor_threads}, "
                                                     f"active emulations: {','.join(active_emulations)}", bold=False)


def list_grafana() -> None:
    """
    List status of grafana

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.grafanaRunning:
            click.secho("Grafana status: " + f" {click.style('[running]', fg='green')} "
                                             f"ip:{node.ip}, port:{constants.COMMANDS.GRAFANA_PORT}", bold=False)
        else:
            click.secho("Grafana status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)


def list_flask() -> None:
    """
    List status of the management system

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.flaskRunning:
            click.secho("REST API (Flask) status: " + f" {click.style('[running]', fg='green')} "
                                                      f"ip:{node.ip}, "
                                                      f"port:{constants.COMMANDS.MANAGEMENT_SYSTEM_PORT}", bold=False)
        else:
            click.secho("REST API (Flask) status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)


def list_cadvisor() -> None:
    """
    Lists status of cadvisor

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.cAdvisorRunning:
            click.secho("cAdvisor status: " + f" {click.style('[running]', fg='green')} "
                                              f"ip:{node.ip}, port:{constants.COMMANDS.CADVISOR_PORT}", bold=False)
        else:
            click.secho("cAdvisor status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)


def list_nginx() -> None:
    """
    Lists status of nginx

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.nginxRunning:
            click.secho("Nginx status: " + f" {click.style('[running]', fg='green')} "
                                           f"ip:{node.ip}", bold=False)
        else:
            click.secho("Nginx status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)


def list_docker_engine() -> None:
    """
    Lists status of the docker engine

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.dockerEngineRunning:
            click.secho("Docker engine status: " + f" {click.style('[running]', fg='green')} "
                                                   f"ip:{node.ip}, port:{constants.COMMANDS.DOCKER_ENGINE_PORT}",
                        bold=False)
        else:
            click.secho("Docker engine status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)


def list_postgresql() -> None:
    """
    Lists status of PostgreSQL

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.postgreSQLRunning:
            click.secho("PostgreSQL status: " + f" {click.style('[running]', fg='green')} "
                                                f"ip:{node.ip}, port:{constants.CITUS.COORDINATOR_PORT}", bold=False)
        else:
            click.secho("PostgreSQL status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)


def list_pgadmin() -> None:
    """
    Lists status of pgadmin

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.pgAdminRunning:
            click.secho("pgAdmin status: " + f" {click.style('[running]', fg='green')} "
                                             f"ip:{node.ip}, port:{constants.COMMANDS.PGADMIN_PORT}", bold=False)
        else:
            click.secho("pgAdmin status: " + f" {click.style('[stopped]', fg='red')} ip:{node.ip}", bold=False)


def list_node_exporter() -> None:
    """
    Lists status of node exporter

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.nodeExporterRunning:
            click.secho("Node exporter status: " + f" {click.style('[running]', fg='green')} "
                                                   f"ip:{node.ip}, port:{constants.COMMANDS.NODE_EXPORTER_PORT}",
                        bold=False)
        else:
            click.secho("Node exporter status: " + f" {click.style('[stopped],', fg='red')} ip:{node.ip}",
                        bold=False)


def list_prometheus() -> None:
    """
    Lists status of prometheus

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController

    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        node_status = ClusterController.get_node_status(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        if node_status.prometheusRunning:
            click.secho("Prometheus status: " + f" {click.style('[running]', fg='green')} "
                                                f"ip: {node.ip}, port:{constants.COMMANDS.PROMETHEUS_PORT}", bold=False)
        else:
            click.secho("Prometheus status: " + f" {click.style('[stopped]', fg='red')} ip: {node.ip}", bold=False)


def list_emulations(all: bool = False, stopped: bool = False, running: bool = True) -> None:
    """
    Lists emulations

    :param all: boolean flag whether all emulations should be listed
    :param stopped: boolean flag whether stopped emulations should be listed
    :param running: boolean flag whether running containers should be listed
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade

    click.secho("CSLE emulations:", fg="magenta", bold=True)
    emulations = MetastoreFacade.list_emulations()
    running_emulations, stopped_emulations = separate_running_and_stopped_emulations(emulations=emulations)
    if (all or running) or not stopped:
        for em in running_emulations:
            click.secho(em + f" {click.style('[running]', fg='green')}", bold=False)

    if (all or stopped) or not running:
        for em in stopped_emulations:
            click.secho(em + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_simulations() -> None:
    """
    Lists simulations

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade

    click.secho("CSLE simulations:", fg="magenta", bold=True)
    simulations = MetastoreFacade.list_simulations()
    for sim in simulations:
        click.secho(sim.name)


def list_emulation_executions() -> None:
    """
    Lists emulation executions

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade

    click.secho("CSLE emulation executions:", fg="magenta", bold=True)
    executions = MetastoreFacade.list_emulation_executions()
    for exec in executions:
        click.secho(f"IP ID: {exec.ip_first_octet}, emulation name: {exec.emulation_name}")


def list_networks() -> None:
    """
    Lists networks

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)

    click.secho("CSLE networks:", fg="magenta", bold=True)
    active_networks_names: List[str] = []
    for node in config.cluster_config.cluster_nodes:
        docker_networks_dto = ClusterController.list_all_docker_networks(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        active_networks_names = active_networks_names + list(docker_networks_dto.networks)
    executions = MetastoreFacade.list_emulation_executions()
    for exec in executions:
        em = exec.emulation_env_config
        for net in em.containers_config.networks:
            active = net.name in active_networks_names
            if active:
                print_network(net, active=active)


def list_cluster() -> None:
    """
    Lists the cluster configuration

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade

    click.secho("CSLE cluster:", fg="magenta", bold=True)
    config = MetastoreFacade.get_config(id=1)
    for node in config.cluster_config.cluster_nodes:
        click.secho(f"ip:{node.ip}, leader:{node.leader}, CPUs:{node.cpus}, GPUs:{node.gpus}, RAM (GB): {node.RAM}",
                    bold=False)


def get_network(name: str) -> Union[None, "ContainerNetwork"]:
    """
    Utility function for getting a given network

    :param name: the name of the network to get
    :return: None if the network was not found and otherwise returns the network
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    active_networks_names: List[str] = []
    for node in config.cluster_config.cluster_nodes:
        docker_networks_dto = ClusterController.list_all_docker_networks(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        active_networks_names = active_networks_names + list(docker_networks_dto.networks)
    emulations = MetastoreFacade.list_emulations()
    for em in emulations:
        for net in em.containers_config.networks:
            if net.name == name and net.name in active_networks_names:
                return net
    return None


def get_running_container(name: str) -> Union[None, DockerContainerDTO]:
    """
    Utility function for getting a running container with a given name

    :param name: the name of the container to get
    :return: None if the container was not found and otherwise returns the container
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    running_containers: List[DockerContainerDTO] = []
    for node in config.cluster_config.cluster_nodes:
        running_containers_dto = ClusterController.list_all_running_containers(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        running_containers_dtos = list(running_containers_dto.runningContainers)
        running_containers = running_containers + running_containers_dtos
    for c in running_containers:
        if name == c.name:
            return c
    return None


def get_stopped_container(name: str) -> Union[None, DockerContainerDTO]:
    """
    Utility function for stopping a given container

    :param name: the name of the container to stop
    :return: None if the container was not found and true otherwise
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    stopped_containers: List[DockerContainerDTO] = []
    for node in config.cluster_config.cluster_nodes:
        stopped_containers_dto = ClusterController.list_all_stopped_containers(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        stopped_containers_dtos = list(stopped_containers_dto.stoppedContainers)
        stopped_containers = stopped_containers + stopped_containers_dtos

    for c in stopped_containers:
        if name == c.name:
            return c
    return None


def list_all_containers() -> None:
    """
    Lists all containers, both running and stopped

    :return: None
    """
    click.secho("CSLE Docker containers:", fg="magenta", bold=True)
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    running_containers: List[DockerContainerDTO] = []
    stopped_containers: List[DockerContainerDTO] = []
    for node in config.cluster_config.cluster_nodes:
        stopped_containers_dto = ClusterController.list_all_stopped_containers(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        stopped_containers_dtos = list(stopped_containers_dto.stoppedContainers)
        running_containers_dto = ClusterController.list_all_running_containers(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        running_containers_dtos = list(running_containers_dto.runningContainers)
        stopped_containers = stopped_containers + stopped_containers_dtos
        running_containers = running_containers + running_containers_dtos
    for c in running_containers:
        print_running_container(c)
    for c in stopped_containers:
        print_stopped_container(c)


def list_running_containers() -> None:
    """
    Lists only running containers

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)

    click.secho("CSLE running Docker containers:", fg="magenta", bold=True)
    running_containers: List[DockerContainerDTO] = []
    for node in config.cluster_config.cluster_nodes:
        running_containers_dto = ClusterController.list_all_running_containers(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        running_containers_dtos = list(running_containers_dto.runningContainers)
        running_containers = running_containers + running_containers_dtos
    for c in running_containers:
        print_running_container(c)


def list_stopped_containers() -> None:
    """
    Lists stopped containers

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    click.secho("CSLE stopped Docker containers:", fg="magenta", bold=True)
    stopped_containers: List[DockerContainerDTO] = []
    for node in config.cluster_config.cluster_nodes:
        stopped_containers_dto = ClusterController.list_all_stopped_containers(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        stopped_containers_dtos = list(stopped_containers_dto.stoppedContainers)
        stopped_containers = stopped_containers + stopped_containers_dtos
    for c in stopped_containers:
        print_stopped_container(c)


def list_images() -> None:
    """
    Lists images

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)

    click.secho("CSLE Docker images:", fg="magenta", bold=True)
    images: List[ContainerImageDTO] = []
    for node in config.cluster_config.cluster_nodes:
        images_dto = ClusterController.list_all_container_images(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        images_dtos = list(images_dto.images)
        images = images + images_dtos
    for img in images:
        print_img(img)


def get_image(name: str) -> Union[None, ContainerImageDTO]:
    """
    Utility function for getting metadata of a docker image
    :param name: the name of the image to get
    :return: None or the image if it was found
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)
    images: List[ContainerImageDTO] = []
    for node in config.cluster_config.cluster_nodes:
        images_dto = ClusterController.list_all_container_images(
            ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
        images_dtos = list(images_dto.images)
        images = images + images_dtos

    for img in images:
        if img.repoTags == name:
            return img
    return None


def rm_name(name: str) -> None:
    """
    Removes a given container or image or network or emulation

    :param name: the name of the image, network, or container to remove
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)

    container_removed = False
    for node in config.cluster_config.cluster_nodes:
        outcome_dto = ClusterController.remove_container(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                                         container_name=name)
        if outcome_dto.outcome:
            container_removed = True
    if not container_removed:
        network_removed = False
        for node in config.cluster_config.cluster_nodes:
            outcome_dto = ClusterController.remove_docker_networks(
                ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, networks=[name])
            if outcome_dto.outcome:
                network_removed = True
        if not network_removed:
            image_removed = False
            for node in config.cluster_config.cluster_nodes:
                outcome_dto = ClusterController.remove_container_image(
                    ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, image_name=name)
                if outcome_dto.outcome:
                    image_removed = True
            if not image_removed:
                emulation_removed = remove_emulation(name=name)
                if not emulation_removed:
                    click.secho(f"name: {name} not recognized", fg="red", bold=True)


def clean_name(name: str, id: int = -1) -> None:
    """
    Cleans a given container or emulation

    :param name: the name of the container or emulation to clean
    :param id: the id of the container or emulation to clean
    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_cluster.cluster_manager.cluster_controller import ClusterController
    config = MetastoreFacade.get_config(id=1)

    container_stopped = False
    for node in config.cluster_config.cluster_nodes:
        outcome_dto = ClusterController.stop_container(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                                       container_name=name)
        if outcome_dto.outcome:
            container_stopped = True
    if container_stopped:
        for node in config.cluster_config.cluster_nodes:
            ClusterController.remove_container(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                               container_name=name)
    else:
        em = MetastoreFacade.get_emulation_by_name(name=name)
        if em is not None:
            if id == -1:
                clean_all_emulation_executions(emulation_env_config=em)
            else:
                clean_emulation_execution(emulation_env_config=em, execution_id=id)
        else:
            try:
                executions = MetastoreFacade.list_emulation_executions_by_id(id=int(name))
                for exec in executions:
                    for node in config.cluster_config.cluster_nodes:
                        ClusterController.clean_execution(ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT,
                                                          emulation=exec.emulation_name,
                                                          ip_first_octet=exec.ip_first_octet)
            except Exception:
                click.secho(f"name: {name} not recognized", fg="red", bold=True)


def remove_emulation(name: str) -> bool:
    """
    Utility function for removing (uninstalling) an emulation

    :param name: the name of the emulation to remove
    :return: True if the emulation was removed, false otherwise
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    click.secho(f"Removing emulation {name}", bold=False)
    emulations = MetastoreFacade.list_emulations()
    for emulation in emulations:
        if emulation.name == name:
            clean_all_emulation_executions(emulation)
            EmulationEnvController.uninstall_emulation(config=emulation)
            return True
    return False


def print_emulation_config(emulation_env_config: "EmulationEnvConfig") -> None:
    """
    Prints the configuration of a given emulation

    :param emulation_env_config: the configuration to print
    :return: None
    """
    import csle_common.constants.constants as constants

    click.secho(f"Emulation name: {emulation_env_config.name}", fg="yellow", bold=True)
    click.secho("Containers:", fg="yellow", bold=True)
    for c in emulation_env_config.containers_config.containers:
        click.secho(f"{c.name} {','.join(c.get_ips())}", bold=False)
    click.secho("Admin login:", fg="yellow", bold=True)
    click.secho(f"Username:{constants.CSLE_ADMIN.SSH_USER}", bold=False)
    click.secho(f"Password:{constants.CSLE_ADMIN.SSH_PW}", bold=False)
    click.secho("Vulnerabilities:", fg="yellow", bold=True)
    for vuln in emulation_env_config.vuln_config.node_vulnerability_configs:
        click.secho(f"{vuln.vuln_type} {vuln.ip}", bold=False)
        click.secho(f"{type(vuln.vuln_type)}", bold=False)
    click.secho("Resource constraints:", fg="yellow", bold=True)
    if emulation_env_config.resources_config is not None:
        for rc in emulation_env_config.resources_config.node_resources_configurations:
            network_bandwidth = ""
            for i, ip_net in enumerate(rc.ips_and_network_configs):
                ip, net = ip_net
                interface = net.interface
                bandwidth = net.rate_limit_mbit
                if i > 0:
                    network_bandwidth = network_bandwidth + ", "
                network_bandwidth = network_bandwidth + f"{interface} {bandwidth}Mbit/s"
            click.secho(f"{rc.container_name}: CPUs:{rc.num_cpus}, memory: {rc.available_memory_gb}GB, "
                        f"network:{network_bandwidth}", bold=False)
    click.secho("Flags:", fg="yellow", bold=True)
    for node_flag_cfg in emulation_env_config.flags_config.node_flag_configs:
        for flag in node_flag_cfg.flags:
            click.secho(f"{flag} {node_flag_cfg.ip}", bold=False)
    click.secho("Users:", fg="yellow", bold=True)
    for node_user_cfg in emulation_env_config.users_config.users_configs:
        for user in node_user_cfg.users:
            click.secho(f"{str(user)} {node_user_cfg.ip}", bold=False)
    click.secho("Kafka configuration:", fg="yellow", bold=True)
    click.secho(f"{emulation_env_config.kafka_config.container.name} "
                f"{','.join(emulation_env_config.kafka_config.container.get_ips())}", bold=False)
    click.secho(f"{emulation_env_config.kafka_config.resources.container_name}: "
                f"CPUs:{emulation_env_config.kafka_config.resources.num_cpus}, "
                f"memory: {emulation_env_config.kafka_config.resources.available_memory_gb}GB", bold=False)
    click.secho("ELK configuration:", fg="yellow", bold=True)
    click.secho(f"{emulation_env_config.elk_config.container.name} "
                f"{','.join(emulation_env_config.elk_config.container.get_ips())}", bold=False)
    click.secho(f"{emulation_env_config.elk_config.resources.container_name}: "
                f"CPUs:{emulation_env_config.elk_config.resources.num_cpus}, "
                f"memory: {emulation_env_config.elk_config.resources.available_memory_gb}GB", bold=False)


def print_simulation_config(simulation_config: SimulationEnvConfig) -> None:
    """
    Prints the configuration of a given emulation

    :param emulation_env_config: the configuration to print
    :return: None
    """

    click.secho(f"Simulation name: {simulation_config.name}", fg="yellow", bold=True)
    click.secho("Description:", fg="yellow", bold=True)
    click.secho(simulation_config.descr)
    click.secho(f"Gym env name: {simulation_config.gym_env_name}", fg="yellow", bold=True)
    click.secho(f"Num players: {len(simulation_config.players_config.player_configs)}", fg="yellow", bold=True)
    click.secho(f"Num states: {len(simulation_config.state_space_config.states)}", fg="yellow", bold=True)
    click.secho(f"Num observations: {len(simulation_config.observation_function_config.observation_tensor)}",
                fg="yellow", bold=True)


@click.command("help", help="lists all commands")
def help() -> None:
    """
    Prints list of all commands

    :return: None
    """
    click.secho(f"{click.style('init', fg='magenta')} Initializes CSLE and sets up mgmt accounts ",
                bold=False)
    click.secho(f"{click.style('ls', fg='magenta')} Lists information about CSLE ", bold=False)
    click.secho(f"{click.style('start', fg='magenta')} Starts en emulation, a job,"
                f" or a container ", bold=False)
    click.secho(f"{click.style('stop', fg='magenta')} Stops en entity, eg. emulation, a job,"
                f" or a container ", bold=False)
    click.secho(f"{click.style('rm', fg='magenta')} Removes a container, a network, an image, "
                f"all networks, all images, or all containers ", bold=False)
    click.secho(
        f"{click.style('install', fg='magenta')} Installs emulations and simulations in the metastore"
        f" and creates Docker images ",
        bold=False)
    click.secho(
        f"{click.style('uninstall', fg='magenta')} Uninstall emulations and simulations from the"
        f" metastore and removes Docker images ",
        bold=False)
    click.secho(
        f"{click.style('clean', fg='magenta')} Removes a container, a network, an image, all networks, "
        f"all images, all containers, all traces, or all statistics ",
        bold=False)
    click.secho(
        f"{click.style('shell', fg='magenta')} Command for opening a shell inside a running container ",
        bold=False)
    click.secho(
        f"{click.style('em', fg='magenta')} Extracts status information of a given emulation ",
        bold=False)
    click.secho(
        f"{click.style('datacollectionjob', fg='magenta')} Starts a data collection job with "
        f"the given id ",
        bold=False)
    click.secho(
        f"{click.style('systemidentificationjob', fg='magenta')} "
        f"Starts a system identification job with the given id ",
        bold=False)
    click.secho(
        f"{click.style('trainingjob', fg='magenta')} Starts a training job with the given id ",
        bold=False)
    click.secho(
        f"{click.style('clustermanager', fg='magenta')} Starts the clustermanager locally ",
        bold=False)
    click.secho(
        f"{click.style('statsmanager', fg='magenta')} Starts the statsmanager locally ",
        bold=False)
    click.secho(
        f"{click.style('start_traffic', fg='magenta')} "
        f"Starts the traffic and client population on a given emulation ",
        bold=False)
    click.secho(
        f"{click.style('stop_traffic', fg='magenta')} Stops the traffic and "
        f"client population on a given emulation ",
        bold=False)
    click.secho(
        f"{click.style('attacker', fg='magenta')} Opens an attacker shell in the given "
        f"emulation execution ",
        bold=False)
    click.secho("* For more information about each command, run csle [command] --help",
                fg="white", bold=False)


# Adds the commands to the group
commands.add_command(ls)
commands.add_command(rm)
commands.add_command(stop)
commands.add_command(start)
commands.add_command(shell)
commands.add_command(clean)
commands.add_command(start_traffic)
commands.add_command(stop_traffic)
commands.add_command(statsmanager)
commands.add_command(clustermanager)
commands.add_command(em)
commands.add_command(attacker)
commands.add_command(trainingjob)
commands.add_command(systemidentificationjob)
commands.add_command(install)
commands.add_command(uninstall)
commands.add_command(init)
commands.add_command(help)
