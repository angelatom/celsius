import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

def setup():
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS userInfo(
            userID SERIAL PRIMARY KEY,
            displayName VARCHAR(32),
            username VARCHAR(32) UNIQUE,
            password VARCHAR(32)
        );
        CREATE TABLE IF NOT EXISTS channel(
            channelID SERIAL PRIMARY KEY,
            participants INTEGER ARRAY
        );
        CREATE TABLE IF NOT EXISTS buddy(
            username INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            buddyuser INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS tags(
            userID INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            tags VARCHAR(32) ARRAY
        );
        CREATE TABLE IF NOT EXISTS messages(
            messageID SERIAL PRIMARY KEY,
            channelID INTEGER REFERENCES channel(channelID) ON DELETE CASCADE,
            author INTEGER REFERENCES userInfo(userID) ON DELETE SET NULL,
            content VARCHAR(2000) NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        '''
    )

setup()
conn.commit()
cursor.close()
conn.close()