from typing import List, Union
import psycopg
import jsonpickle
import json
import csle_common.constants.constants as constants
from csle_common.dao.container_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.container_config.log_sink_config import LogSinkConfig


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
    def list_log_sinks() -> List[LogSinkConfig]:
        """
        :return: A list of emulations in the metastore
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.LOGSINKS_TABLE}")
                records = cur.fetchall()
                records = list(map(lambda x: MetastoreFacade._convert_log_sink_record_to_dto(x), records))
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
    def get_log_sink(name: str) -> Union[None, LogSinkConfig]:
        """
        Function for extracting the metadata of a log sink with a given name

        :param name: the name of the log sink
        :return: The log sink config or None if the log sink was not found
        """
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {constants.METADATA_STORE.LOGSINKS_TABLE} WHERE name = %s", (name,))
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
    def _convert_log_sink_record_to_dto(log_sink_record) -> LogSinkConfig:
        """
        Converts a log sink record fetched from the metastore into a DTO

        :param emulation_record: the record to convert
        :return: the DTO representing the record
        """
        log_sink_config_json_str = json.dumps(log_sink_record[2], indent=4, sort_keys=True)
        log_sink_config: LogSinkConfig = jsonpickle.decode(log_sink_config_json_str)
        return log_sink_config