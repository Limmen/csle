from typing import List, Dict
import psycopg
import csle_common.constants.constants as constants


def query_metastore_select(table: str) -> List[Dict[int, Dict]]:
    """
    Performs a SELECT * query for a given table in the metastore

    :param table: the name of the table to select data  from
    :return: the selected records
    """
    with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                         f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                         f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                         f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table}")
            records = cur.fetchall()
            return records


if __name__ == '__main__':
    example_table = constants.METADATA_STORE.EMULATION_SIMULATION_TRACES_TABLE
    records = query_metastore_select(table=example_table)
