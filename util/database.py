import os, atexit
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
cursor = conn.cursor()

@atexit.register
def saveandexit():
    conn.commit()
    cursor.close()
    conn.close()