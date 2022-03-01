import psycopg2
from config.connection import config

def getDevice():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
    
        cur.execute("""SELECT ip_address FROM tb_list_device WHERE setatus = %s""",('ON',))
        rows = cur.fetchall()
        
        for row in rows:
            print(row[0])
        cur.close()
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')




if __name__ == '__main__':
    getDevice()