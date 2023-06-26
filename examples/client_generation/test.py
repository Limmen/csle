import psycopg
import csle_common.constants.constants as constants
import time
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.management.session_token import SessionToken

if __name__ == '__main__':
    ts = time.time()
    session_token = SessionToken(token = "mytesttoken", timestamp=ts, username="admin")
    with psycopg.connect(f"{constants.METADATA_STORE.DB_NAME_PROPERTY}={constants.METADATA_STORE.DBNAME} "
                         f"{constants.METADATA_STORE.USER_PROPERTY}={constants.METADATA_STORE.USER} "
                         f"{constants.METADATA_STORE.PW_PROPERTY}={constants.METADATA_STORE.PASSWORD} "
                         f"{constants.METADATA_STORE.HOST_PROPERTY}={constants.METADATA_STORE.HOST}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO {constants.METADATA_STORE.SESSION_TOKENS_TABLE} "
                        f"(token, timestamp, username) "
                        f"VALUES (%s, %s, %s) RETURNING token",
                        (session_token.token, ts, session_token.username))
            token_of_new_row = cur.fetchone()[0]
            conn.commit()
            print(token_of_new_row)