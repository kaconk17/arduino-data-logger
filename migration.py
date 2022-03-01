import psycopg2
from config.connection import config

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS tb_list_device(
            address VARCHAR(100) NOT NULL PRIMARY KEY,
            nama VARCHAR(100) NOT NULL,
            mac VARCHAR(100) NOT NULL,
            jenis VARCHAR(100) NOT NULL,
            setatus VARCHAR(10) NOT NULL,
            lokasi VARCHAR(100),
            keterangan VARCHAR(100),
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        """,
    )
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
    create_tables()