from typing import List, Union
import psycopg
import jsonpickle
import json
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace


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
    def _convert_emulation_record_to_dto(emulation_record) -> EmulationEnvConfig:
        """
        Converts an emulation record fetched from the metastore into a DTO

        :param emulation_record: the record to convert
        :return: the DTO representing the record
        """
        emulation_config_json_str = json.dumps(emulation_record[2], indent=4, sort_keys=True)
        emulation_env_config: EmulationEnvConfig = jsonpickle.decode(emulation_config_json_str)
        return emulation_env_config


    @staticmethod
    def _convert_trace_record_to_dto(trace_record) -> EmulationTrace:
        """
        Converts a trace record fetched from the metastore into a DTO

        :param trace_record: the record to convert
        :return: the DTO representing the record
        """
        trace_json_str = json.dumps(trace_record[2], indent=4, sort_keys=True)
        trace: EmulationTrace = EmulationTrace.from_dict(json.loads(trace_json_str))
        return trace


    @staticmethod
    def install_emulation(config: EmulationEnvConfig) -> None:
        """
        Installs the emulation configuration in the metastore

        :param config: the config to install
        :return: None
        """
        print(f"Installing emulation:{config.name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                try:
                    config_json_str = json.dumps(json.loads(jsonpickle.encode(config)), indent=4, sort_keys=True)
                    cur.execute(f"INSERT INTO {constants.METADATA_STORE.EMULATIONS_TABLE} (name, config) "
                                f"VALUES (%s, %s)", (config.name, config_json_str))
                    conn.commit()
                    print(f"Emulation {config.name} installed successfully")
                except psycopg.errors.UniqueViolation as e:
                    print(f"Emulation {config.name} is already installed")


    @staticmethod
    def uninstall_emulation(config: EmulationEnvConfig) -> None:
        """
        Uninstalls the emulation configuration in the metastore

        :param config: the config to uninstall
        :return: None
        """
        print(f"Uninstalling emulation:{config.name} from the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {constants.METADATA_STORE.EMULATIONS_TABLE} WHERE name = %s", (config.name,))
                conn.commit()
                print(f"Emulation {config.name} uninstalled successfully")

    @staticmethod
    def save_trace(trace: EmulationTrace) -> None:
        """
        Saves a trace from the emulation

        :param trace: the trace to save
        :return: None
        """
        print(f"Installing trace for emulation:{trace.emulation_name} in the metastore")
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                config_json_str = json.dumps(trace.to_dict(), indent=4, sort_keys=True)
                cur.execute(f"INSERT INTO {constants.METADATA_STORE.TRACES_TABLE} (emulation_name, trace) "
                            f"VALUES (%s, %s)", (trace.emulation_name, config_json_str))
                conn.commit()
                print(f"Trace for emulation {trace.emulation_name} saved successfully")


    @staticmethod
    def list_traces() -> List[EmulationTrace]:
        """
        :return: A list of emulation traces in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TRACES_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_trace_record_to_dto(x), records))
                return records

    @staticmethod
    def get_trace(id: int) -> Union[None, EmulationTrace]:
        """
        Function for fetching a trace with a given id from the metastore

        :param id: the id of the trace
        :return: The trace or None if it could not be found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.TRACES_TABLE} WHERE id = %s", (id,))
                record = cur.fetchone()
                if record is not None:
                    record = MetastoreFacade._convert_trace_record_to_dto(trace_record=record)
                return record