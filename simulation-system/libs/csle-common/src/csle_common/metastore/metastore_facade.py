from typing import List, Union, Any, Tuple
import psycopg
import json
import time
import zlib
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.logging.log import Logger
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.dao.system_identification.empirical_system_model import EmpiricalSystemModel
from csle_common.dao.system_identification.mcmc_system_model import MCMCSystemModel
from csle_common.dao.system_identification.gp_system_model import GPSystemModel
from csle_common.dao.encoding.np_encoder import NpEncoder
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_common.dao.training.dqn_policy import DQNPolicy
from csle_common.dao.training.fnn_with_softmax_policy import FNNWithSoftmaxPolicy
from csle_common.dao.training.vector_policy import VectorPolicy
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.management.management_user import ManagementUser
from csle_common.dao.management.session_token import SessionToken
from csle_common.dao.datasets.traces_dataset import TracesDataset
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.dao.emulation_config.config import Config
from csle_common.util.general_util import GeneralUtil


class MetastoreFacade:
    """
    Facade for the metastore, contains methods for querying the metastore
    """

    @staticmethod
    def list_emulations() -> List[EmulationEnvConfig]:
        """
        :return: A list of emulations in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_emulation_record_to_dto(x), records))

    @staticmethod
    def list_emulations_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of emulation ids and names in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,name FROM {constants.METADATA_STORE.EMULATIONS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def get_emulation_by_name(name: str) -> Union[None, EmulationEnvConfig]:
        """
        Function for extracting the metadata of an emulation with a given name

        :param name: the name of the emulation
        :return: The emulation config or None if the emulation was not found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s", (name,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_record_to_dto(emulation_record=record)
                return record

    @staticmethod
    def get_emulation(id: int) -> Union[None, EmulationEnvConfig]:
        """
        Function for extracting the metadata of an emulation with a id

        :param id: the id of the emulation
        :return: The emulation config or None if the emulation was not found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_record_to_dto(emulation_record=record)
                return record

    @staticmethod
    def list_simulations() -> List[SimulationEnvConfig]:
        """
        :return: A list of simulations in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATIONS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_simulation_record_to_dto(x), records))

    @staticmethod
    def list_simulation_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of simulation ids and names in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,name FROM {constants.METADATA_STORE.SIMULATIONS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def get_simulation_by_name(name: str) -> Union[None, SimulationEnvConfig]:
        """
        Function for extracting the metadata of a simulation with a given name

        :param name: the name of the simulation
        :return: The simulation config or None if the simulation was not found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATIONS_TABLE} WHERE name = %s", (name,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_simulation_record_to_dto(simulation_record=record)
                return record

    @staticmethod
    def get_simulation(id: int) -> Union[None, SimulationEnvConfig]:
        """
        Function for extracting the metadata of a simulation with a given id

        :param id: the id of the simulation
        :return: The simulation config or None if the simulation was not found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATIONS_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_simulation_record_to_dto(simulation_record=record)
                return record

    @staticmethod
    def _convert_emulation_record_to_dto(emulation_record) -> EmulationEnvConfig:
        """
        Converts an emulation record fetched from the metastore into a DTO

        :param emulation_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_config_json_str = json.dumps(emulation_record[2], indent=4, sort_keys=True, cls=NpEncoder)
        emulation_env_config: EmulationEnvConfig = EmulationEnvConfig.from_dict(json.loads(emulation_config_json_str))
        emulation_env_config.id = emulation_record[0]
        return emulation_env_config

    @staticmethod
    def _convert_simulation_record_to_dto(simulation_record) -> SimulationEnvConfig:
        """
        Converts an simulation record fetched from the metastore into a DTO

        :param simulation_record: the record to convert
        :return: the DTO representing the record
        """
        simulation_config_json_str = json.dumps(simulation_record[2], indent=4, sort_keys=True, cls=NpEncoder)
        simulation_env_config: SimulationEnvConfig = SimulationEnvConfig.from_dict(
            json.loads(simulation_config_json_str))
        simulation_env_config.id = simulation_record[0]
        return simulation_env_config

    @staticmethod
    def _convert_emulation_trace_record_to_dto(emulation_trace_record) -> EmulationTrace:
        """
        Converts an emulation trace record fetched from the metastore into a DTO

        :param emulation_trace_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_trace_json_str = zlib.decompress(emulation_trace_record[2]).decode()
        emulation_trace: EmulationTrace = EmulationTrace.from_dict(json.loads(emulation_trace_json_str))
        emulation_trace.id = emulation_trace_record[0]
        return emulation_trace

    @staticmethod
    def _convert_emulation_simulation_trace_record_to_dto(emulation_simulation_trace_record) \
            -> EmulationSimulationTrace:
        """
        Converts an emulation-simulkation trace record fetched from the metastore into a DTO

        :param emulation_simulation_trace_record: the record to convert
        :return: the DTO representing the record
        """
        id = emulation_simulation_trace_record[0]
        emulation_trace_id = emulation_simulation_trace_record[1]
        simulation_trace_id = emulation_simulation_trace_record[2]
        emulation_trace = MetastoreFacade.get_emulation_trace(id=emulation_trace_id)
        simulation_trace = MetastoreFacade.get_simulation_trace(id=simulation_trace_id)
        if emulation_trace is None:
            raise ValueError(f"Could not find an emulation trace with id: {emulation_trace_id}")
        if simulation_trace is None:
            raise ValueError(f"Could not find a simulation trace with id: {simulation_trace_id}")
        emulation_simulation_trace = EmulationSimulationTrace(emulation_trace=emulation_trace,
                                                              simulation_trace=simulation_trace)
        emulation_simulation_trace.id = id
        return emulation_simulation_trace

    @staticmethod
    def _convert_simulation_trace_record_to_dto(simulation_trace_record) -> SimulationTrace:
        """
        Converts an emulation trace record fetched from the metastore into a DTO

        :param simulation_trace_record: the record to convert
        :return: the DTO representing the record
        """
        simulation_trace_json_str = json.dumps(simulation_trace_record[2], indent=4, sort_keys=True, cls=NpEncoder)
        simulation_trace: SimulationTrace = SimulationTrace.from_dict(json.loads(simulation_trace_json_str))
        simulation_trace.id = simulation_trace_record[0]
        return simulation_trace

    @staticmethod
    def _convert_emulation_statistics_record_to_dto(emulation_statistics_record) -> EmulationStatistics:
        """
        Converts an emulation statistics record fetched from the metastore into a DTO

        :param emulation_statistics_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_statistics_json_str = zlib.decompress(emulation_statistics_record[2]).decode()
        emulation_statistics: EmulationStatistics = EmulationStatistics.from_dict(
            json.loads(emulation_statistics_json_str,
                       object_hook=lambda d: {int(k.split(".", 1)[0]) if k.split(".", 1)[0].lstrip('-').isdigit()
                                              else k: v for k, v in d.items()}))
        emulation_statistics.id = emulation_statistics_record[0]
        return emulation_statistics

    @staticmethod
    def _convert_emulation_image_record_to_tuple(emulation_image_record) -> Tuple[str, bytes]:
        """
        Converts an emulation image record fetched from the metastore into bytes

        :param emulation_image_record: the record to convert
        :return: a tuple (emulation name, image bytes)
        """
        emulation_name = emulation_image_record[1]
        image_bytes = emulation_image_record[2]
        return emulation_name, image_bytes

    @staticmethod
    def _convert_simulation_image_record_to_tuple(simulation_image_record) -> Tuple[str, bytes]:
        """
        Converts a simulation image record fetched from the metastore into bytes

        :param simulation_image_record: the record to convert
        :return: a tuple (emulation name, image bytes)
        """
        emulation_name = simulation_image_record[1]
        image_bytes = simulation_image_record[2]
        return emulation_name, image_bytes

    @staticmethod
    def install_emulation(config: EmulationEnvConfig) -> Union[int, None]:
        """
        Installs the emulation configuration in the metastore

        :param config: the config to install
        :return: id of the created row or None if the installation failed
        """
        Logger.__call__().get_logger().debug(f"Installing emulation:{config.name} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    # Need to manually set the ID since CITUS does not handle serial columns
                    # on distributed tables properly
                    id = GeneralUtil.get_latest_table_id(cur=cur,
                                                         table_name=constants.METADATA_STORE.EMULATIONS_TABLE)
                    config_json_str = json.dumps(config.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATIONS_TABLE} (id, name, config) "
                                f"VALUES (%s, %s, %s) RETURNING id", (id, config.name, config_json_str))
                    record = cur.fetchone()
                    id_of_new_row = None
                    if record is not None:
                        id_of_new_row = int(record[0])
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Emulation {config.name} installed successfully")
                    return id_of_new_row
                except psycopg.errors.UniqueViolation as e:
                    Logger.__call__().get_logger().debug(f"Emulation {config.name} is already installed "
                                                         f"{str(e), repr(e)}")
                    return None

    @staticmethod
    def uninstall_emulation(config: EmulationEnvConfig) -> None:
        """
        Uninstalls the emulation configuration in the metastore

        :param config: the config to uninstall
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Uninstalling emulation:{config.name} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s", (config.name,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation {config.name} uninstalled successfully")
        return None

    @staticmethod
    def install_simulation(config: SimulationEnvConfig) -> Union[None, int]:
        """
        Installs the simulation configuration in the metastore

        :param config: the config to install
        :return: id of the created row
        """
        Logger.__call__().get_logger().debug(f"Installing simulation:{config.name} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    # Need to manually set the ID since CITUS does not handle serial columns
                    # on distributed tables properly
                    id = GeneralUtil.get_latest_table_id(cur=cur,
                                                         table_name=constants.METADATA_STORE.SIMULATIONS_TABLE)
                    config_json_str = config.to_json_str()
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.SIMULATIONS_TABLE} "
                                f"(id, name, config) "
                                f"VALUES (%s, %s, %s) RETURNING id", (id, config.name, config_json_str))
                    record = cur.fetchone()
                    id_of_new_row = None
                    if record is not None:
                        id_of_new_row = int(record[0])
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Simulation {config.name} installed successfully")
                    return id_of_new_row
                except psycopg.errors.UniqueViolation as e:
                    Logger.__call__().get_logger().debug(f"Simulation {config.name} is already installed, "
                                                         f"{str(e), repr(e)}")
                    return None

    @staticmethod
    def uninstall_simulation(config: SimulationEnvConfig) -> None:
        """
        Uninstalls the simulation configuration in the metastore

        :param config: the config to uninstall
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Uninstalling simulation:{config.name} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.SIMULATIONS_TABLE} WHERE name = %s", (config.name,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Simulation {config.name} uninstalled successfully")

    @staticmethod
    def save_emulation_trace(emulation_trace: EmulationTrace) -> Union[Any, int]:
        """
        Saves a trace from the emulation

        :param emulation_trace: the emulation trace to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Installing emulation trace for "
                                             f"emulation:{emulation_trace.emulation_name} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns on distributed tables properly
                id = GeneralUtil.get_latest_table_id(cur=cur,
                                                     table_name=constants.METADATA_STORE.EMULATION_TRACES_TABLE)
                config_json_str = json.dumps(emulation_trace.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                # Need to compress due to postgres size limits
                compressed_json_str = zlib.compress(config_json_str.encode())
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATION_TRACES_TABLE} "
                            f"(id, emulation_name, trace) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, emulation_trace.emulation_name,
                                                                  compressed_json_str))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation trace for "
                                                     f"emulation {emulation_trace.emulation_name} saved successfully")
                return id_of_new_row

    @staticmethod
    def save_emulation_statistic(emulation_statistics: EmulationStatistics) -> Union[Any, int]:
        """
        Saves a DTO with emulation statistics to the metastore

        :param emulation_statistics: the emulation statistics to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Installing statistics "
                                             f"for emulation:{emulation_statistics.emulation_name} in the metastore")
        emulation_statistics.compute_descriptive_statistics_and_distributions()
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns on distributed tables properly
                id = GeneralUtil.get_latest_table_id(cur=cur,
                                                     table_name=constants.METADATA_STORE.EMULATION_STATISTICS_TABLE)
                config_json_str = json.dumps(emulation_statistics.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                # Need to compress due to postgres size limits
                compressed_json_str = zlib.compress(config_json_str.encode())
                cur.execute(f"INSERT INTO "
                            f"{constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
                            f"(id, emulation_name, statistics) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, emulation_statistics.emulation_name,
                                                                  compressed_json_str))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug(f"Statistics for emulation "
                                                     f"{emulation_statistics.emulation_name} saved successfully")
                return id_of_new_row

    @staticmethod
    def update_emulation_statistic(emulation_statistics: EmulationStatistics, id: int) -> None:
        """
        Updates a row with emulation statistic in the metastore

        :param emulation_statistics: the emulation statistics to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Installing statistics "
                                             f"for emulation:{emulation_statistics.emulation_name} in the metastore")
        emulation_statistics.compute_descriptive_statistics_and_distributions()
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(emulation_statistics.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                compressed_json_str = zlib.compress(config_json_str.encode())
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
                            f" SET statistics=%s "
                            f"WHERE {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE}.id = %s",
                            (compressed_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Statistics for emulation "
                                                     f"{emulation_statistics.emulation_name} with id {id} "
                                                     f"updated successfully")

    @staticmethod
    def list_emulation_statistics() -> List[EmulationStatistics]:
        """
        :return: A list of emulation statistics in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_emulation_statistics_record_to_dto(x), records))

    @staticmethod
    def list_emulation_statistics_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of emulation statistics ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,emulation_name FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def list_emulation_traces() -> List[EmulationTrace]:
        """
        :return: A list of emulation traces in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_emulation_trace_record_to_dto(x), records))

    @staticmethod
    def list_emulation_traces_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of emulation traces ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,emulation_name FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def list_emulation_simulation_traces_ids() -> List[int]:
        """
        :return: A list of emulation-simulation traces ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: int(x[0]), records))

    @staticmethod
    def list_simulation_traces_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of simulation traces ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,gym_env FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def list_simulation_traces() -> List[SimulationTrace]:
        """
        :return: A list of simulation traces in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_simulation_trace_record_to_dto(x), records))

    @staticmethod
    def remove_simulation_trace(simulation_trace: SimulationTrace) -> None:
        """
        Removes a simulation trace from the metastore

        :param simulation_trace: the simulation trace to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing simulation traec with "
                                             f"id:{simulation_trace.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE} WHERE id = %s",
                            (simulation_trace.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Simulation trace "
                                                     f"with id {simulation_trace.id} deleted successfully")

    @staticmethod
    def get_emulation_trace(id: int) -> Union[None, EmulationTrace]:
        """
        Function for fetching an emulation trace with a given id from the metastore

        :param id: the id of the emulation trace
        :return: The emulation trace or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_trace_record_to_dto(emulation_trace_record=record)
                return record

    @staticmethod
    def remove_emulation_trace(emulation_trace: EmulationTrace) -> None:
        """
        Removes an emulation trace from the metastore

        :param emulation_trace: the emulation trace to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing simulation traec with "
                                             f"id:{emulation_trace.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE} WHERE id = %s",
                            (emulation_trace.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation trace "
                                                     f"with id {emulation_trace.id} deleted successfully")

    @staticmethod
    def remove_emulation_simulation_trace(emulation_simulation_trace: EmulationSimulationTrace) -> None:
        """
        Removes an emulation-simulation trace from the metastore

        :param emulation_simulation_trace: the emulation-simulation trace to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing an emulation-simulation trace with "
                                             f"id:{emulation_simulation_trace.id} "
                                             f"from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE} WHERE id = %s",
                            (emulation_simulation_trace.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation-Simulation trace "
                                                     f"with id {emulation_simulation_trace.id} deleted successfully")

    @staticmethod
    def get_emulation_statistic(id: int) -> Union[None, EmulationStatistics]:
        """
        Function for fetching an emulation satistic with a given id from the metastore

        :param id: the id of the statistics
        :return: The emulation statistic or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_statistics_record_to_dto(
                        emulation_statistics_record=record)
                return record

    @staticmethod
    def remove_emulation_statistic(emulation_statistic: EmulationStatistics) -> None:
        """
        Removes an emulation statistic from the metastore

        :param emulation_statistic: the emulation statistic to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing emulation statistic with "
                                             f"id:{emulation_statistic.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} WHERE id = %s",
                            (emulation_statistic.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation statistic "
                                                     f"with id {emulation_statistic.id} deleted successfully")

    @staticmethod
    def get_simulation_trace(id: int) -> Union[None, SimulationTrace]:
        """
        Function for fetching a simulation trace with a given id from the metastore

        :param id: the id of the simulation trace
        :return: The simulation trace or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_simulation_trace_record_to_dto(simulation_trace_record=record)
                return record

    @staticmethod
    def save_simulation_trace(simulation_trace: SimulationTrace) -> Union[Any, int]:
        """
        Saves a trace from the simulation

        :param simulation_trace: the simulation trace to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Installing simulation trace "
                                             f"for simulation env:{simulation_trace.simulation_env} "
                                             f"in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(cur=cur,
                                                     table_name=constants.METADATA_STORE.SIMULATION_TRACES_TABLE)
                config_json_str = json.dumps(simulation_trace.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.SIMULATION_TRACES_TABLE} (id, gym_env, trace) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, simulation_trace.simulation_env, config_json_str))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug(f"Simulation trace for "
                                                     f"env {simulation_trace.simulation_env} "
                                                     f"saved successfully")
                return id_of_new_row

    @staticmethod
    def save_emulation_simulation_trace(emulation_simulation_trace: EmulationSimulationTrace) -> Union[Any, int]:
        """
        Saves an emulation_simulation trace

        :param emulation_simulation_trace: the emulation trace to save
        :return: id of the new row
        """
        Logger.__call__().get_logger().debug(f"Installing emulation-simulation trace for "
                                             f"emulation:{emulation_simulation_trace.emulation_trace.emulation_name} "
                                             f"and simulation environment: "
                                             f"{emulation_simulation_trace.simulation_trace.simulation_env} in the "
                                             f"metastore")
        emulation_trace_id = MetastoreFacade.save_emulation_trace(
            emulation_trace=emulation_simulation_trace.emulation_trace)
        simulation_trace_id = MetastoreFacade.save_simulation_trace(
            simulation_trace=emulation_simulation_trace.simulation_trace)
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE)
                cur.execute(f"INSERT INTO "
                            f"{constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE} "
                            f"(id, emulation_trace, simulation_trace) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, emulation_trace_id, simulation_trace_id))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug(
                    f"Emulation-Simulation trace for "
                    f"emulation {emulation_simulation_trace.emulation_trace.emulation_name} "
                    f"and simulation: {emulation_simulation_trace.simulation_trace.simulation_env} saved successfully")
                return id_of_new_row

    @staticmethod
    def list_emulation_simulation_traces() -> List[EmulationSimulationTrace]:
        """
        :return: A list of emulation-simulation traces in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_emulation_simulation_trace_record_to_dto(x),
                                records))

    @staticmethod
    def get_emulation_simulation_trace(id: int) -> Union[None, EmulationSimulationTrace]:
        """
        Function for fetching a simulation trace with a given id from the metastore

        :param id: the id of the emulation-simulation trace
        :return: The emulation-simulation trace or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_simulation_trace_record_to_dto(
                        emulation_simulation_trace_record=record)
                return record

    @staticmethod
    def save_emulation_image(img: bytes, emulation_name: str) -> Any:
        """
        Saves the image of an emulation in the metastore

        :param img: the image data to save
        :param emulation_name: the name of the emulation
        :return: id of the created row
        """
        Logger.__call__().get_logger().debug(f"Saving image for emulation:{emulation_name} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    # Need to manually set the ID since CITUS does not handle serial columns
                    # on distributed tables properly
                    id = GeneralUtil.get_latest_table_id(cur=cur,
                                                         table_name=constants.METADATA_STORE.EMULATION_IMAGES_TABLE)
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATION_IMAGES_TABLE} "
                                f"(id, emulation_name, image) VALUES (%s, %s, %s) RETURNING id", (id,
                                                                                                  emulation_name, img))
                    record = cur.fetchone()
                    id_of_new_row = None
                    if record is not None:
                        id_of_new_row = int(record[0])
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Saved image for emulation {emulation_name} successfully")
                    return id_of_new_row
                except Exception as e:
                    Logger.__call__().get_logger().warning(f"There was an error saving an image "
                                                           f"for emulation {emulation_name}, {str(e), repr(e)}")

    @staticmethod
    def list_emulation_images() -> List[Tuple[str, bytes]]:
        """
        :return: A list of emulation names and images in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_IMAGES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_emulation_image_record_to_tuple(x), records))

    @staticmethod
    def get_emulation_image(emulation_name: str) -> Union[None, Tuple[str, bytes]]:
        """
        Function for fetching the image of a given emulation

        :param emulation_name: the name of the emulatin to fetch the image for
        :return: The simulation trace or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_IMAGES_TABLE} "
                            f"WHERE emulation_name = %s", (emulation_name,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_image_record_to_tuple(emulation_image_record=record)
                return record

    @staticmethod
    def delete_all(table: str) -> None:
        """
        Deletes all rows in the metastore from a given table

        :param table: the table to delete from
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Deleting all traces from table "
                                             f"{table}")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {table}")
                conn.commit()

                Logger.__call__().get_logger().debug(f"All traces deleted from table "
                                                     f"{table} successfully")

    @staticmethod
    def save_simulation_image(img: bytes, simulation_name: str) -> Union[Any, int]:
        """
        Saves the image of a simulation in the metastore

        :param img: the image data to save
        :param simulation_name: the name of the simulation
        :return: id of the created row
        """
        Logger.__call__().get_logger().debug(f"Saving image for simulation:{simulation_name} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    # Need to manually set the ID since CITUS does not handle serial columns
                    # on distributed tables properly
                    id = GeneralUtil.get_latest_table_id(cur=cur,
                                                         table_name=constants.METADATA_STORE.SIMULATION_IMAGES_TABLE)
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.SIMULATION_IMAGES_TABLE} "
                                f"(id, simulation_name, image) VALUES (%s, %s, %s) RETURNING id",
                                (id, simulation_name, img))
                    record = cur.fetchone()
                    id_of_new_row = None
                    if record is not None:
                        id_of_new_row = int(record[0])
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Saved image for simulation {simulation_name} successfully")
                    return id_of_new_row
                except Exception as e:
                    Logger.__call__().get_logger().warning(f"There was an error saving an image "
                                                           f"for simulation {simulation_name}, {str(e), repr(e)}")
                    return None

    @staticmethod
    def list_simulation_images() -> List[Tuple[str, bytes]]:
        """
        :return: A list of simulation names and images in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_IMAGES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_simulation_image_record_to_tuple(x), records))

    @staticmethod
    def get_simulation_image(simulation_name: str) -> Union[None, Tuple[str, bytes]]:
        """
        Function for fetching the image of a given simulation

        :param simulation_name: the name of the simulation to fetch the image for
        :return: The simulation trace or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_IMAGES_TABLE} "
                            f"WHERE simulation_name = %s", (simulation_name,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_simulation_image_record_to_tuple(simulation_image_record=record)
                return record

    @staticmethod
    def save_experiment_execution(experiment_execution: ExperimentExecution) -> Union[Any, int]:
        """
        Saves an experiment execution to the metastore

        :param experiment_execution: the experiment execution to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Installing experiment exection for emulation: "
                                             f"{experiment_execution.emulation_name} "
                                             f"and simulation: {experiment_execution.simulation_name} "
                                             f"in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(cur=cur,
                                                     table_name=constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE)
                config_json_str = json.dumps(experiment_execution.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} "
                            f"(id, execution, simulation_name, emulation_name) "
                            f"VALUES (%s, %s, %s, %s) RETURNING id",
                            (id, config_json_str, experiment_execution.simulation_name,
                             experiment_execution.emulation_name))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug(f"Experiment execution for "
                                                     f"emulation {experiment_execution.emulation_name} "
                                                     f"and simulation {experiment_execution.simulation_name} "
                                                     f"saved successfully")
                return id_of_new_row

    @staticmethod
    def list_experiment_executions() -> List[ExperimentExecution]:
        """
        :return: A list of emulation traces in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_experiment_execution_record_to_dto(x), records))

    @staticmethod
    def list_experiment_executions_ids() -> List[Tuple[int, str, str]]:
        """
        :return: A list of experiment execution ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name,emulation_name FROM "
                            f"{constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1]), str(x[2])), records))

    @staticmethod
    def _convert_experiment_execution_record_to_dto(experiment_execution_record) -> ExperimentExecution:
        """
        Converts an experiment execution record fetched from the metastore into a DTO

        :param experiment_execution_record: the record to convert
        :return: the DTO representing the record
        """
        experiment_execution_json = json.dumps(experiment_execution_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        experiment_execution: ExperimentExecution = ExperimentExecution.from_dict(json.loads(experiment_execution_json))
        experiment_execution.id = experiment_execution_record[0]
        return experiment_execution

    @staticmethod
    def get_experiment_execution(id: int) -> Union[None, ExperimentExecution]:
        """
        Function for fetching an experiment execution with a given id from the metastore

        :param id: the id of the emulation trace
        :return: The emulation trace or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_experiment_execution_record_to_dto(
                        experiment_execution_record=record)
                return record

    @staticmethod
    def remove_experiment_execution(experiment_execution: ExperimentExecution) -> None:
        """
        Removes an experiment execution from the metastore

        :param experiment_execution: the experiment execution to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing experiment execution with "
                                             f"id:{experiment_execution.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} WHERE id = %s",
                            (experiment_execution.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Experiment execution "
                                                     f"with id {experiment_execution.id} deleted successfully")

    @staticmethod
    def list_multi_threshold_stopping_policies() -> List[MultiThresholdStoppingPolicy]:
        """
        :return: A list of Multi-threshold stopping policies in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(
                    lambda x: MetastoreFacade._convert_multi_threshold_stopping_policy_record_to_dto(x), records))

    @staticmethod
    def list_multi_threshold_stopping_policies_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of Multi-threshold stopping policies ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name FROM "
                            f"{constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def _convert_multi_threshold_stopping_policy_record_to_dto(multi_threshold_stopping_policy_record) \
            -> MultiThresholdStoppingPolicy:
        """
        Converts a Multi-threshold stopping policy record fetched from the metastore into a DTO

        :param multi_threshold_stopping_policy_record: the record to convert
        :return: the DTO representing the record
        """
        multi_threshold_stopping_policy_json = json.dumps(multi_threshold_stopping_policy_record[1], indent=4,
                                                          sort_keys=True, cls=NpEncoder)
        multi_threshold_stopping_policy: MultiThresholdStoppingPolicy = MultiThresholdStoppingPolicy.from_dict(
            json.loads(multi_threshold_stopping_policy_json))
        multi_threshold_stopping_policy.id = multi_threshold_stopping_policy_record[0]
        return multi_threshold_stopping_policy

    @staticmethod
    def get_multi_threshold_stopping_policy(id: int) -> Union[None, MultiThresholdStoppingPolicy]:
        """
        Function for fetching a mult-threshold policy with a given id from the metastore

        :param id: the id of the multi-threshold policy
        :return: The mult-threshold policy or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_multi_threshold_stopping_policy_record_to_dto(
                        multi_threshold_stopping_policy_record=record)
                return record

    @staticmethod
    def remove_multi_threshold_stopping_policy(multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) -> None:
        """
        Removes a multi-threshold stopping policy from the metastore

        :param multi_threshold_stopping_policy: the policy to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing Multi-threshold stopping policy with "
                                             f"id:{multi_threshold_stopping_policy.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE} "
                            f"WHERE id = %s",
                            (multi_threshold_stopping_policy.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Multi-threshold stopping policy "
                                                     f"with id {multi_threshold_stopping_policy.id} "
                                                     f"deleted successfully")

    @staticmethod
    def save_multi_threshold_stopping_policy(multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) \
            -> Union[Any, int]:
        """
        Saves a multi-threshold stopping policy to the metastore

        :param multi_threshold_stopping_policy: the policy to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Installing a multi-threshold stopping policy in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE)
                policy_json_str = json.dumps(multi_threshold_stopping_policy.to_dict(), indent=4, sort_keys=True,
                                             cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE} "
                            f"(id, policy, simulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, policy_json_str,
                                                                  multi_threshold_stopping_policy.simulation_name))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("Multi-threshold policy saved successfully")
                return id_of_new_row

    @staticmethod
    def _convert_training_job_record_to_dto(training_job_record) -> TrainingJobConfig:
        """
        Converts a training job record fetched from the metastore into a DTO

        :param training_job_record: the record to convert
        :return: the DTO representing the record
        """
        tranining_job_config_json = json.dumps(training_job_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        training_job_config: TrainingJobConfig = TrainingJobConfig.from_dict(json.loads(tranining_job_config_json))
        training_job_config.id = training_job_record[0]
        return training_job_config

    @staticmethod
    def list_training_jobs() -> List[TrainingJobConfig]:
        """
        :return: A list of training jobs in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TRAINING_JOBS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_training_job_record_to_dto(x), records))

    @staticmethod
    def list_training_jobs_ids() -> List[Tuple[int, str, str, int]]:
        """
        :return: A list of training job ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name,emulation_name,pid FROM "
                            f"{constants.METADATA_STORE.TRAINING_JOBS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1]), str(x[2]), int(x[3])), records))

    @staticmethod
    def get_training_job_config(id: int) -> Union[None, TrainingJobConfig]:
        """
        Function for fetching a training job config with a given id from the metastore

        :param id: the id of the training job config
        :return: The trainign job config or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TRAINING_JOBS_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_training_job_record_to_dto(training_job_record=record)
                return record

    @staticmethod
    def save_training_job(training_job: TrainingJobConfig) -> Union[Any, int]:
        """
        Saves a training job to the metastore

        :param training_job: the training job to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Saving a training job in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                id = GeneralUtil.get_latest_table_id(cur=cur,
                                                     table_name=constants.METADATA_STORE.TRAINING_JOBS_TABLE)
                training_job_str = json.dumps(training_job.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                emulation_name: Union[str, None] = training_job.emulation_env_name
                if emulation_name == "":
                    emulation_name = None
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.TRAINING_JOBS_TABLE} "
                            f"(id, config, simulation_name, emulation_name, pid) "
                            f"VALUES (%s, %s, %s, %s, %s) RETURNING id",
                            (id, training_job_str, training_job.simulation_env_name, emulation_name, training_job.pid))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("Training job saved successfully")
                return id_of_new_row

    @staticmethod
    def _convert_data_collection_job_record_to_dto(data_collection_job_record) -> \
            DataCollectionJobConfig:
        """
        Converts a data collection job record fetched from the metastore into a DTO

        :param data_collection_job_record: the record to convert
        :return: the DTO representing the record
        """
        data_collection_job_config_json = json.dumps(data_collection_job_record[1], indent=4,
                                                     sort_keys=True, cls=NpEncoder)
        data_collection_job_config: DataCollectionJobConfig = \
            DataCollectionJobConfig.from_dict(json.loads(data_collection_job_config_json))
        data_collection_job_config.id = data_collection_job_record[0]
        return data_collection_job_config

    @staticmethod
    def list_data_collection_jobs() -> List[DataCollectionJobConfig]:
        """
        :return: A list of data collection jobs in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_data_collection_job_record_to_dto(x), records))

    @staticmethod
    def list_data_collection_jobs_ids() -> List[Tuple[int, str, int]]:
        """
        :return: A list of data collection job ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,emulation_name,pid FROM {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1]), int(x[2])), records))

    @staticmethod
    def get_data_collection_job_config(id: int) -> Union[None, DataCollectionJobConfig]:
        """
        Function for fetching a data collection job config with a given id from the metastore

        :param id: the id of the data collection job config
        :return: The data collection job config or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_data_collection_job_record_to_dto(
                        data_collection_job_record=record)
                return record

    @staticmethod
    def save_data_collection_job(data_collection_job: DataCollectionJobConfig) -> Union[Any, int]:
        """
        Saves a data collection job to the metastore

        :param data_collection_job: the data collection job to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Saving a data collection job in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns on distributed tables properly
                id = GeneralUtil.get_latest_table_id(cur=cur,
                                                     table_name=constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE)
                data_collection_job_json = json.dumps(data_collection_job.to_dict(), indent=4,
                                                      sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE} "
                            f"(id, config, emulation_name, pid) "
                            f"VALUES (%s, %s, %s, %s) RETURNING id",
                            (id, data_collection_job_json, data_collection_job.emulation_env_name,
                             data_collection_job.pid))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("Data collection job saved successfully")
                return id_of_new_row

    @staticmethod
    def update_training_job(training_job: TrainingJobConfig, id: int) -> None:
        """
        Updates a training job in the metastore

        :param training_job: the training job to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating training job with id: {id} in the metastore")
        for i in range(constants.METADATA_STORE.NUM_RETRIES_UPDATE_TRAINING_JOB):
            try:
                with psycopg.connect(
                        f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                        f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                        f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                        f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
                    with conn.cursor() as cur:
                        config_json_str = json.dumps(training_job.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                        cur.execute(f"UPDATE "
                                    f"{constants.METADATA_STORE.TRAINING_JOBS_TABLE} "
                                    f" SET config=%s "
                                    f"WHERE {constants.METADATA_STORE.TRAINING_JOBS_TABLE}.id = %s",
                                    (config_json_str, id))
                        conn.commit()
                        Logger.__call__().get_logger().debug(f"Training job with id: {id} updated successfully")
                        break
            except Exception:
                pass

    @staticmethod
    def update_experiment_execution(experiment_execution: ExperimentExecution, id: int) -> None:
        """
        Updates an experiment execution in the metastore

        :param experiment_execution: the experiment execution to update
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating experiment execution with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(experiment_execution.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} "
                            f" SET execution=%s "
                            f"WHERE {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Experiment execution with id: {id} updated successfully")

    @staticmethod
    def update_data_collection_job(data_collection_job: DataCollectionJobConfig, id: int) -> None:
        """
        Updates a data collection job in the metastore

        :param training_job: the training job to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating data collection job with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(data_collection_job.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE} "
                            f" SET config=%s "
                            f"WHERE {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Data collection job with id: {id} updated successfully")

    @staticmethod
    def remove_training_job(training_job: TrainingJobConfig) -> None:
        """
        Removes a training job from the metastore

        :param config: the config to uninstall
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing training job with id:{training_job.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.TRAINING_JOBS_TABLE} WHERE id = %s",
                            (training_job.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Training job with id {training_job.id} deleted successfully")

    @staticmethod
    def remove_data_collection_job(data_collection_job: DataCollectionJobConfig) -> None:
        """
        Removes a data collection job from the metastore

        :param config: the config to uninstall
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing data collection job with "
                                             f"id:{data_collection_job.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE} WHERE id = %s",
                            (data_collection_job.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Training job with "
                                                     f"id {data_collection_job.id} deleted successfully")

    @staticmethod
    def list_ppo_policies() -> List[PPOPolicy]:
        """
        :return: A list of PPO policies in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.PPO_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_ppo_policy_record_to_dto(x), records))

    @staticmethod
    def list_ppo_policies_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of PPO policies ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name FROM {constants.METADATA_STORE.PPO_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def _convert_ppo_policy_record_to_dto(ppo_policy_record) -> PPOPolicy:
        """
        Converts a PPO policy record fetched from the metastore into a DTO

        :param ppo_policy_record: the record to convert
        :return: the DTO representing the record
        """
        ppo_policy_json = json.dumps(ppo_policy_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        ppo_policy: PPOPolicy = PPOPolicy.from_dict(json.loads(ppo_policy_json))
        ppo_policy.id = ppo_policy_record[0]
        return ppo_policy

    @staticmethod
    def get_ppo_policy(id: int) -> Union[None, PPOPolicy]:
        """
        Function for fetching a PPO policy with a given id from the metastore

        :param id: the id of the PPO policy
        :return: The PPO policy or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.PPO_POLICIES_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_ppo_policy_record_to_dto(ppo_policy_record=record)
                return record

    @staticmethod
    def remove_ppo_policy(ppo_policy: PPOPolicy) -> None:
        """
        Removes a PPO policy from the metastore

        :param ppo_policy: the policy to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing ppo policy with "
                                             f"id:{ppo_policy.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.PPO_POLICIES_TABLE} WHERE id = %s",
                            (ppo_policy.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"PPO policy "
                                                     f"with id {ppo_policy.id} deleted successfully")

    @staticmethod
    def save_ppo_policy(ppo_policy: PPOPolicy) -> Union[Any, int]:
        """
        Saves a PPO policy to the metastore

        :param ppo_policy: the policy to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Installing PPO policy in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(cur=cur,
                                                     table_name=constants.METADATA_STORE.PPO_POLICIES_TABLE)
                policy_json_str = json.dumps(ppo_policy.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.PPO_POLICIES_TABLE} "
                            f"(id, policy, simulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, policy_json_str, ppo_policy.simulation_name))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("PPO policy saved successfully")
                return id_of_new_row

    @staticmethod
    def _convert_system_identification_job_record_to_dto(system_identification_job_record) -> \
            SystemIdentificationJobConfig:
        """
        Converts a system identification job record fetched from the metastore into a DTO

        :param system_identification_job_record: the record to convert
        :return: the DTO representing the record
        """
        system_identification_job_config_json = json.dumps(system_identification_job_record[1], indent=4,
                                                           sort_keys=True, cls=NpEncoder)
        system_identification_job_config: SystemIdentificationJobConfig = \
            SystemIdentificationJobConfig.from_dict(json.loads(system_identification_job_config_json))
        system_identification_job_config.id = system_identification_job_record[0]
        return system_identification_job_config

    @staticmethod
    def list_system_identification_jobs() -> List[SystemIdentificationJobConfig]:
        """
        :return: A list of system identification jobs in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_system_identification_job_record_to_dto(x), records))

    @staticmethod
    def list_system_identification_jobs_ids() -> List[Tuple[int, str, int]]:
        """
        :return: A list of system identification job ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,emulation_name,pid FROM "
                            f"{constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1]), int(x[2])), records))

    @staticmethod
    def get_system_identification_job_config(id: int) -> Union[None, SystemIdentificationJobConfig]:
        """
        Function for fetching a system identification job config with a given id from the metastore

        :param id: the id of the system identification job config
        :return: The system identification job config or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM "
                            f"{constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_system_identification_job_record_to_dto(
                        system_identification_job_record=record)
                return record

    @staticmethod
    def save_system_identification_job(system_identification_job: SystemIdentificationJobConfig) -> Union[Any, int]:
        """
        Saves a system_identification job to the metastore

        :param system_identification_job: the system identification job to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Saving a system identification job in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE)
                system_identification_job_json = json.dumps(system_identification_job.to_dict(), indent=4,
                                                            sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} "
                            f"(id, config, emulation_name, pid) "
                            f"VALUES (%s, %s, %s, %s) RETURNING id", (id, system_identification_job_json,
                                                                      system_identification_job.emulation_env_name,
                                                                      system_identification_job.pid))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("System identification job saved successfully")
                return id_of_new_row

    @staticmethod
    def update_system_identification_job(system_identification_job: SystemIdentificationJobConfig, id: int) -> None:
        """
        Updates a system identification job in the metastore

        :param system_identification_job: the system identification job to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating system identification job with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(system_identification_job.to_dict(), indent=4, sort_keys=True,
                                             cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} "
                            f" SET config=%s "
                            f"WHERE {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"System identification job with id: {id} updated successfully")

    @staticmethod
    def remove_system_identification_job(system_identification_job: SystemIdentificationJobConfig) -> None:
        """
        Removes a system identification job from the metastore

        :param system_identification_job: the job to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing system identification job with "
                                             f"id:{system_identification_job.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} WHERE id = %s",
                            (system_identification_job.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"System identification job with "
                                                     f"id {system_identification_job.id} deleted successfully")

    @staticmethod
    def _convert_gaussian_mixture_system_model_record_to_dto(gaussian_mixture_system_model_record) -> \
            GaussianMixtureSystemModel:
        """
        Converts a gaussian mixture system model record fetched from the metastore into a DTO

        :param gaussian_mixture_system_model_record: the record to convert
        :return: the DTO representing the record
        """
        gaussian_mixture_system_model_config_json = json.dumps(gaussian_mixture_system_model_record[1], indent=4,
                                                               sort_keys=True, cls=NpEncoder)
        gaussian_mixture_system_model_config: GaussianMixtureSystemModel = \
            GaussianMixtureSystemModel.from_dict(json.loads(gaussian_mixture_system_model_config_json))
        gaussian_mixture_system_model_config.id = gaussian_mixture_system_model_record[0]
        return gaussian_mixture_system_model_config

    @staticmethod
    def list_gaussian_mixture_system_models() -> List[GaussianMixtureSystemModel]:
        """
        :return: A list of gaussian mixture system models in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                return list(map(
                    lambda x: MetastoreFacade._convert_gaussian_mixture_system_model_record_to_dto(x), records))

    @staticmethod
    def list_gaussian_mixture_system_models_ids() -> List[Tuple[int, str, int]]:
        """
        :return: A list of gaussian mixture system model ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,emulation_name,emulation_statistic_id FROM "
                            f"{constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1]), int(x[2])), records))

    @staticmethod
    def get_gaussian_mixture_system_model_config(id: int) -> Union[None, GaussianMixtureSystemModel]:
        """
        Function for fetching a gaussian mixture system model config with a given id from the metastore

        :param id: the id of the gaussian mixture system model config
        :return: The gaussian mixture system model config or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_gaussian_mixture_system_model_record_to_dto(
                        gaussian_mixture_system_model_record=record)
                return record

    @staticmethod
    def save_gaussian_mixture_system_model(gaussian_mixture_system_model: GaussianMixtureSystemModel) \
            -> Union[Any, int]:
        """
        Saves a gaussian mixture system model to the metastore

        :param gaussian_mixture_system_model: the gaussian mixture system model to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Saving a gaussian mixture system model in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE)
                gaussian_mixture_system_model_json = json.dumps(gaussian_mixture_system_model.to_dict(), indent=4,
                                                                sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
                            f"(id, model, emulation_name, emulation_statistic_id) "
                            f"VALUES (%s, %s, %s, %s) RETURNING id",
                            (id, gaussian_mixture_system_model_json,
                             gaussian_mixture_system_model.emulation_env_name,
                             gaussian_mixture_system_model.emulation_statistic_id))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("Gaussian mixture model saved successfully")
                return id_of_new_row

    @staticmethod
    def update_gaussian_mixture_system_model(gaussian_mixture_system_model: GaussianMixtureSystemModel, id: int) \
            -> None:
        """
        Updates a gaussian mixture system model in the metastore

        :param gaussian_mixture_system_model: the gaussian mixture system model to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating gaussian mixture system model with id: {id} "
                                             f"in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(gaussian_mixture_system_model.to_dict(), indent=4, sort_keys=True,
                                             cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
                            f" SET config=%s "
                            f"WHERE {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Gaussian mixture system model with id: {id} "
                                                     f"updated successfully")

    @staticmethod
    def remove_gaussian_mixture_system_model(gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Removes a gaussian mixture system model from the metastore

        :param gaussian_mixture_system_model: the to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing gaussian mixture system model with "
                                             f"id:{gaussian_mixture_system_model.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
                            f"WHERE id = %s", (gaussian_mixture_system_model.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Gaussian mixture system model with "
                                                     f"id {gaussian_mixture_system_model.id} deleted successfully")

    @staticmethod
    def list_tabular_policies() -> List[TabularPolicy]:
        """
        :return: A list of Tabular policies in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TABULAR_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_tabular_policy_record_to_dto(x), records))

    @staticmethod
    def list_tabular_policies_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of Tabular policies ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name FROM {constants.METADATA_STORE.TABULAR_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def _convert_tabular_policy_record_to_dto(tabular_policy_record) -> TabularPolicy:
        """
        Converts a Tabular policy record fetched from the metastore into a DTO

        :param tabular_policy_record: the record to convert
        :return: the DTO representing the record
        """
        tabular_policy_json = json.dumps(tabular_policy_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        tabular_policy: TabularPolicy = TabularPolicy.from_dict(json.loads(tabular_policy_json))
        tabular_policy.id = tabular_policy_record[0]
        return tabular_policy

    @staticmethod
    def get_tabular_policy(id: int) -> Union[None, TabularPolicy]:
        """
        Function for fetching a Tabular policy with a given id from the metastore

        :param id: the id of the Tabular policy
        :return: The Tabular policy or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TABULAR_POLICIES_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_tabular_policy_record_to_dto(tabular_policy_record=record)
                return record

    @staticmethod
    def remove_tabular_policy(tabular_policy: TabularPolicy) -> None:
        """
        Removes a Tabular policy from the metastore

        :param tabular_policy: the policy to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing tabular policy with "
                                             f"id:{tabular_policy.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.TABULAR_POLICIES_TABLE} WHERE id = %s",
                            (tabular_policy.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Tabular policy "
                                                     f"with id {tabular_policy.id} deleted successfully")

    @staticmethod
    def save_tabular_policy(tabular_policy: TabularPolicy) -> Union[Any, int]:
        """
        Saves a Tabular policy to the metastore

        :param tabular_policy: the policy to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Installing Tabular policy in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.TABULAR_POLICIES_TABLE)
                policy_json_str = json.dumps(tabular_policy.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.TABULAR_POLICIES_TABLE} "
                            f"(id, policy, simulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, policy_json_str, tabular_policy.simulation_name))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("Tabular policy saved successfully")
                return id_of_new_row

    @staticmethod
    def list_alpha_vec_policies() -> List[AlphaVectorsPolicy]:
        """
        :return: A list of AlphaVec policies in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_alpha_vec_policy_record_to_dto(x), records))

    @staticmethod
    def list_alpha_vec_policies_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of AlphaVec policies ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name FROM {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def _convert_alpha_vec_policy_record_to_dto(alpha_vec_policy_record) -> AlphaVectorsPolicy:
        """
        Converts a AlphaVec policy record fetched from the metastore into a DTO

        :param alpha_vec_policy_record: the record to convert
        :return: the DTO representing the record
        """
        alpha_vec_policy_json = json.dumps(alpha_vec_policy_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        alpha_vec_policy: AlphaVectorsPolicy = AlphaVectorsPolicy.from_dict(json.loads(alpha_vec_policy_json))
        alpha_vec_policy.id = alpha_vec_policy_record[0]
        return alpha_vec_policy

    @staticmethod
    def get_alpha_vec_policy(id: int) -> Union[None, AlphaVectorsPolicy]:
        """
        Function for fetching a AlphaVec policy with a given id from the metastore

        :param id: the id of the AlphaVec policy
        :return: The AlphaVec policy or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_alpha_vec_policy_record_to_dto(alpha_vec_policy_record=record)
                return record

    @staticmethod
    def remove_alpha_vec_policy(alpha_vec_policy: AlphaVectorsPolicy) -> None:
        """
        Removes a AlphaVec policy from the metastore

        :param alpha_vec_policy: the policy to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing alpha_vec policy with "
                                             f"id:{alpha_vec_policy.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE} WHERE id = %s",
                            (alpha_vec_policy.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"AlphaVec policy "
                                                     f"with id {alpha_vec_policy.id} deleted successfully")

    @staticmethod
    def save_alpha_vec_policy(alpha_vec_policy: AlphaVectorsPolicy) -> Union[Any, int]:
        """
        Saves a AlphaVec policy to the metastore

        :param alpha_vec_policy: the policy to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Installing AlphaVec policy in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE)
                policy_json_str = json.dumps(alpha_vec_policy.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.ALPHA_VEC_POLICIES_TABLE} "
                            f"(id, policy, simulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id,
                                                                  policy_json_str, alpha_vec_policy.simulation_name))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("AlphaVec policy saved successfully")
                return id_of_new_row

    @staticmethod
    def list_dqn_policies() -> List[DQNPolicy]:
        """
        :return: A list of DQN policies in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.DQN_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_dqn_policy_record_to_dto(x), records))

    @staticmethod
    def list_dqn_policies_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of DQN policies ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name FROM {constants.METADATA_STORE.DQN_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def _convert_dqn_policy_record_to_dto(dqn_policy_record) -> DQNPolicy:
        """
        Converts a DQN policy record fetched from the metastore into a DTO

        :param dqn_policy_record: the record to convert
        :return: the DTO representing the record
        """
        dqn_policy_json = json.dumps(dqn_policy_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        dqn_policy: DQNPolicy = DQNPolicy.from_dict(json.loads(dqn_policy_json))
        dqn_policy.id = dqn_policy_record[0]
        return dqn_policy

    @staticmethod
    def get_dqn_policy(id: int) -> Union[None, DQNPolicy]:
        """
        Function for fetching a DQN policy with a given id from the metastore

        :param id: the id of the DQN policy
        :return: The DQN policy or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.DQN_POLICIES_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_dqn_policy_record_to_dto(dqn_policy_record=record)
                return record

    @staticmethod
    def remove_dqn_policy(dqn_policy: DQNPolicy) -> None:
        """
        Removes a DQN policy from the metastore

        :param dqn_policy: the policy to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing dqn policy with "
                                             f"id:{dqn_policy.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.DQN_POLICIES_TABLE} WHERE id = %s",
                            (dqn_policy.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"DQN policy "
                                                     f"with id {dqn_policy.id} deleted successfully")

    @staticmethod
    def save_dqn_policy(dqn_policy: DQNPolicy) -> Union[Any, int]:
        """
        Saves a DQN policy to the metastore

        :param dqn_policy: the policy to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Installing DQN policy in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.DQN_POLICIES_TABLE)
                policy_json_str = json.dumps(dqn_policy.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.DQN_POLICIES_TABLE} "
                            f"(id, policy, simulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, policy_json_str, dqn_policy.simulation_name))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("DQN policy saved successfully")
                return id_of_new_row

    @staticmethod
    def list_fnn_w_softmax_policies() -> List[FNNWithSoftmaxPolicy]:
        """
        :return: A list of FNN with softmax policies in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_fnn_w_softmax_policy_record_to_dto(x), records))

    @staticmethod
    def list_fnn_w_softmax_policies_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of FNN with softmax policies ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name FROM {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def _convert_fnn_w_softmax_policy_record_to_dto(fnn_w_softmax_policy_record) -> FNNWithSoftmaxPolicy:
        """
        Converts a FNN with softmax policy record fetched from the metastore into a DTO

        :param fnn_w_softmax_policy_record: the record to convert
        :return: the DTO representing the record
        """
        fnn_w_softmax_policy_json = json.dumps(fnn_w_softmax_policy_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        fnn_w_softmax_policy: FNNWithSoftmaxPolicy = FNNWithSoftmaxPolicy.from_dict(json.loads(
            fnn_w_softmax_policy_json))
        fnn_w_softmax_policy.id = fnn_w_softmax_policy_record[0]
        return fnn_w_softmax_policy

    @staticmethod
    def get_fnn_w_softmax_policy(id: int) -> Union[None, FNNWithSoftmaxPolicy]:
        """
        Function for fetching a FNN with softmax policy with a given id from the metastore

        :param id: the id of the FNN with softmax policy
        :return: The FNN with softmax policy or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_fnn_w_softmax_policy_record_to_dto(
                        fnn_w_softmax_policy_record=record)
                return record

    @staticmethod
    def remove_fnn_w_softmax_policy(fnn_w_softmax_policy: FNNWithSoftmaxPolicy) -> None:
        """
        Removes a FNN with softmax policy from the metastore

        :param fnn_w_softmax_policy: the policy to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing fnn_w_softmax policy with "
                                             f"id:{fnn_w_softmax_policy.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE} WHERE id = %s",
                            (fnn_w_softmax_policy.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"FNN with softmax policy "
                                                     f"with id {fnn_w_softmax_policy.id} deleted successfully")

    @staticmethod
    def save_fnn_w_softmax_policy(fnn_w_softmax_policy: FNNWithSoftmaxPolicy) -> Union[Any, int]:
        """
        Saves a FNN with softmax policy to the metastore

        :param fnn_w_softmax_policy: the policy to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Installing FNN with softmax policy in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE)
                policy_json_str = json.dumps(fnn_w_softmax_policy.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.FNN_W_SOFTMAX_POLICIES_TABLE} "
                            f"(id, policy, simulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id,
                                                                  policy_json_str,
                                                                  fnn_w_softmax_policy.simulation_name))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("FNN with softmax policy saved successfully")
                return id_of_new_row

    @staticmethod
    def list_vector_policies() -> List[VectorPolicy]:
        """
        :return: A list of vector policies in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.VECTOR_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_vector_policy_record_to_dto(x), records))

    @staticmethod
    def list_vector_policies_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of vector policies ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name FROM {constants.METADATA_STORE.VECTOR_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def _convert_vector_policy_record_to_dto(vector_policy_record) -> VectorPolicy:
        """
        Converts a vector policy record fetched from the metastore into a DTO

        :param vector_policy_record: the record to convert
        :return: the DTO representing the record
        """
        vector_policy_json = json.dumps(vector_policy_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        vector_policy: VectorPolicy = VectorPolicy.from_dict(json.loads(vector_policy_json))
        vector_policy.id = vector_policy_record[0]
        return vector_policy

    @staticmethod
    def get_vector_policy(id: int) -> Union[None, VectorPolicy]:
        """
        Function for fetching a vector policy with a given id from the metastore

        :param id: the id of the vector policy
        :return: The vector policy or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.VECTOR_POLICIES_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_vector_policy_record_to_dto(vector_policy_record=record)
                return record

    @staticmethod
    def remove_vector_policy(vector_policy: VectorPolicy) -> None:
        """
        Removes a vector policy from the metastore

        :param vector_policy: the policy to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing vector policy with "
                                             f"id:{vector_policy.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.VECTOR_POLICIES_TABLE} WHERE id = %s",
                            (vector_policy.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"vector policy "
                                                     f"with id {vector_policy.id} deleted successfully")

    @staticmethod
    def save_vector_policy(vector_policy: VectorPolicy) -> Union[Any, int]:
        """
        Saves a vector policy to the metastore

        :param vector_policy: the policy to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Installing vector policy in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.VECTOR_POLICIES_TABLE)
                policy_json_str = json.dumps(vector_policy.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.VECTOR_POLICIES_TABLE} "
                            f"(id, policy, simulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, policy_json_str, vector_policy.simulation_name))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("vector policy saved successfully")
                return id_of_new_row

    @staticmethod
    def list_emulation_execution_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of emulation executions in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT ip_first_octet,emulation_name FROM "
                            f"{constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def list_emulation_executions() -> List[EmulationExecution]:
        """
        :return: A list of emulation executions in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_emulation_execution_record_to_dto(x), records))

    @staticmethod
    def list_emulation_executions_for_a_given_emulation(emulation_name: str) -> List[EmulationExecution]:
        """
        :param emulation_name: the name of the emulation
        :return: A list of emulation executions in the metastore for a given emulation
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
                            f"WHERE emulation_name = %s", (emulation_name,))
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_emulation_execution_record_to_dto(x), records))

    @staticmethod
    def list_emulation_executions_by_id(id: int) -> List[EmulationExecution]:
        """
        :param id: the first IP octet of the execution
        :return: A list of emulation executions in the metastore for a given emulation
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
                            f"WHERE ip_first_octet = %s", (id,))
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_emulation_execution_record_to_dto(x), records))

    @staticmethod
    def _convert_emulation_execution_record_to_dto(emulation_execution_record) -> EmulationExecution:
        """
        Converts a emulation execution record fetched from the metastore into a DTO

        :param emulation_execution_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_execution_json = json.dumps(emulation_execution_record[2], indent=4, sort_keys=True, cls=NpEncoder)
        emulation_execution: EmulationExecution = EmulationExecution.from_dict(json.loads(emulation_execution_json))
        return emulation_execution

    @staticmethod
    def get_emulation_execution(ip_first_octet: int, emulation_name: str) -> Union[None, EmulationExecution]:
        """
        Function for fetching a emulation execution with a given id from the metastore

        :param ip_first_octet: the id of the emulation execution
        :param emulation_name: the name of the emulation
        :return: The emulation execution or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
                            f"WHERE ip_first_octet = %s AND emulation_name=%s", (ip_first_octet, emulation_name))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_execution_record_to_dto(
                        emulation_execution_record=record)
                return record

    @staticmethod
    def remove_emulation_execution(emulation_execution: EmulationExecution) -> None:
        """
        Removes a emulation execution from the metastore

        :param emulation_execution: the policy to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing emulation execution with "
                                             f"ip_first_octet:{emulation_execution.ip_first_octet} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
                            f"WHERE ip_first_octet = %s AND emulation_name = %s",
                            (emulation_execution.ip_first_octet, emulation_execution.emulation_name))
                conn.commit()
                Logger.__call__().get_logger().debug(f"emulation execution "
                                                     f"with ip_first_octet {emulation_execution.ip_first_octet} "
                                                     f"deleted successfully")

    @staticmethod
    def save_emulation_execution(emulation_execution: EmulationExecution) -> Union[Any, int]:
        """
        Saves a emulation execution to the metastore

        :param emulation_execution: the policy to save
        :return: None
        """
        Logger.__call__().get_logger().debug("Installing emulation execution in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                emulation_execution_str = \
                    json.dumps(emulation_execution.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
                            f"(ip_first_octet, emulation_name, info) "
                            f"VALUES (%s, %s, %s) RETURNING ip_first_octet",
                            (
                                emulation_execution.ip_first_octet,
                                emulation_execution.emulation_name,
                                emulation_execution_str))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("emulation execution saved successfully")
                return id_of_new_row

    @staticmethod
    def update_emulation_execution(emulation_execution: EmulationExecution, ip_first_octet: int,
                                   emulation: str) -> None:
        """
        Updates an emulation execution in the metastore

        :param emulation_execution: the emulation execution to update
        :param ip_first_octet: the first octet of the ip of the execution
        :param emulation: the emulation of the execution
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating emulation execution with ip first octet: {ip_first_octet} "
                                             f"and emulation: {emulation} "
                                             f"in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(emulation_execution.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE} "
                            f" SET info=%s "
                            f"WHERE {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE}.ip_first_octet = %s "
                            f"AND {constants.METADATA_STORE.EMULATION_EXECUTIONS_TABLE}.emulation_name = %s",
                            (config_json_str, ip_first_octet, emulation))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation execution with ip first octet: {ip_first_octet} "
                                                     f"and emulation: {emulation} "
                                                     f"updated successfully")

    @staticmethod
    def _convert_empirical_system_model_record_to_dto(empirical_system_model_record) -> \
            EmpiricalSystemModel:
        """
        Converts a empirical system model record fetched from the metastore into a DTO

        :param empirical_system_model_record: the record to convert
        :return: the DTO representing the record
        """
        empirical_system_model_config_json = json.dumps(empirical_system_model_record[1], indent=4, sort_keys=True,
                                                        cls=NpEncoder)
        empirical_system_model_config: EmpiricalSystemModel = \
            EmpiricalSystemModel.from_dict(json.loads(empirical_system_model_config_json))
        empirical_system_model_config.id = empirical_system_model_record[0]
        return empirical_system_model_config

    @staticmethod
    def list_empirical_system_models() -> List[EmpiricalSystemModel]:
        """
        :return: A list of empirical system models in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_empirical_system_model_record_to_dto(x), records))

    @staticmethod
    def list_empirical_system_models_ids() -> List[Tuple[int, str, int]]:
        """
        :return: A list of empirical system model ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,emulation_name,emulation_statistic_id FROM "
                            f"{constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1]), int(x[2])), records))

    @staticmethod
    def get_empirical_system_model_config(id: int) -> Union[None, EmpiricalSystemModel]:
        """
        Function for fetching an empirical system model config with a given id from the metastore

        :param id: the id of the empirical system model config
        :return: The empirical system model config or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_empirical_system_model_record_to_dto(
                        empirical_system_model_record=record)
                return record

    @staticmethod
    def save_empirical_system_model(empirical_system_model: EmpiricalSystemModel) -> Union[Any, int]:
        """
        Saves a empirical system model to the metastore

        :param empirical_system_model: the empirical system model to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Saving a empirical system model in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE)
                empirical_system_model_json = json.dumps(empirical_system_model.to_dict(), indent=4, sort_keys=True,
                                                         cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE} "
                            f"(id, model, emulation_name, emulation_statistic_id) "
                            f"VALUES (%s, %s, %s, %s) RETURNING id", (id, empirical_system_model_json,
                                                                      empirical_system_model.emulation_env_name,
                                                                      empirical_system_model.emulation_statistic_id))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("empirical system model saved successfully")
                return id_of_new_row

    @staticmethod
    def update_empirical_system_model(empirical_system_model: EmpiricalSystemModel, id: int) -> None:
        """
        Updates a empirical system model in the metastore

        :param empirical_system_model: the empirical system model to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating empirical system model with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(empirical_system_model.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE} "
                            f" SET config=%s "
                            f"WHERE {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Empirical system model with id: {id} updated successfully")

    @staticmethod
    def remove_empirical_system_model(empirical_system_model: EmpiricalSystemModel) -> None:
        """
        Removes a empirical system model from the metastore

        :param empirical_system_model: the to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing empirical system model with "
                                             f"id:{empirical_system_model.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMPIRICAL_SYSTEM_MODELS_TABLE} WHERE id = %s",
                            (empirical_system_model.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Empirical system model with "
                                                     f"id {empirical_system_model.id} deleted successfully")

    @staticmethod
    def _convert_mcmc_system_model_record_to_dto(mcmc_system_model_record) -> MCMCSystemModel:
        """
        Converts a MCMC system model record fetched from the metastore into a DTO

        :param mcmc_system_model_record: the record to convert
        :return: the DTO representing the record
        """
        mcmc_system_model_config_json = json.dumps(mcmc_system_model_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        mcmc_system_model_config: MCMCSystemModel = MCMCSystemModel.from_dict(json.loads(mcmc_system_model_config_json))
        mcmc_system_model_config.id = mcmc_system_model_record[0]
        return mcmc_system_model_config

    @staticmethod
    def list_mcmc_system_models() -> List[MCMCSystemModel]:
        """
        :return: A list of MCMC system models in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_mcmc_system_model_record_to_dto(x), records))

    @staticmethod
    def list_mcmc_system_models_ids() -> List[Tuple[int, str, int]]:
        """
        :return: A list of MCMC system model ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,emulation_name,emulation_statistic_id FROM "
                            f"{constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1]), int(x[2])), records))

    @staticmethod
    def get_mcmc_system_model_config(id: int) -> Union[None, MCMCSystemModel]:
        """
        Function for fetching a mcmc system model config with a given id from the metastore

        :param id: the id of the mcmc system model config
        :return: The mcmc system model config or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_mcmc_system_model_record_to_dto(mcmc_system_model_record=record)
                return record

    @staticmethod
    def save_mcmc_system_model(mcmc_system_model: MCMCSystemModel) -> Union[Any, int]:
        """
        Saves a mcmc system model to the metastore

        :param mcmc_system_model: the mcmc system model to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Saving a mcmc system model in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE)
                mcmc_system_model_json = json.dumps(mcmc_system_model.to_dict(),
                                                    indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE} "
                            f"(id, model, emulation_name, emulation_statistic_id) "
                            f"VALUES (%s, %s, %s, %s) RETURNING id", (id, mcmc_system_model_json,
                                                                      mcmc_system_model.emulation_env_name,
                                                                      mcmc_system_model.emulation_statistic_id))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("mcmc system model saved successfully")
                return id_of_new_row

    @staticmethod
    def update_mcmc_system_model(mcmc_system_model: MCMCSystemModel, id: int) -> None:
        """
        Updates a mcmc system model in the metastore

        :param mcmc_system_model: the mcmc system model to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating mcmc system model with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(mcmc_system_model.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE} "
                            f" SET config=%s "
                            f"WHERE {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"MCMC system model with id: {id} updated successfully")

    @staticmethod
    def remove_mcmc_system_model(mcmc_system_model: MCMCSystemModel) -> None:
        """
        Removes a MCMC system model from the metastore

        :param mcmc_system_model: the system model to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing MCMC system model with "
                                             f"id:{mcmc_system_model.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.MCMC_SYSTEM_MODELS_TABLE} WHERE id = %s",
                            (mcmc_system_model.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"MCMC system model with "
                                                     f"id {mcmc_system_model.id} deleted successfully")

    @staticmethod
    def _convert_gp_system_model_record_to_dto(gp_system_model_record) -> GPSystemModel:
        """
        Converts a gp system model record fetched from the metastore into a DTO

        :param gp_system_model_record: the record to convert
        :return: the DTO representing the record
        """
        gp_system_model_config_json = json.dumps(gp_system_model_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        gp_system_model_config: GPSystemModel = \
            GPSystemModel.from_dict(json.loads(gp_system_model_config_json))
        gp_system_model_config.id = gp_system_model_record[0]
        return gp_system_model_config

    @staticmethod
    def list_gp_system_models() -> List[GPSystemModel]:
        """
        :return: A list of gp system models in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_gp_system_model_record_to_dto(x), records))

    @staticmethod
    def list_gp_system_models_ids() -> List[Tuple[int, str, int]]:
        """
        :return: A list of gp system model ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,emulation_name,emulation_statistic_id FROM "
                            f"{constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1]), int(x[2])), records))

    @staticmethod
    def get_gp_system_model_config(id: int) -> Union[None, GPSystemModel]:
        """
        Function for fetching a gp system model config with a given id from the metastore

        :param id: the id of the gp system model config
        :return: The gp system model config or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_gp_system_model_record_to_dto(
                        gp_system_model_record=record)
                return record

    @staticmethod
    def save_gp_system_model(gp_system_model: GPSystemModel) -> Union[Any, int]:
        """
        Saves a gp system model to the metastore

        :param gp_system_model: the gp system model to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Saving a gp system model in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE)
                gp_system_model_json = json.dumps(gp_system_model.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE} "
                            f"(id, model, emulation_name, emulation_statistic_id) "
                            f"VALUES (%s, %s, %s, %s) RETURNING id", (id, gp_system_model_json,
                                                                      gp_system_model.emulation_env_name,
                                                                      gp_system_model.emulation_statistic_id))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("gp system model saved successfully")
                return id_of_new_row

    @staticmethod
    def update_gp_system_model(gp_system_model: GPSystemModel, id: int) -> None:
        """
        Updates a gp system model in the metastore

        :param gp_system_model: the gp system model to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating gp system model with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(gp_system_model.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE} "
                            f" SET config=%s "
                            f"WHERE {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"GP system model with id: {id} updated successfully")

    @staticmethod
    def remove_gp_system_model(gp_system_model: GPSystemModel) -> None:
        """
        Removes a gp system model from the metastore

        :param gp_system_model: the model to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing gp system model with "
                                             f"id:{gp_system_model.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.GP_SYSTEM_MODELS_TABLE} WHERE id = %s",
                            (gp_system_model.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"GP system model with "
                                                     f"id {gp_system_model.id} deleted successfully")

    @staticmethod
    def _convert_management_user_record_to_dto(management_user_record) -> ManagementUser:
        """
        Converts a management user record fetched from the metastore into a DTO

        :param management_user_record: the record to convert
        :return: the DTO representing the record
        """
        management_user = ManagementUser(username=management_user_record[1], password=management_user_record[2],
                                         email=management_user_record[3], first_name=management_user_record[4],
                                         last_name=management_user_record[5], organization=management_user_record[6],
                                         admin=management_user_record[7], salt=management_user_record[8])
        management_user.id = management_user_record[0]
        return management_user

    @staticmethod
    def list_management_users() -> List[ManagementUser]:
        """
        :return: A list of management users in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_management_user_record_to_dto(x), records))

    @staticmethod
    def list_management_users_ids() -> List[int]:
        """
        :return: A list of management user ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id FROM "
                            f"{constants.METADATA_STORE.MANAGEMENT_USERS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: int(x[0]), records))

    @staticmethod
    def get_management_user_config(id: int) -> Union[None, ManagementUser]:
        """
        Function for fetching a management user with a given id from the metastore

        :param id: the id of the management user
        :return: The management user or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_management_user_record_to_dto(
                        management_user_record=record)
                return record

    @staticmethod
    def save_management_user(management_user: ManagementUser) -> Union[None, int]:
        """
        Saves a management user to the metastore

        :param management_user: the management user to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Saving a management user in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.MANAGEMENT_USERS_TABLE)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} "
                            f"(id, username, password, email, first_name, last_name, organization, admin, salt) "
                            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                            (id, management_user.username, management_user.password, management_user.email,
                             management_user.first_name, management_user.last_name, management_user.organization,
                             management_user.admin, management_user.salt))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("management user saved successfully")
                return id_of_new_row

    @staticmethod
    def update_management_user(management_user: ManagementUser, id: int) -> None:
        """
        Updates a management user in the metastore

        :param management_user: the management user to update
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating management user with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} "
                            f" SET username=%s, password=%s, email=%s, first_name=%s, last_name=%s, organization=%s, "
                            f"admin=%s, salt=%s WHERE {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE}.id = %s",
                            (management_user.username, management_user.password, management_user.email,
                             management_user.first_name, management_user.last_name, management_user.organization,
                             management_user.admin, management_user.salt, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Management user with id: {id} updated successfully")

    @staticmethod
    def remove_management_user(management_user: ManagementUser) -> None:
        """
        Removes a management user from the metastore

        :param management_user: the user to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing management user with "
                                             f"id:{management_user.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} WHERE id = %s",
                            (management_user.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Management user with "
                                                     f"id {management_user.id} deleted successfully")

    @staticmethod
    def get_management_user_by_username(username: str) -> Union[None, ManagementUser]:
        """
        Function for extracting a management user account based on the username

        :param username: the username of the user
        :return: The management user or None if no user with the given username was found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.MANAGEMENT_USERS_TABLE} "
                            f"WHERE username = %s", (username,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_management_user_record_to_dto(management_user_record=record)
                return record

    @staticmethod
    def _convert_session_token_record_to_dto(session_token_record) -> SessionToken:
        """
        Converts a session token record fetched from the metastore into a DTO

        :param session_token_record: the record to convert
        :return: the DTO representing the record
        """
        session_token = SessionToken(token=session_token_record[0], timestamp=session_token_record[1],
                                     username=session_token_record[2])
        return session_token

    @staticmethod
    def list_session_tokens() -> List[SessionToken]:
        """
        :return: A list of session tokens in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SESSION_TOKENS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_session_token_record_to_dto(x), records))

    @staticmethod
    def get_session_token_metadata(token: str) -> Union[None, SessionToken]:
        """
        Function for fetching the metadata of a given session token

        :param token: the token to lookup the metadata dor
        :return: The session token and its metadata or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SESSION_TOKENS_TABLE} "
                            f"WHERE token = %s", (token,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_session_token_record_to_dto(
                        session_token_record=record)
                return record

    @staticmethod
    def save_session_token(session_token: SessionToken) -> Union[None, str]:
        """
        Saves a session token to the metastore

        :param session_token: the session token to save
        :return: token of the created record
        """
        ts = time.time()
        Logger.__call__().get_logger().debug("Saving a session token in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.SESSION_TOKENS_TABLE} "
                                f"(token, timestamp, username) "
                                f"VALUES (%s, %s, %s) RETURNING token",
                                (session_token.token, ts, session_token.username))
                    record = cur.fetchone()
                    token_of_new_row = None
                    if record is not None:
                        token_of_new_row = record[0]
                    conn.commit()
                    Logger.__call__().get_logger().debug("Session token saved successfully")
                    return token_of_new_row
                except Exception as e:
                    Logger.__call__().get_logger().error(f"Could not save session token to database, error: {str(e)}, "
                                                         f"{repr(e)}")
                    return None

    @staticmethod
    def update_session_token(session_token: SessionToken, token: str) -> None:
        """
        Updates a session token in the metastore

        :param session_token: the session token to update
        :param token: the token of the row to update
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Updating session token with token: {token} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.SESSION_TOKENS_TABLE} "
                            f" SET token=%s, timestamp=%s, username=%s "
                            f"WHERE {constants.METADATA_STORE.SESSION_TOKENS_TABLE}.token = %s",
                            (session_token.token, session_token.timestamp, session_token.username,
                             token))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Session token {token} updated successfully")

    @staticmethod
    def remove_session_token(session_token: SessionToken) -> None:
        """
        Removes a session token from the metastore

        :param session_token: the session token to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing session token with "
                                             f"token:{session_token.token} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.SESSION_TOKENS_TABLE} WHERE token = %s",
                            (session_token.token,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Session token with "
                                                     f"token {session_token.token} deleted successfully")

    @staticmethod
    def get_session_token_by_username(username: str) -> Union[None, SessionToken]:
        """
        Function for extracting a session token account based on the username

        :param username: the username of the user
        :return: The session token or None if no user with the given username was found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SESSION_TOKENS_TABLE} "
                            f"WHERE username = %s", (username,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_session_token_record_to_dto(session_token_record=record)
                return record

    @staticmethod
    def _convert_traces_dataset_record_to_dto(traces_dataset_record) -> TracesDataset:
        """
        Converts a traces dataset record fetched from the metastore into a DTO

        :param traces_dataset_record: the record to convert
        :return: the DTO representing the record
        """
        data_schema = {}
        if traces_dataset_record[3] is not None and traces_dataset_record[3] != "":
            data_schema_json_str = json.dumps(traces_dataset_record[3], indent=4, sort_keys=True, cls=NpEncoder)
            data_schema = json.loads(data_schema_json_str)
        traces_dataset = TracesDataset(name=traces_dataset_record[1], description=traces_dataset_record[2],
                                       data_schema=data_schema, download_count=traces_dataset_record[4],
                                       file_path=traces_dataset_record[5], url=traces_dataset_record[6],
                                       date_added=traces_dataset_record[7], num_traces=traces_dataset_record[8],
                                       num_attributes_per_time_step=traces_dataset_record[9],
                                       size_in_gb=traces_dataset_record[10],
                                       compressed_size_in_gb=traces_dataset_record[11],
                                       citation=traces_dataset_record[12], num_files=traces_dataset_record[13],
                                       file_format=traces_dataset_record[14], added_by=traces_dataset_record[15],
                                       columns=traces_dataset_record[16])
        traces_dataset.id = traces_dataset_record[0]
        return traces_dataset

    @staticmethod
    def list_traces_datasets_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of traces datasets ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,name FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def list_traces_datasets() -> List[TracesDataset]:
        """
        :return: A list of traces datasets in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_traces_dataset_record_to_dto(x), records))

    @staticmethod
    def get_traces_dataset_metadata(id: int) -> Union[None, TracesDataset]:
        """
        Function for fetching the metadata of a given dataset name

        :param id: the id of the dataset to get the metadata of
        :return: The traces dataset and its metadata or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_traces_dataset_record_to_dto(
                        traces_dataset_record=record)
                return record

    @staticmethod
    def get_traces_dataset_metadata_by_name(dataset_name: str) -> Union[None, TracesDataset]:
        """
        Function for fetching the metadata of a given dataset name

        :param dataset_name: the dataset name to lookup the metadata for
        :return: The traces dataset and its metadata or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE} "
                            f"WHERE name = %s", (dataset_name,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_traces_dataset_record_to_dto(
                        traces_dataset_record=record)
                return record

    @staticmethod
    def save_traces_dataset(traces_dataset: TracesDataset) -> Union[Any, int]:
        """
        Saves a traces dataset to the metastore

        :param traces_dataset: the traces dataset to save
        :return: idg of the created record
        """
        Logger.__call__().get_logger().debug("Saving a traces dataset in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                schema_json_str = ""
                if traces_dataset.data_schema is not None:
                    schema_json_str = json.dumps(traces_dataset.data_schema, indent=4, sort_keys=True, cls=NpEncoder)
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.TRACES_DATASETS_TABLE)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.TRACES_DATASETS_TABLE} "
                            f"(id, name, description, data_schema, download_count, "
                            f"file_path, url, date_added, num_traces, "
                            f"num_attributes_per_time_step, size_in_gb, compressed_size_in_gb, citation, num_files, "
                            f"file_format, added_by, columns) "
                            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                            (id, traces_dataset.name, traces_dataset.description, schema_json_str,
                             traces_dataset.download_count, traces_dataset.file_path, traces_dataset.url,
                             traces_dataset.date_added, traces_dataset.num_traces,
                             traces_dataset.num_attributes_per_time_step,
                             traces_dataset.size_in_gb, traces_dataset.compressed_size_in_gb,
                             traces_dataset.citation, traces_dataset.num_files, traces_dataset.file_format,
                             traces_dataset.added_by, traces_dataset.columns))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("traces dataset saved successfully")
                return id_of_new_row

    @staticmethod
    def update_traces_dataset(traces_dataset: TracesDataset, id: int) -> None:
        """
        Updates a traces dataset in the metastore

        :param traces_dataset: the traces dataset to update
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating traces dataset with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                schema_json_str = ""
                if traces_dataset.data_schema is not None:
                    schema_json_str = json.dumps(traces_dataset.data_schema, indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.TRACES_DATASETS_TABLE} "
                            f" SET name=%s, description=%s, data_schema=%s, download_count=%s, file_path=%s, "
                            f"url=%s, date_added=%s, num_traces=%s, num_attributes_per_time_step=%s, size_in_gb=%s, "
                            f"compressed_size_in_gb=%s, citation=%s, num_files=%s, file_format=%s, added_by=%s, "
                            f"columns=%s "
                            f"WHERE {constants.METADATA_STORE.TRACES_DATASETS_TABLE}.id = %s",
                            (traces_dataset.name, traces_dataset.description, schema_json_str,
                             traces_dataset.download_count, traces_dataset.file_path, traces_dataset.url,
                             traces_dataset.date_added, traces_dataset.num_traces,
                             traces_dataset.num_attributes_per_time_step, traces_dataset.size_in_gb,
                             traces_dataset.compressed_size_in_gb, traces_dataset.citation,
                             traces_dataset.num_files, traces_dataset.file_format, traces_dataset.added_by,
                             traces_dataset.columns, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Traces dataset with {id} updated successfully")

    @staticmethod
    def remove_traces_dataset(traces_dataset: TracesDataset) -> None:
        """
        Removes a traces dataset from the metastore

        :param traces_dataset: the traces dataset to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing traces dataset with "
                                             f"id:{traces_dataset.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.TRACES_DATASETS_TABLE} WHERE id = %s",
                            (traces_dataset.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Traces dataset with "
                                                     f"id {traces_dataset.id} deleted successfully")

    @staticmethod
    def _convert_statistics_dataset_record_to_dto(statistics_dataset_record) -> StatisticsDataset:
        """
        Converts a statistics dataset record fetched from the metastore into a DTO

        :param statistics_dataset_record: the record to convert
        :return: the DTO representing the record
        """
        statistics_dataset = StatisticsDataset(
            name=statistics_dataset_record[1], description=statistics_dataset_record[2],
            download_count=statistics_dataset_record[3],
            file_path=statistics_dataset_record[4], url=statistics_dataset_record[5],
            date_added=statistics_dataset_record[6], num_measurements=statistics_dataset_record[7],
            num_metrics=statistics_dataset_record[8], size_in_gb=statistics_dataset_record[9],
            compressed_size_in_gb=statistics_dataset_record[10],
            citation=statistics_dataset_record[11], num_files=statistics_dataset_record[12],
            file_format=statistics_dataset_record[13], added_by=statistics_dataset_record[14],
            conditions=statistics_dataset_record[15], metrics=statistics_dataset_record[16],
            num_conditions=statistics_dataset_record[17])
        statistics_dataset.id = statistics_dataset_record[0]
        return statistics_dataset

    @staticmethod
    def list_statistics_datasets_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of statistics datasets ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,name FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def list_statistics_datasets() -> List[StatisticsDataset]:
        """
        :return: A list of statistics datasets in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_statistics_dataset_record_to_dto(x), records))

    @staticmethod
    def get_statistics_dataset_metadata(id: int) -> Union[None, StatisticsDataset]:
        """
        Function for fetching the metadata of a given dataset name

        :param id: the id of the dataset to get the metadata of
        :return: The statistics dataset and its metadata or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_statistics_dataset_record_to_dto(
                        statistics_dataset_record=record)
                return record

    @staticmethod
    def get_statistics_dataset_metadata_by_name(dataset_name: str) -> Union[None, StatisticsDataset]:
        """
        Function for fetching the metadata of a given dataset name

        :param dataset_name: the dataset name to lookup the metadata for
        :return: The statistics dataset and its metadata or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE} "
                            f"WHERE name = %s", (dataset_name,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_statistics_dataset_record_to_dto(
                        statistics_dataset_record=record)
                return record

    @staticmethod
    def save_statistics_dataset(statistics_dataset: StatisticsDataset) -> Union[Any, int]:
        """
        Saves a statistics dataset to the metastore

        :param statistics_dataset: the statistics dataset to save
        :return: idg of the created record
        """
        Logger.__call__().get_logger().debug("Saving a statistics dataset in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.STATISTICS_DATASETS_TABLE)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE} "
                            f"(id, name, description, download_count, file_path, url, date_added, num_measurements, "
                            f"num_metrics, size_in_gb, compressed_size_in_gb, citation, num_files, "
                            f"file_format, added_by, conditions, metrics, num_conditions) "
                            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                            f"RETURNING id",
                            (id, statistics_dataset.name, statistics_dataset.description,
                             statistics_dataset.download_count, statistics_dataset.file_path, statistics_dataset.url,
                             statistics_dataset.date_added, statistics_dataset.num_measurements,
                             statistics_dataset.num_metrics,
                             statistics_dataset.size_in_gb, statistics_dataset.compressed_size_in_gb,
                             statistics_dataset.citation, statistics_dataset.num_files, statistics_dataset.file_format,
                             statistics_dataset.added_by, statistics_dataset.conditions, statistics_dataset.metrics,
                             statistics_dataset.num_conditions))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("statistics dataset saved successfully")
                return id_of_new_row

    @staticmethod
    def update_statistics_dataset(statistics_dataset: StatisticsDataset, id: int) -> None:
        """
        Updates a statistics dataset in the metastore

        :param statistics_dataset: the statistics dataset to update
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating statistics dataset with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.STATISTICS_DATASETS_TABLE} "
                            f" SET name=%s, description=%s, download_count=%s, file_path=%s, "
                            f"url=%s, date_added=%s, num_measurements=%s, num_metrics=%s, size_in_gb=%s, "
                            f"compressed_size_in_gb=%s, citation=%s, num_files=%s, file_format=%s, added_by=%s, "
                            f"conditions=%s, metrics=%s, num_conditions=%s "
                            f"WHERE {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE}.id = %s",
                            (statistics_dataset.name, statistics_dataset.description,
                             statistics_dataset.download_count, statistics_dataset.file_path, statistics_dataset.url,
                             statistics_dataset.date_added, statistics_dataset.num_measurements,
                             statistics_dataset.num_metrics, statistics_dataset.size_in_gb,
                             statistics_dataset.compressed_size_in_gb, statistics_dataset.citation,
                             statistics_dataset.num_files, statistics_dataset.file_format, statistics_dataset.added_by,
                             statistics_dataset.conditions, statistics_dataset.metrics,
                             statistics_dataset.num_conditions, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Statistics dataset with {id} updated successfully")

    @staticmethod
    def remove_statistics_dataset(statistics_dataset: StatisticsDataset) -> None:
        """
        Removes a statistics dataset from the metastore

        :param statistics_dataset: the statistic dataset to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing statistics dataset with "
                                             f"id:{statistics_dataset.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.STATISTICS_DATASETS_TABLE} WHERE id = %s",
                            (statistics_dataset.id,))
                conn.commit()
                Logger.__call__().get_logger().debug("Statistics dataset with "
                                                     f"id {statistics_dataset.id} deleted successfully")

    @staticmethod
    def _convert_config_record_to_dto(config_record) -> Config:
        """
        Converts a config record fetched from the metastore into a DTO

        :param config_record: the record to convert
        :return: the DTO representing the record
        """
        config_json = json.dumps(config_record[1], indent=4, sort_keys=True, cls=NpEncoder)
        config: Config = Config.from_dict(json.loads(config_json))
        config.id = config_record[0]
        return config

    @staticmethod
    def list_configs() -> List[Config]:
        """
        :return: A list of configs in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.CONFIG_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: MetastoreFacade._convert_config_record_to_dto(x), records))

    @staticmethod
    def list_config_ids() -> List[int]:
        """
        :return: A list of config ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id FROM {constants.METADATA_STORE.CONFIG_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: int(x[0]), records))

    @staticmethod
    def get_config(id: int) -> Union[None, Config]:
        """
        Function for fetching the config with a given id from the metastore

        :param id: the id of the config
        :return: The config or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.CONFIG_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_config_record_to_dto(config_record=record)
                return record

    @staticmethod
    def save_config(config: Config) -> Union[Any, int]:
        """
        Saves a config to the metastore

        :param config: the config to save
        :return: id of the config
        """
        Logger.__call__().get_logger().info("Updating the configuration in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json = json.dumps(config.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.CONFIG_TABLE} "
                            f"(id, config) "
                            f"VALUES (%s, %s) RETURNING id", (1, config_json,))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("config saved successfully")
                return id_of_new_row

    @staticmethod
    def update_config(config: Config, id: int) -> None:
        """
        Updates a config in the metastore

        :param config: the config to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating config with id: {id} in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(config.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.CONFIG_TABLE} "
                            f" SET config=%s "
                            f"WHERE {constants.METADATA_STORE.CONFIG_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Config with id: {id} updated successfully")

    @staticmethod
    def remove_config(config: Config) -> None:
        """
        Removes a config from the metastore

        :param config: the config to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing config with "
                                             f"id:{config.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.CONFIG_TABLE} WHERE id = %s", (config.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Config with "
                                                     f"id {config.id} deleted successfully")

    @staticmethod
    def list_linear_threshold_stopping_policies() -> List[LinearThresholdStoppingPolicy]:
        """
        :return: A list of Linear-threshold stopping policies in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(
                    lambda x: MetastoreFacade._convert_linear_threshold_stopping_policy_record_to_dto(x), records))

    @staticmethod
    def list_linear_threshold_stopping_policies_ids() -> List[Tuple[int, str]]:
        """
        :return: A list of Linear-threshold stopping policies ids in the metastore
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id,simulation_name FROM "
                            f"{constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE}")
                records = cur.fetchall()
                return list(map(lambda x: (int(x[0]), str(x[1])), records))

    @staticmethod
    def _convert_linear_threshold_stopping_policy_record_to_dto(linear_threshold_stopping_policy_record) \
            -> LinearThresholdStoppingPolicy:
        """
        Converts a Linear-threshold stopping policy record fetched from the metastore into a DTO

        :param linear_threshold_stopping_policy_record: the record to convert
        :return: the DTO representing the record
        """
        linear_threshold_stopping_policy_json = json.dumps(linear_threshold_stopping_policy_record[1], indent=4,
                                                           sort_keys=True, cls=NpEncoder)
        linear_threshold_stopping_policy: LinearThresholdStoppingPolicy = LinearThresholdStoppingPolicy.from_dict(
            json.loads(linear_threshold_stopping_policy_json))
        linear_threshold_stopping_policy.id = linear_threshold_stopping_policy_record[0]
        return linear_threshold_stopping_policy

    @staticmethod
    def get_linear_threshold_stopping_policy(id: int) -> Union[None, LinearThresholdStoppingPolicy]:
        """
        Function for fetching a mult-threshold policy with a given id from the metastore

        :param id: the id of the linear-threshold policy
        :return: The mult-threshold policy or None if it could not be found
        """
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_linear_threshold_stopping_policy_record_to_dto(
                        linear_threshold_stopping_policy_record=record)
                return record

    @staticmethod
    def remove_linear_threshold_stopping_policy(
            linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) -> None:
        """
        Removes a linear-threshold stopping policy from the metastore

        :param linear_threshold_stopping_policy: the policy to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing Linear-threshold stopping policy with "
                                             f"id:{linear_threshold_stopping_policy.id} from the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE} "
                            f"WHERE id = %s",
                            (linear_threshold_stopping_policy.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Linear-threshold stopping policy "
                                                     f"with id {linear_threshold_stopping_policy.id} "
                                                     f"deleted successfully")

    @staticmethod
    def save_linear_threshold_stopping_policy(linear_threshold_stopping_policy: LinearThresholdStoppingPolicy) \
            -> Union[Any, int]:
        """
        Saves a linear-threshold stopping policy to the metastore

        :param linear_threshold_stopping_policy: the policy to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug("Installing a linear-threshold stopping policy in the metastore")
        with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                             f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                             f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                             f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                # Need to manually set the ID since CITUS does not handle serial columns
                # on distributed tables properly
                id = GeneralUtil.get_latest_table_id(
                    cur=cur, table_name=constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE)
                policy_json_str = json.dumps(linear_threshold_stopping_policy.to_dict(), indent=4, sort_keys=True,
                                             cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.LINEAR_THRESHOLD_STOPPING_POLICIES_TABLE} "
                            f"(id, policy, simulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (id, policy_json_str,
                                                                  linear_threshold_stopping_policy.simulation_name))
                record = cur.fetchone()
                id_of_new_row = None
                if record is not None:
                    id_of_new_row = int(record[0])
                conn.commit()
                Logger.__call__().get_logger().debug("Linear-threshold policy saved successfully")
                return id_of_new_row
