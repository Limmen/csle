"""
CSLE runner

To see options, run:
`csle --help`
"""
from typing import List, Tuple, Union
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.config import Config
import click

Config.set_config_parameters_from_config_file()


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
    ManagementUtil.create_default_management_admin_account()
    ManagementUtil.create_default_management_guest_account()


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
            # try:
            attacker_action_idx = int(raw_input)
            attacker_action = s.attacker_action_config.actions[attacker_action_idx]
            s = Attacker.attacker_transition(s=s, attacker_action=attacker_action)
            # except Exception as e:
            #     print("There was an error parsing the input, please enter an integer representing an attacker action")


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
    import gym
    import csle_common.constants.constants as constants

    click.secho("Registered OpenAI gym environments:", fg="magenta", bold=True)
    for env in gym.envs.registry.all():
        if constants.CSLE.NAME in env.id:
            click.secho(f"{env.id}", bold=False)


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
    from csle_common.controllers.container_controller import ContainerController
    from csle_common.controllers.traffic_controller import TrafficController
    from csle_common.controllers.snort_ids_controller import SnortIDSController
    from csle_common.controllers.kafka_controller import KafkaController
    from csle_common.controllers.host_controller import HostController

    emulation_env_config = MetastoreFacade.get_emulation_by_name(name=emulation)
    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(
        emulation_name=emulation_env_config.name)
    if emulation_env_config is not None:
        click.secho(f"Executions of: {emulation}", fg="magenta", bold=True)
        for exec in executions:
            click.secho(f"IP ID: {exec.ip_first_octet}, emulation name: {exec.emulation_name}")
        if clients:
            for exec in executions:
                clients_dto = TrafficController.get_num_active_clients(emulation_env_config=exec.emulation_env_config)
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
            for exec in executions:
                snort_ids_monitors_statuses = SnortIDSController.get_snort_idses_monitor_threads_statuses(
                    emulation_env_config=exec.emulation_env_config)
                for snort_ids_monitor_status in snort_ids_monitors_statuses:
                    click.secho(f"Snort IDS monitor status for execution {exec.ip_first_octet} of {emulation}",
                                fg="magenta", bold=True)
                    if snort_ids_monitor_status.running:
                        click.secho("Snort IDS monitor status: "
                                    + f" {click.style('[running]', fg='green')}", bold=False)
                    else:
                        click.secho("Snort IDS monitor status: "
                                    + f" {click.style('[stopped]', fg='red')}", bold=False)
        if kafka:
            for exec in executions:
                kafka_dto = KafkaController.get_kafka_status(emulation_env_config=exec.emulation_env_config)
                click.secho(f"Kafka manager status for execution {exec.ip_first_octet} of {emulation}",
                            fg="magenta", bold=True)
                if kafka_dto.running:
                    click.secho("Kafka broker status: " + f" {click.style('[running]', fg='green')}", bold=False)
                else:
                    click.secho("Kafka broker status: " + f" {click.style('[stopped]', fg='red')}", bold=False)
                click.secho("Topics:", bold=True)
                for topic in kafka_dto.topics:
                    click.secho(f"{topic}", bold=False)
        if stats:
            for exec in executions:
                stats_manager_dto = ContainerController.get_docker_stats_manager_status(
                    docker_stats_manager_config=exec.emulation_env_config.docker_stats_manager_config)
                click.secho(f"Docker stats manager status for execution {exec.ip_first_octet} of {emulation}",
                            fg="magenta", bold=True)
                click.secho(f"Number of active monitors: {stats_manager_dto.num_monitors}", bold=False)

        if host:
            for exec in executions:
                click.secho(f"Host manager statuses for execution {exec.ip_first_octet} of {emulation}",
                            fg="magenta", bold=True)
                host_manager_dtos = HostController.get_host_monitor_thread_status(emulation_env_config=exec.
                                                                                  emulation_env_config)
                for ip_hmd in host_manager_dtos:
                    hmd, ip = ip_hmd
                    if not hmd.running:
                        click.secho(f"Host manager on {ip} " + f" {click.style('[stopped]', fg='red')}", bold=False)
                    else:
                        click.secho(f"Host manager on {ip}: " + f" {click.style('[running]', fg='green')}", bold=False)
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


@click.option('--psf', default=None, type=float)
@click.option('--tsf', default=None, type=float)
@click.option('--nc', default=None, type=int)
@click.option('--t', default=None, type=int)
@click.option('--lamb', default=None, type=int)
@click.option('--mu', default=None, type=float)
@click.argument('id', default=-1, type=int)
@click.argument('emulation', default="", type=str, shell_complete=start_traffic_shell_complete)
@click.command("start_traffic", help="emulation-name execution-id")
def start_traffic(emulation: str, id: int, mu: float, lamb: float, t: int,
                  nc: int, tsf: float, psf: float) -> None:
    """
    Starts the traffic and client population on a given emulation

    :param emulation: the emulation to start the traffic of
    :param id: the id of the execution
    :param mu: the mu parameter of the service time of the client arrivals
    :param lamb: the lambda parameter of the client arrival process
    :param t: time-step length to measure the arrival process
    :param nc: number of commands per client
    :param psf: the period scaling factor for non-stationary Poisson processes
    :param tsf: the time scaling factor for non-stationary Poisson processes
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.emulation_env_controller import EmulationEnvController
    execution = MetastoreFacade.get_emulation_execution(ip_first_octet=id, emulation_name=emulation)
    if execution is not None:
        emulation_env_config = execution.emulation_env_config
        if mu is not None:
            emulation_env_config.traffic_config.client_population_config.mu = mu
        if lamb is not None:
            emulation_env_config.traffic_config.client_population_config.lamb = lamb
        if t is not None:
            emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds = t
        if nc is not None:
            emulation_env_config.traffic_config.client_population_config.num_commands = nc
        if tsf is not None:
            emulation_env_config.traffic_config.client_population_config.time_scaling_factor = tsf
        if psf is not None:
            emulation_env_config.traffic_config.client_population_config.period_scaling_factor = psf
        click.secho(f"Starting client population with "
                    f"config:{emulation_env_config.traffic_config.client_population_config}")
        EmulationEnvController.start_custom_traffic(emulation_env_config=emulation_env_config)
    else:
        click.secho(f"execution {id} of emulation {emulation} not recognized", fg="red", bold=True)


def stop_traffic_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Completion suggestiosn for the traffic command

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
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    emulation_execution = MetastoreFacade.get_emulation_execution(ip_first_octet=id, emulation_name=emulation)
    if emulation_execution is not None:
        EmulationEnvController.stop_custom_traffic(emulation_env_config=emulation_execution.emulation_env_config)
    else:
        click.secho(f"execution {id} of emulation {emulation} not recognized", fg="red", bold=True)


def shell_shell_complete(ctx, param, incomplete) -> List[str]:
    """
    Shell completion for the shell command

    :param ctx: the command context
    :param param: the command parameter
    :param incomplete: the command incomplete flag
    :return: a list of completion suggestions
    """
    from csle_common.controllers.container_controller import ContainerController
    running_containers = ContainerController.list_all_running_containers()
    stopped_containers = ContainerController.list_all_stopped_containers()
    containers = running_containers + stopped_containers
    containers = list(map(lambda x: x[0], containers))
    return containers


@click.argument('container', default="", shell_complete=shell_shell_complete)
@click.command("shell", help="container-name")
def shell(container: str) -> None:
    """
    Command for opening a shell inside a running container

    :param container: the name of the container
    :return: None
    """
    from csle_common.controllers.container_controller import ContainerController

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
        click.secho(f"Container: {container} not found among running containers", fg="red", bold=False)


def run_emulation(emulation_env_config: "EmulationEnvConfig", no_traffic: bool, no_clients: bool) -> None:
    """
    Runs an emulation with the given config

    :param emulation_env_config: the config of the emulation to run
    :param no_traffic: a boolean parameter that is True if the traffic generators should be skipped
    :param no_clients: a boolean parameter that is True if the client_population should be skipped
    :return: None
    """
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    click.secho(f"Starting emulation {emulation_env_config.name}", bold=False)
    emulation_execution = EmulationEnvController.create_execution(emulation_env_config=emulation_env_config)
    EmulationEnvController.run_containers(emulation_execution=emulation_execution)
    EmulationEnvController.apply_emulation_env_config(emulation_execution=emulation_execution,
                                                      no_traffic=no_traffic, no_clients=no_clients)


def separate_running_and_stopped_emulations(emulations: List["EmulationEnvConfig"]) -> Tuple[List[str], List[str]]:
    """
    Partitions the set of emulations into a set of running emulations and a set of stopped emulations

    :param emulations: the list of emulations
    :return: running_emulations, stopped_emulations
    """
    from csle_common.controllers.container_controller import ContainerController

    rc_emulations = ContainerController.list_running_emulations()
    stopped_emulations = []
    running_emulations = []
    for em in emulations:
        if em.name in rc_emulations:
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
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    click.secho(f"Stopping all executions of emulation {emulation_env_config.name}", bold=False)
    EmulationEnvController.stop_all_executions_of_emulation(emulation_env_config=emulation_env_config)


def stop_emulation_execution(emulation_env_config: "EmulationEnvConfig", execution_id: int) -> None:
    """
    Stops the emulation with the given configuration

    :param emulation_env_config: the configuration of the emulation to stop
    :param execution_id: id of the execution to stop
    :return: None
    """
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    click.secho(f"Stopping execution {execution_id} of emulation {emulation_env_config.name}", bold=False)
    EmulationEnvController.stop_execution_of_emulation(emulation_env_config=emulation_env_config,
                                                       execution_id=execution_id)


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
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    click.secho("Stopping and cleaning all emulation executions", bold=False)
    EmulationEnvController.clean_all_executions()


def stop_emulation_executions() -> None:
    """
    Stops all emulation executions

    :return: None
    """
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    click.secho("Stopping all emulation executions", bold=False)
    EmulationEnvController.stop_all_executions()


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
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    click.secho(f"Cleaning emulation {emulation_env_config.name}", bold=False)
    EmulationEnvController.clean_all_emulation_executions(emulation_env_config=emulation_env_config)


def clean_emulation_execution(emulation_env_config: "EmulationEnvConfig", execution_id: int) -> None:
    """
    Cleans an execution of an emulation

    :param execution_id: the id of the execution to clean
    :param emulation_env_config: the configuration of the emulation
    :return: None
    """
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    click.secho(f"Cleaning execution {execution_id} of emulation {emulation_env_config.name}", bold=False)
    EmulationEnvController.clean_emulation_execution(emulation_env_config, execution_id)


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
    emulations = running_emulations
    running_containers = ContainerController.list_all_running_containers()
    containers = running_containers
    containers = list(map(lambda x: x[0], containers))
    return ["prometheus", "node_exporter", "cadvisor", "grafana", "managementsystem",
            "statsmanager", "all", "emulation_executions"] + emulations + containers


@click.argument('id', default=-1)
@click.argument('entity', default="", shell_complete=stop_shell_complete)
@click.command("stop", help="prometheus | node_exporter | cadvisor | grafana | managementsystem | container-name | "
                            "emulation-name | statsmanager | emulation_executions | all")
def stop(entity: str, id: int = -1) -> None:
    """
    Stops an entity

    :param entity: the name of the container to stop or "all"
    :param id: id when stopping a specific emulation execution
    :return: None
    """
    from csle_common.controllers.container_controller import ContainerController
    from csle_common.controllers.management_system_controller import ManagementSystemController
    from csle_common.metastore.metastore_facade import MetastoreFacade

    if entity == "all":
        ContainerController.stop_all_running_containers()
        for emulation in MetastoreFacade.list_emulations():
            stop_all_executions_of_emulation(emulation_env_config=emulation)
    elif entity == "node_exporter":
        ManagementSystemController.stop_node_exporter()
    elif entity == "prometheus":
        ManagementSystemController.stop_prometheus()
    elif entity == "cadvisor":
        ManagementSystemController.stop_cadvisor()
    elif entity == "grafana":
        ManagementSystemController.stop_grafana()
    elif entity == "managementsystem":
        ManagementSystemController.stop_management_system()
    elif entity == "statsmanager":
        ManagementSystemController.stop_docker_stats_manager()
    elif entity == "emulation_executions":
        stop_emulation_executions()
    else:
        container_stopped = ContainerController.stop_container(name=entity)
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
    containers = stopped_containers
    containers = list(map(lambda x: x[0], containers))
    image_names = ContainerController.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
    return (["prometheus", "node_exporter", "grafana", "cadvisor", "managementsystem", "all",
             "statsmanager", "training_job", "system_id_job", "--id", "--no_traffic"]
            + emulations + containers + image_names)


@click.argument('max_workers', default=10, type=int, shell_complete=start_shell_complete)
@click.argument('log_file', default="docker_statsmanager.log", type=str, shell_complete=start_shell_complete)
@click.argument('log_dir', default="/var/log/csle", type=str, shell_complete=start_shell_complete)
@click.argument('port', default=50046, type=int, shell_complete=start_shell_complete)
@click.option('--id', default=None, type=int)
@click.option('--no_clients', is_flag=True, help='skip starting the client population')
@click.option('--no_traffic', is_flag=True, help='skip starting the traffic generators')
@click.option('--no_network', is_flag=True, help='skip creating network when starting individual container')
@click.argument('name', default="", type=str)
@click.argument('entity', default="", type=str, shell_complete=start_shell_complete)
@click.command("start", help="prometheus | node_exporter | grafana | cadvisor | managementsystem | "
                             "container-name | emulation-name | all | statsmanager | training_job "
                             "| system_id_job ")
def start(entity: str, no_traffic: bool, name: str, id: int, no_clients: bool, no_network: bool, port: int,
          log_file: str, log_dir: str, max_workers: int) -> None:
    """
    Starts an entity, e.g. a container or the management system

    :param entity: the container or emulation to start or "all"
    :param name: extra parameter for running a Docker image
    :param port: extra parameter for starting the docker stats manager
    :param log_file: extra parameter for starting the docker stats manager
    :param log_dir: extra parameter for starting the docker stats manager
    :param max_workers: extra parameter for starting the docker stats manager
    :param no_traffic: a boolean parameter that is True if the traffic generators should be skipped
    :param no_clients: a boolean parameter that is True if the client population should be skipped
    :param no_network: a boolean parameter that is True if the network should be skipped when creating a container
    :param id: (optional) an id parameter to identify the entity to start
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    from csle_common.controllers.management_system_controller import ManagementSystemController
    from csle_agents.job_controllers.training_job_manager import TrainingJobManager
    from csle_system_identification.job_controllers.data_collection_job_manager import DataCollectionJobManager

    if entity == "all":
        ContainerController.start_all_stopped_containers()
    elif entity == "statsmanager":
        start_docker_stats_manager(port=port, log_file=log_file, log_dir=log_dir, max_workers=max_workers)
    elif entity == "node_exporter":
        ManagementSystemController.start_node_exporter()
    elif entity == "prometheus":
        ManagementSystemController.start_prometheus()
    elif entity == "cadvisor":
        ManagementSystemController.start_cadvisor()
    elif entity == "grafana":
        ManagementSystemController.start_grafana()
    elif entity == "training_job":
        training_job = MetastoreFacade.get_training_job_config(id=id)
        TrainingJobManager.start_training_job_in_background(training_job=training_job)
    elif entity == "system_id_job":
        system_id_job = MetastoreFacade.get_data_collection_job_config(id=id)
        DataCollectionJobManager.start_data_collection_job_in_background(
            data_collection_job=system_id_job)
    elif entity == "managementsystem":
        ManagementSystemController.start_management_system()
    else:
        container_started = ContainerController.start_container(name=entity)
        if not container_started:
            emulation_env_config = MetastoreFacade.get_emulation_by_name(name=entity)
            if emulation_env_config is not None:
                run_emulation(emulation_env_config, no_traffic=no_traffic, no_clients=no_clients)
                emulation_started = True
            else:
                emulation_started = False
            if not emulation_started:
                image_started = run_image(image=entity, name=name, create_network=(not no_network))
                if not image_started:
                    click.secho(f"name: {entity} not recognized", fg="red", bold=True)


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
    containers = running_containers + stopped_containers
    containers = list(map(lambda x: x[0], containers))
    image_names = ContainerController.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
    return (["network-name", "container-name", "image-name", "networks", "images", "containers"] +
            emulations + containers + image_names)


@click.argument('entity', default="", shell_complete=rm_shell_complete)
@click.command("rm", help="network-name | container-name | image-name | networks | images | containers")
def rm(entity: str) -> None:
    """
    Removes a container, a network, an image, all networks, all images, or all containers

    :param entity: the container(s), network(s), or images(s) to remove
    :return: None
    """
    from csle_common.controllers.container_controller import ContainerController

    if entity == "containers":
        ContainerController.rm_all_stopped_containers()
    elif entity == "images":
        ContainerController.rm_all_images()
    elif entity == "networks":
        ContainerController.rm_all_networks()
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
    running_containers = ContainerController.list_all_running_containers()
    stopped_containers = ContainerController.list_all_stopped_containers()
    containers = running_containers + stopped_containers
    containers = list(map(lambda x: x[0], containers))
    return ["all", "containers", "emulations", "emulation_traces", "simulation_traces", "emulation_statistics",
            "name", "emulation_executions"] + emulations + containers


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
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController

    if entity == "all":
        ContainerController.stop_all_running_containers()
        ContainerController.rm_all_stopped_containers()
        for emulation in MetastoreFacade.list_emulations():
            clean_all_emulation_executions(emulation_env_config=emulation)
    elif entity == "containers":
        ContainerController.stop_all_running_containers()
        ContainerController.rm_all_stopped_containers()
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
        clean_name(name=entity)


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
    image_names = ContainerController.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
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
    image_names = ContainerController.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
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
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    simulations = list(map(lambda x: x.name, MetastoreFacade.list_simulations()))
    running_containers = ContainerController.list_all_running_containers()
    stopped_containers = ContainerController.list_all_stopped_containers()
    containers = running_containers + stopped_containers
    containers = list(map(lambda x: x[0], containers))
    image_names = ContainerController.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
    active_networks_names = ContainerController.list_all_networks()
    return (["containers", "networks", "images", "emulations", "all", "environments", "prometheus", "node_exporter",
            "cadvisor", "managementsystem", "statsmanager", "--all", "--running", "--stopped"] + emulations
            + containers + image_names + active_networks_names + simulations)


@click.command("ls", help="containers | networks | images | emulations | all | environments | prometheus "
                          "| node_exporter | cadvisor | statsmanager | managementsystem | "
                          "simulations | emulation_executions")
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
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController

    if entity == "all":
        list_all(all=all, running=running, stopped=stopped)
    elif entity == "networks":
        list_networks()
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
    elif entity == "grafana":
        list_grafana()
    elif entity == "managementsystem":
        list_management_system()
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
                        active_networks_names = ContainerController.list_all_networks()
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


def print_running_container(container) -> None:
    """
    Utility function for printing information about a running container

    :param container: the container to print
    :return: None
    """
    click.secho(container[0] + f" image:{container[1]}, ip: {container[2]} {click.style('[running]', fg='green')}",
                bold=False)


def print_stopped_container(container) -> None:
    """
    Utiltiy function for printing information about a stopped container

    :param container: the stopped container to print
    :return: None
    """
    click.secho(container[0] + f" image:{container[1]}, ip: {container[2]} {click.style('[stopped]', fg='red')}",
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


def print_img(img: Tuple[str, str, str, str, str]) -> None:
    """
    Utility function for printing a given Docker image

    :param img: the image to print
    :return: None
    """
    click.secho(f"name:{img[0]}, size:{img[4]}B", bold=False)


def list_all(all: bool = False, running: bool = True, stopped: bool = False) -> None:
    """
    Lists all containers, images, networks, and emulations

    :param all: boolean flag whether all containers/emulations should be listed
    :param running: boolean flag whether running containers/emulations should be listed (default)
    :param stopped: boolean flag whether stopped containers/emulations should be listed
    :return: None
    """
    list_networks()
    list_all_containers()
    list_images()
    list_emulations(all=all, stopped=stopped, running=running)
    list_emulation_executions()
    list_simulations()
    list_csle_gym_envs()
    click.secho("CSLE management system:", fg="magenta", bold=True)
    list_prometheus()
    list_node_exporter()
    list_cadvisor()
    list_grafana()
    list_statsmanager()
    list_management_system()


def list_statsmanager() -> None:
    """
    List status of the docker host manager

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    from csle_common.controllers.management_system_controller import ManagementSystemController

    if ManagementSystemController.is_statsmanager_running():
        emulations = MetastoreFacade.list_emulations()
        running_emulations, stopped_emulations = separate_running_and_stopped_emulations(emulations=emulations)
        docker_stats_monitor_status = None
        for em in emulations:
            if em.name in running_emulations:
                docker_stats_monitor_status = ContainerController.get_docker_stats_manager_status(
                    docker_stats_manager_config=em.docker_stats_manager_config)
                break
        active_monitor_threads = 0
        active_emulations = []
        if docker_stats_monitor_status is not None:
            active_monitor_threads = docker_stats_monitor_status.num_monitors
            active_emulations = docker_stats_monitor_status.emulations
        click.secho("Docker statsmanager status: " + f" {click.style('[running], ', fg='green')} "
                                                     f"port:{50046}, num active monitor threads: "
                                                     f"{active_monitor_threads}, "
                                                     f"active emulations: {','.join(active_emulations)}", bold=False)
    else:
        click.secho("Docker statsmanager status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_grafana() -> None:
    """
    List status of grafana

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.management_system_controller import ManagementSystemController

    if ManagementSystemController.is_grafana_running():
        click.secho("Grafana status: " + f" {click.style('[running]', fg='green')} "
                                         f"port:{constants.COMMANDS.GRAFANA_PORT}", bold=False)
    else:
        click.secho("Grafana status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_management_system() -> None:
    """
    List status of the management system

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.management_system_controller import ManagementSystemController

    if ManagementSystemController.is_management_system_running():
        click.secho("Management system status: " + f" {click.style('[running]', fg='green')} "
                                                   f"port:{constants.COMMANDS.MANAGEMENT_SYSTEM_PORT}", bold=False)
    else:
        click.secho("Management system status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_cadvisor() -> None:
    """
    Lists status of cadvisor

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.management_system_controller import ManagementSystemController

    if ManagementSystemController.is_cadvisor_running():
        click.secho("Cadvisor status: " + f" {click.style('[running]', fg='green')} "
                                          f"port:{constants.COMMANDS.CADVISOR_PORT}", bold=False)
    else:
        click.secho("Cadvisor status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_node_exporter() -> None:
    """
    Lists status of node exporter

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.management_system_controller import ManagementSystemController

    if ManagementSystemController.is_node_exporter_running():
        click.secho("Node exporter status: " + f" {click.style('[running]', fg='green')} "
                                               f"port:{constants.COMMANDS.NODE_EXPORTER_PORT}", bold=False)
    else:
        click.secho("Node exporter status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_prometheus() -> None:
    """
    Lists status of prometheus

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.management_system_controller import ManagementSystemController

    if ManagementSystemController.is_prometheus_running():
        click.secho("Prometheus status: " + f" {click.style('[running]', fg='green')} "
                                            f"port:{constants.COMMANDS.PROMETHEUS_PORT}", bold=False)
    else:
        click.secho("Prometheus status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


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
    if all or not stopped:
        for em in running_emulations:
            click.secho(em + f" {click.style('[running]', fg='green')}", bold=False)
    if all or stopped:
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
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController

    click.secho("CSLE networks:", fg="magenta", bold=True)
    active_networks_names = ContainerController.list_all_networks()
    executions = MetastoreFacade.list_emulation_executions()
    for exec in executions:
        em = exec.emulation_env_config
        for net in em.containers_config.networks:
            active = net.name in active_networks_names
            if active:
                print_network(net, active=active)


def get_network(name: str) -> Union[None, "ContainerNetwork"]:
    """
    Utility function for getting a given network

    :param name: the name of the network to get
    :return: None if the network was not found and otherwise returns the network
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController

    active_networks_names = ContainerController.list_all_networks()
    emulations = MetastoreFacade.list_emulations()
    for em in emulations:
        for net in em.containers_config.networks:
            if net.name == name and net.name in active_networks_names:
                return net
    return None


def get_running_container(name: str) -> Union[None, Tuple[str, str, str]]:
    """
    Utility function for getting a running container with a given name

    :param name: the name of the container to get
    :return: None if the container was not found and otherwise returns the container
    """
    from csle_common.controllers.container_controller import ContainerController

    running_containers = ContainerController.list_all_running_containers()
    for c in running_containers:
        if name == c[0]:
            return c
    return None


def get_stopped_container(name: str) -> Union[None, Tuple[str, str, str]]:
    """
    Utility function for stopping a given container

    :param name: the name of the container to stop
    :return: None if the container was not found and true otherwise
    """
    from csle_common.controllers.container_controller import ContainerController

    stopped_containers = ContainerController.list_all_stopped_containers()
    for c in stopped_containers:
        if name == c[0]:
            return c
    return None


def list_all_containers() -> None:
    """
    Lists all containers, both running and stopped

    :return: None
    """
    from csle_common.controllers.container_controller import ContainerController

    click.secho("CSLE Docker containers:", fg="magenta", bold=True)
    running_containers = ContainerController.list_all_running_containers()
    stopped_containers = ContainerController.list_all_stopped_containers()
    containers = running_containers + stopped_containers
    for c in containers:
        if c in running_containers:
            print_running_container(c)
        else:
            print_stopped_container(c)


def list_running_containers() -> None:
    """
    Lists only running containers

    :return: None
    """
    from csle_common.controllers.container_controller import ContainerController

    click.secho("CSLE running Docker containers:", fg="magenta", bold=True)
    containers = ContainerController.list_all_running_containers()
    for c in containers:
        print_running_container(c)


def list_stopped_containers() -> None:
    """
    Lists stopped containers

    :return: None
    """
    from csle_common.controllers.container_controller import ContainerController

    click.secho("CSLE stopped Docker containers:", fg="magenta", bold=True)
    containers = ContainerController.list_all_stopped_containers()
    for c in containers:
        print_stopped_container(c)


def list_images() -> None:
    """
    Lists images

    :return: None
    """
    from csle_common.controllers.container_controller import ContainerController

    click.secho("CSLE Docker images:", fg="magenta", bold=True)
    image_names = ContainerController.list_all_images()
    for img in image_names:
        print_img(img)


def get_image(name: str) -> Union[None, Tuple[str, str, str, str, str]]:
    """
    Utility function for getting metadata of a docker image
    :param name: the name of the image to get
    :return: None or the image if it was found
    """
    from csle_common.controllers.container_controller import ContainerController

    image_names = ContainerController.list_all_images()
    for img in image_names:
        if img == name:
            return img
    return None


def rm_name(name: str) -> None:
    """
    Removes a given container or image or network or emulation

    :param name: the name of the image, network, or container to remove
    :return: None
    """
    from csle_common.controllers.container_controller import ContainerController

    container_removed = ContainerController.rm_container(name)
    if not container_removed:
        network_removed = ContainerController.rm_network(name)
        if not network_removed:
            image_removed = ContainerController.rm_image(name)
            if not image_removed:
                emulation_removed = remove_emulation(name=name)
                if not emulation_removed:
                    click.secho(f"name: {name} not recognized", fg="red", bold=True)


def clean_name(name: str) -> None:
    """
    Cleans a given container or emulation

    :param name: the name of the container or emulation to clean
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_controller import ContainerController
    from csle_common.controllers.emulation_env_controller import EmulationEnvController

    container_stopped = ContainerController.stop_container(name=name)
    if container_stopped:
        ContainerController.rm_container(container_name=name)
    else:
        em = MetastoreFacade.get_emulation_by_name(name=name)
        if em is not None:
            clean_all_emulation_executions(emulation_env_config=em)
        else:
            try:
                executions = MetastoreFacade.list_emulation_executions_by_id(id=int(name))
                for exec in executions:
                    EmulationEnvController.clean_emulation_execution(
                        emulation_env_config=exec.emulation_env_config, execution_id=exec.ip_first_octet)
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
    for flag in emulation_env_config.flags_config.node_flag_configs:
        click.secho(f"{flag.flags[0][0]} {flag.ip}", bold=False)
    click.secho("Users:", fg="yellow", bold=True)
    for user in emulation_env_config.users_config.users_configs:
        users = ",".join(list(map(lambda x: x[0], user.users)))
        click.secho(f"{users} {user.ip}", bold=False)
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


# Set config parameters


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
commands.add_command(em)
commands.add_command(attacker)
commands.add_command(trainingjob)
commands.add_command(systemidentificationjob)
commands.add_command(install)
commands.add_command(uninstall)
commands.add_command(init)
