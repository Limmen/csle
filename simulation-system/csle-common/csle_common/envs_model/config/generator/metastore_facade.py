from typing import List, Union
import psycopg
import jsonpickle
import json
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig

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
        emulation_env_config.vuln_config = VulnerabilitiesConfig.from_dict(emulation_env_config.vuln_config)
        for vuln in emulation_env_config.vuln_config.vulnerabilities:
            if isinstance(vuln.vuln_type, str):
                pass
        return emulation_env_config


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
                    config.vuln_config = config.vuln_config.to_dict()
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
