from typing import List, Union, Any, Tuple
import psycopg
import json
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
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.util.np_encoder import NpEncoder
from csle_common.dao.training.ppo_policy import PPOPolicy


class MetastoreFacade:
    """
    Facade for the metastore, contains methods for querying the metastore
    """

    @staticmethod
    def list_emulations() -> List[EmulationEnvConfig]:
        """
        :return: A list of emulations in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_emulation_record_to_dto(x), records))
                return records

    @staticmethod
    def get_emulation(name: str) -> Union[None, EmulationEnvConfig]:
        """
        Function for extracting the metadata of an emulation with a given name

        :param name: the name of the emulation
        :return: The emulation config or None if the emulation was not found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s", (name,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_record_to_dto(emulation_record=record)
                return record

    @staticmethod
    def list_simulations() -> List[SimulationEnvConfig]:
        """
        :return: A list of simulations in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATIONS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_simulation_record_to_dto(x), records))
                return records

    @staticmethod
    def get_simulation(name: str) -> Union[None, SimulationEnvConfig]:
        """
        Function for extracting the metadata of a simulation with a given name

        :param name: the name of the simulation
        :return: The simulation config or None if the simulation was not found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATIONS_TABLE} WHERE name = %s", (name,))
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
        emulation_config_json_str = json.dumps(emulation_record[2], indent=4, sort_keys=True)
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
        simulation_config_json_str = json.dumps(simulation_record[3], indent=4, sort_keys=True)
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
        emulation_trace_json_str = json.dumps(emulation_trace_record[2], indent=4, sort_keys=True)
        emulation_trace: EmulationTrace = EmulationTrace.from_dict(json.loads(emulation_trace_json_str))
        emulation_trace.id = emulation_trace_record[0]
        return emulation_trace

    @staticmethod
    def _convert_emulation_simulation_trace_record_to_dto(emulation_simulation_trace_record) -> EmulationSimulationTrace:
        """
        Converts an emulation-simulkation trace record fetched from the metastore into a DTO

        :param emulation_simulation_trace_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_simulation_trace_json_str = json.dumps(emulation_simulation_trace_record[2], indent=4,
                                                         sort_keys=True)
        emulation_simulation_trace: EmulationSimulationTrace = \
            EmulationSimulationTrace.from_dict(json.loads(emulation_simulation_trace_json_str))
        return emulation_simulation_trace

    @staticmethod
    def _convert_simulation_trace_record_to_dto(simulation_trace_record) -> SimulationTrace:
        """
        Converts an emulation trace record fetched from the metastore into a DTO

        :param simulation_trace_record: the record to convert
        :return: the DTO representing the record
        """
        simulation_trace_json_str = json.dumps(simulation_trace_record[2], indent=4, sort_keys=True)
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
        emulation_statistics_json_str = json.dumps(emulation_statistics_record[2], indent=4, sort_keys=True)
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
    def install_emulation(config: EmulationEnvConfig) -> Union[Any, int]:
        """
        Installs the emulation configuration in the metastore

        :param config: the config to install
        :return: id of the created row
        """
        Logger.__call__().get_logger().debug(f"Installing emulation:{config.name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    config_json_str = json.dumps(config.to_dict(), indent=4, sort_keys=True)
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATIONS_TABLE} (name, config) "
                                f"VALUES (%s, %s) RETURNING id", (config.name, config_json_str))
                    id_of_new_row = cur.fetchone()[0]
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Emulation {config.name} installed successfully")
                    return id_of_new_row
                except psycopg.errors.UniqueViolation as e:
                    Logger.__call__().get_logger().debug(f"Emulation {config.name} is already installed")

    @staticmethod
    def uninstall_emulation(config: EmulationEnvConfig) -> None:
        """
        Uninstalls the emulation configuration in the metastore

        :param config: the config to uninstall
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Uninstalling emulation:{config.name} from the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s", (config.name,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation {config.name} uninstalled successfully")


    @staticmethod
    def install_simulation(config: SimulationEnvConfig) -> Union[Any, int]:
        """
        Installs the simulation configuration in the metastore

        :param config: the config to install
        :return: id of the created row
        """
        Logger.__call__().get_logger().debug(f"Installing simulation:{config.name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    config_json_str = json.dumps(config.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.SIMULATIONS_TABLE} "
                                f"(name, emulation_statistic_id, config) "
                                f"VALUES (%s, %s, %s) RETURNING id", (config.name, config.emulation_statistic_id,
                                                                      config_json_str))
                    id_of_new_row = cur.fetchone()[0]
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Simulation {config.name} installed successfully")
                    return id_of_new_row
                except psycopg.errors.UniqueViolation as e:
                    Logger.__call__().get_logger().debug(f"Simulation {config.name} is already installed")

    @staticmethod
    def uninstall_simulation(config: SimulationEnvConfig) -> None:
        """
        Uninstalls the simulation configuration in the metastore

        :param config: the config to uninstall
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Uninstalling simulation:{config.name} from the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(emulation_trace.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATION_TRACES_TABLE} (emulation_name, trace) "
                            f"VALUES (%s, %s) RETURNING id", (emulation_trace.emulation_name, config_json_str))
                id_of_new_row = cur.fetchone()[0]
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(emulation_statistics.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO "
                            f"{constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
                            f"(emulation_name, statistics) "
                            f"VALUES (%s, %s) RETURNING id", (emulation_statistics.emulation_name, config_json_str))
                id_of_new_row = cur.fetchone()[0]
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(emulation_statistics.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.EMULATION_STATISTICS_TABLE} "
                            f" SET statistics=%s "
                            f"WHERE {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Statistics for emulation "
                                                     f"{emulation_statistics.emulation_name} with id {id} "
                                                     f"updated successfully")

    @staticmethod
    def list_emulation_statistics() -> List[EmulationStatistics]:
        """
        :return: A list of emulation statistics in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_STATISTICS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_emulation_statistics_record_to_dto(x), records))
                return records

    @staticmethod
    def list_emulation_traces() -> List[EmulationTrace]:
        """
        :return: A list of emulation traces in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_emulation_trace_record_to_dto(x), records))
                return records

    @staticmethod
    def list_simulation_traces() -> List[SimulationTrace]:
        """
        :return: A list of simulation traces in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_simulation_trace_record_to_dto(x), records))
                return records

    @staticmethod
    def remove_simulation_trace(simulation_trace: SimulationTrace) -> None:
        """
        Removes a simulation trace from the metastore

        :param simulation_trace: the simulation trace to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing simulation traec with "
                                             f"id:{simulation_trace.id} from the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATION_TRACES_TABLE} WHERE id = %s",
                            (emulation_trace.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Emulation trace "
                                                     f"with id {emulation_trace.id} deleted successfully")

    @staticmethod
    def get_emulation_statistic(id: int) -> Union[None, EmulationStatistics]:
        """
        Function for fetching an emulation satistic with a given id from the metastore

        :param id: the id of the statistics
        :return: The emulation statistic or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(simulation_trace.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.SIMULATION_TRACES_TABLE} (gym_env, trace) "
                            f"VALUES (%s, %s) RETURNING id", (simulation_trace.simulation_env, config_json_str))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"Simulation trace for "
                                                     f"env {simulation_trace.simulation_env} "
                                                     f"saved successfully")
                return id_of_new_row

    @staticmethod
    def save_emulation_simulation_trace(emulation_simulation_trace: EmulationSimulationTrace) -> None:
        """
        Saves an emulation_simulation trace

        :param emulation_simulation_trace: the emulation trace to save
        :return: None
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"INSERT INTO "
                            f"{constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE} "
                            f"(emulation_trace, simulation_trace) "
                            f"VALUES (%s, %s) RETURNING id", (emulation_trace_id, simulation_trace_id))
                conn.commit()
                Logger.__call__().get_logger().debug(
                    f"Emulation-Simulation trace for "
                    f"emulation {emulation_simulation_trace.emulation_trace.emulation_name} "
                    f"and simulation: {emulation_simulation_trace.simulation_trace.simulation_env} saved successfully")

    @staticmethod
    def list_emulation_simulation_traces() -> List[EmulationSimulationTrace]:
        """
        :return: A list of emulation-simulation traces in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_emulation_simulation_trace_record_to_dto(x),
                                   records))
                return records

    @staticmethod
    def get_emulation_simulation_trace(id: int) -> Union[None, EmulationSimulationTrace]:
        """
        Function for fetching a simulation trace with a given id from the metastore

        :param id: the id of the emulation-simulation trace
        :return: The emulation-simulation trace or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_emulation_simulation_trace_record_to_dto(
                        emulation_simulation_trace_record=record)
                return record


    @staticmethod
    def save_emulation_image(img: bytes, emulation_name: str) -> Union[Any, int]:
        """
        Saves the image of an emulation in the metastore

        :param img: the image data to save
        :param emulation_name: the name of the emulation
        :return: id of the created row
        """
        Logger.__call__().get_logger().debug(f"Saving image for emulation:{emulation_name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATION_IMAGES_TABLE} (emulation_name, image) "
                                f"VALUES (%s, %s) RETURNING id", (emulation_name, img))
                    id_of_new_row = cur.fetchone()[0]
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Saved image for emulation {emulation_name} successfully")
                    return id_of_new_row
                except Exception as e:
                    Logger.__call__().get_logger().warning(f"There was an error saving an image "
                                                         f"for emulation {emulation_name}")

    @staticmethod
    def list_emulation_images() -> List[Tuple[str, bytes]]:
        """
        :return: A list of emulation names and images in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EMULATION_IMAGES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_emulation_image_record_to_tuple(x), records))
                return records


    @staticmethod
    def get_emulation_image(emulation_name : str) -> Union[None, Tuple[str, bytes]]:
        """
        Function for fetching the image of a given emulation

        :param emulation_name: the name of the emulatin to fetch the image for
        :return: The simulation trace or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.SIMULATION_IMAGES_TABLE} (simulation_name, image) "
                                f"VALUES (%s, %s) RETURNING id", (simulation_name, img))
                    id_of_new_row = cur.fetchone()[0]
                    conn.commit()
                    Logger.__call__().get_logger().debug(f"Saved image for simulation {simulation_name} successfully")
                    return id_of_new_row
                except Exception as e:
                    Logger.__call__().get_logger().warning(f"There was an error saving an image "
                                                           f"for simulation {simulation_name}")

    @staticmethod
    def list_simulation_images() -> List[Tuple[str, bytes]]:
        """
        :return: A list of simulation names and images in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SIMULATION_IMAGES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_simulation_image_record_to_tuple(x), records))
                return records


    @staticmethod
    def get_simulation_image(simulation_name : str) -> Union[None, Tuple[str, bytes]]:
        """
        Function for fetching the image of a given simulation

        :param simulation_name: the name of the simulation to fetch the image for
        :return: The simulation trace or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(experiment_execution.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} "
                            f"(execution, simulation_name, emulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (config_json_str, experiment_execution.simulation_name,
                                                              experiment_execution.emulation_name))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"Experiment execution for "
                                                     f"emulation {experiment_execution.emulation_name} "
                                                     f"and simulation {experiment_execution.simulation_name} "
                                                     f"saved successfully")
                return id_of_new_row

    @staticmethod
    def list_experiment_executions() -> List[EmulationTrace]:
        """
        :return: A list of emulation traces in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_experiment_execution_record_to_dto(x), records))
                return records

    @staticmethod
    def _convert_experiment_execution_record_to_dto(experiment_execution_record) -> ExperimentExecution:
        """
        Converts an experiment execution record fetched from the metastore into a DTO

        :param experiment_execution_record: the record to convert
        :return: the DTO representing the record
        """
        experiment_execution_json = json.dumps(experiment_execution_record[1], indent=4, sort_keys=True)
        experiment_execution: ExperimentExecution = ExperimentExecution.from_dict(json.loads(experiment_execution_json))
        experiment_execution.id = experiment_execution_record[0]
        return experiment_execution

    @staticmethod
    def get_experiment_execution(id: int) -> Union[None, EmulationTrace]:
        """
        Function for fetching an experiment execution with a given id from the metastore

        :param id: the id of the emulation trace
        :return: The emulation trace or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.EXPERIMENT_EXECUTIONS_TABLE} WHERE id = %s", (id,))
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_multi_threshold_stopping_policy_record_to_dto(x), records))
                return records


    @staticmethod
    def _convert_multi_threshold_stopping_policy_record_to_dto(multi_threshold_stopping_policy_record) \
            -> MultiThresholdStoppingPolicy:
        """
        Converts a Multi-threshold stopping policy record fetched from the metastore into a DTO

        :param multi_threshold_stopping_policy_record: the record to convert
        :return: the DTO representing the record
        """
        multi_threshold_stopping_policy_json = json.dumps(multi_threshold_stopping_policy_record[1], indent=4, sort_keys=True)
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE} "
                            f"WHERE id = %s",
                            (multi_threshold_stopping_policy.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Multi-threshold stopping policy "
                                                     f"with id {multi_threshold_stopping_policy.id} deleted successfully")

    @staticmethod
    def save_multi_threshold_stopping_policy(multi_threshold_stopping_policy: MultiThresholdStoppingPolicy) \
            -> Union[Any, int]:
        """
        Saves a multi-threshold stopping policy to the metastore

        :param multi_threshold_stopping_policy: the policy to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Installing a multi-threshold stopping policy in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                policy_json_str = json.dumps(multi_threshold_stopping_policy.to_dict(), indent=4, sort_keys=True)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.MULTI_THRESHOLD_STOPPING_POLICIES_TABLE} "
                            f"(policy, simulation_name) "
                            f"VALUES (%s, %s) RETURNING id", (policy_json_str,
                                                              multi_threshold_stopping_policy.simulation_name))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"Multi-threshold policy saved successfully")
                return id_of_new_row

    @staticmethod
    def _convert_training_job_record_to_dto(training_job_record) -> TrainingJobConfig:
        """
        Converts a training job record fetched from the metastore into a DTO

        :param training_job_record: the record to convert
        :return: the DTO representing the record
        """
        tranining_job_config_json = json.dumps(training_job_record[1], indent=4, sort_keys=True)
        training_job_config: TrainingJobConfig = TrainingJobConfig.from_dict(json.loads(tranining_job_config_json))
        training_job_config.id = training_job_record[0]
        return training_job_config

    @staticmethod
    def list_training_jobs() -> List[TrainingJobConfig]:
        """
        :return: A list of training jobs in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TRAINING_JOBS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_training_job_record_to_dto(x), records))
                return records


    @staticmethod
    def get_training_job_config(id: int) -> Union[None, TrainingJobConfig]:
        """
        Function for fetching a training job config with a given id from the metastore

        :param id: the id of the training job config
        :return: The trainign job config or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        Logger.__call__().get_logger().debug(f"Saving a training job in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                training_job_str = json.dumps(training_job.to_dict(), indent=4, sort_keys=True)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.TRAINING_JOBS_TABLE} "
                            f"(config, simulation_name, emulation_name) "
                            f"VALUES (%s, %s, %s) RETURNING id", (training_job_str, training_job.simulation_env_name,
                                                              training_job.emulation_env_name))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"Training job saved successfully")
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
                                                     sort_keys=True)
        data_collection_job_config: DataCollectionJobConfig = \
            DataCollectionJobConfig.from_dict(json.loads(data_collection_job_config_json))
        data_collection_job_config.id = data_collection_job_record[0]
        return data_collection_job_config

    @staticmethod
    def list_data_collection_jobs() -> List[DataCollectionJobConfig]:
        """
        :return: A list of data collection jobs in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_data_collection_job_record_to_dto(x),
                                   records))
                return records

    @staticmethod
    def get_data_collection_job_config(id: int) -> Union[None, DataCollectionJobConfig]:
        """
        Function for fetching a data collection job config with a given id from the metastore

        :param id: the id of the data collection job config
        :return: The data collection job config or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        Logger.__call__().get_logger().debug(f"Saving a data collection job in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                data_collection_job_json = json.dumps(data_collection_job.to_dict(), indent=4,
                                                            sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.DATA_COLLECTION_JOBS_TABLE} "
                            f"(config, emulation_name) "
                            f"VALUES (%s, %s) RETURNING id", (data_collection_job_json,
                                                              data_collection_job.emulation_env_name))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"Data collection job saved successfully")
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(training_job.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.TRAINING_JOBS_TABLE} "
                            f" SET config=%s "
                            f"WHERE {constants.METADATA_STORE.TRAINING_JOBS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Training job with id: {id} updated successfully")

    @staticmethod
    def update_experiment_execution(experiment_execution: ExperimentExecution, id: int) -> None:
        """
        Updates an experiment execution in the metastore

        :param experiment_execution: the experiment execution to update
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating experiment execution with id: {id} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(data_collection_job.to_dict(), indent=4, sort_keys=True)
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.PPO_POLICIES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_ppo_policy_record_to_dto(x), records))
                return records

    @staticmethod
    def _convert_ppo_policy_record_to_dto(ppo_policy_record) -> PPOPolicy:
        """
        Converts a PPO policy record fetched from the metastore into a DTO

        :param ppo_policy_record: the record to convert
        :return: the DTO representing the record
        """
        ppo_policy_json = json.dumps(ppo_policy_record[1], indent=4, sort_keys=True)
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        Logger.__call__().get_logger().debug(f"Installing PPO policy in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                policy_json_str = json.dumps(ppo_policy.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.PPO_POLICIES_TABLE} "
                            f"(policy, simulation_name) "
                            f"VALUES (%s, %s) RETURNING id", (policy_json_str, ppo_policy.simulation_name))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"PPO policy saved successfully")
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
                                                     sort_keys=True)
        system_identification_job_config: SystemIdentificationJobConfig = \
            SystemIdentificationJobConfig.from_dict(json.loads(system_identification_job_config_json))
        system_identification_job_config.id = system_identification_job_record[0]
        return system_identification_job_config

    @staticmethod
    def list_system_identification_jobs() -> List[SystemIdentificationJobConfig]:
        """
        :return: A list of system identification jobs in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_system_identification_job_record_to_dto(x),
                                   records))
                return records

    @staticmethod
    def get_system_identification_job_config(id: int) -> Union[None, SystemIdentificationJobConfig]:
        """
        Function for fetching a system identification job config with a given id from the metastore

        :param id: the id of the system identification job config
        :return: The system identification job config or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} WHERE id = %s", (id,))
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
        Logger.__call__().get_logger().debug(f"Saving a system identification job in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                system_identification_job_json = json.dumps(system_identification_job.to_dict(), indent=4,
                                                      sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.SYSTEM_IDENTIFICATION_JOBS_TABLE} "
                            f"(config, emulation_name) "
                            f"VALUES (%s, %s) RETURNING id", (system_identification_job_json,
                                                              system_identification_job.emulation_env_name))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"System identification job saved successfully")
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(system_identification_job.to_dict(), indent=4, sort_keys=True)
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
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
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
        Converts a gaussian mixture system model job record fetched from the metastore into a DTO

        :param gaussian_mixture_system_model_record: the record to convert
        :return: the DTO representing the record
        """
        gaussian_mixture_system_model_config_json = json.dumps(gaussian_mixture_system_model_record[1], indent=4,
                                                           sort_keys=True)
        gaussian_mixture_system_model_config: GaussianMixtureSystemModel = \
            GaussianMixtureSystemModel.from_dict(json.loads(gaussian_mixture_system_model_config_json))
        gaussian_mixture_system_model_config.id = gaussian_mixture_system_model_record[0]
        return gaussian_mixture_system_model_config

    @staticmethod
    def list_gaussian_mixture_system_models() -> List[GaussianMixtureSystemModel]:
        """
        :return: A list of gaussian mixture system model jobs in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_gaussian_mixture_system_model_record_to_dto(x),
                                   records))
                return records

    @staticmethod
    def get_gaussian_mixture_system_model_config(id: int) -> Union[None, GaussianMixtureSystemModel]:
        """
        Function for fetching a gaussian mixture system model job config with a given id from the metastore

        :param id: the id of the gaussian mixture system model job config
        :return: The gaussian mixture system model job config or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
                            f"WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_gaussian_mixture_system_model_record_to_dto(
                        gaussian_mixture_system_model_record=record)
                return record

    @staticmethod
    def save_gaussian_mixture_system_model(gaussian_mixture_system_model: GaussianMixtureSystemModel) -> Union[Any, int]:
        """
        Saves a gaussian mixture system model to the metastore

        :param gaussian_mixture_system_model: the gaussian mixture system model job to save
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Saving a gaussian mixture system model job in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                gaussian_mixture_system_model_json = json.dumps(gaussian_mixture_system_model.to_dict(), indent=4,
                                                            sort_keys=True, cls=NpEncoder)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
                            f"(config, emulation_name, emulation_statistic_id) "
                            f"VALUES (%s, %s) RETURNING id", (gaussian_mixture_system_model_json,
                                                              gaussian_mixture_system_model.emulation_env_name,
                                                              gaussian_mixture_system_model.emulation_statistic_id))
                id_of_new_row = cur.fetchone()[0]
                conn.commit()
                Logger.__call__().get_logger().debug(f"Gaussian mixture model saved successfully")
                return id_of_new_row

    @staticmethod
    def update_gaussian_mixture_system_model(gaussian_mixture_system_model: GaussianMixtureSystemModel, id: int) -> None:
        """
        Updates a gaussian mixture system model job in the metastore

        :param gaussian_mixture_system_model: the gaussian mixture system model job to save
        :param id: the id of the row to update
        :return: id of the created record
        """
        Logger.__call__().get_logger().debug(f"Updating gaussian mixture system model job with id: {id} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(gaussian_mixture_system_model.to_dict(), indent=4, sort_keys=True)
                cur.execute(f"UPDATE "
                            f"{constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} "
                            f" SET config=%s "
                            f"WHERE {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE}.id = %s",
                            (config_json_str, id))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Gaussian mixture system model with id: {id} updated successfully")

    @staticmethod
    def remove_gaussian_mixture_system_model(gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Removes a gaussian mixture system model job from the metastore

        :param gaussian_mixture_system_model: the job to remove
        :return: None
        """
        Logger.__call__().get_logger().debug(f"Removing gaussian mixture system model job with "
                                             f"id:{gaussian_mixture_system_model.id} from the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.GAUSSIAN_MIXTURE_SYSTEM_MODELS_TABLE} WHERE id = %s",
                            (gaussian_mixture_system_model.id,))
                conn.commit()
                Logger.__call__().get_logger().debug(f"Gaussian mixture system model with "
                                                     f"id {gaussian_mixture_system_model.id} deleted successfully")