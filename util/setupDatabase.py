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
            displayName TEXT,
            username TEXT UNIQUE,
            password TEXT
        );
        CREATE TABLE IF NOT EXISTS channels(
            channelID SERIAL PRIMARY KEY
        );
        CREATE TABLE IF NOT EXISTS channelParticipants(
            channelID INTEGER REFERENCES channels(channelID) ON DELETE CASCADE,
            userID INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS buddy(
            userID INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            buddyUser INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            CONSTRAINT unq_user_buddyUser UNIQUE(userID, buddyUser)
        );
        CREATE TABLE IF NOT EXISTS buddyRequests(
            senderID INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            receiverID INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            CONSTRAINT unq_senderID_receiverID UNIQUE(senderID, receiverID)
        );
        CREATE TABLE IF NOT EXISTS tags(
            userID INTEGER UNIQUE REFERENCES userInfo(userID) ON DELETE CASCADE,
            tags TEXT ARRAY
        );
        CREATE TABLE IF NOT EXISTS messages(
            messageID SERIAL PRIMARY KEY,
            channelID INTEGER REFERENCES channels(channelID) ON DELETE CASCADE,
            author INTEGER REFERENCES userInfo(userID) ON DELETE SET NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        '''
    )

setup()
conn.commit()
cursor.close()
conn.close()