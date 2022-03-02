import psycopg2
from config.connection import config
#import requests
import aiohttp
import asyncio

def getDevice():
    """ Connect to the PostgreSQL database server """
    conn = None
    res = []
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
    
        cur.execute("""SELECT ip_address FROM tb_list_device WHERE setatus = %s""",('ON',))
        rows = cur.fetchall()
        
        for row in rows:
            res.append(row[0])
        cur.close()
	
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return res   

async def getData(session, addres):
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with session.get(addres, timeout=timeout) as resp:
            dt = await resp.json()
            return dt
    except Exception as e:
        print(e)

async def dataProc():

    async with aiohttp.ClientSession() as session:
        task = []
        listDev = getDevice()

        for dev in listDev:
            addr = f'http://{dev}'
            task.append(asyncio.ensure_future(getData(session,addr)))
        
        rawData = await asyncio.gather(*task)
        #print(rawData)
        if rawData is not None:
            for res in rawData:
                print(res['temp'])


if __name__ == '__main__':
    asyncio.run(dataProc())