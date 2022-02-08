from typing import List
import psycopg
import csle_common.constants.constants as constants


class MetastoreFacade:
    """
    Facade for the metastore, contains methods for querying the metastore
    """

    @staticmethod
    def list_emulations() -> List:
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM emulations")
                records = cur.fetchall()
                return records


    @staticmethod
    def get_emulation(name: str):
        with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                             f"password={constants.METADATA_STORE.PASSWORD} "
                             f"host={constants.METADATA_STORE.HOST}") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM emulations WHERE name = %s", (name,))
                record = cur.fetchone()
                return record