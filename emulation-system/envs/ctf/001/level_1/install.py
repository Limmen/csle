import psycopg
import csle_common.constants.constants as constants

def test():
    with psycopg.connect(f"dbname={constants.METADATA_STORE.DBNAME} user={constants.METADATA_STORE.USER} "
                         f"password={constants.METADATA_STORE.PASSWORD} host={constants.METADATA_STORE.HOST}") as conn:
        with conn.cursor() as cur:

            # Execute a command: this creates a new table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS test (
                    id serial PRIMARY KEY,
                    num integer,
                    data text)
                """)
            print("created table?")

            # Pass data to fill a query placeholders and let Psycopg perform
            # the correct conversion (no SQL injections!)
            cur.execute(
                "INSERT INTO test (num, data) VALUES (%s, %s)",
                (100, "abc'def"))

            # Query the database and obtain data as Python objects.
            cur.execute("SELECT * FROM test")
            cur.fetchone()
            # will return (1, 100, "abc'def")

            # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
            # of several records, or even iterate on the cursor
            for record in cur:
                print("rec?")
                print(record)

            # Make the changes to the database persistent
            conn.commit()



if __name__ == '__main__':
    test()