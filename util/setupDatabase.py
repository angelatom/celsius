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
        CREATE TABLE IF NOT EXISTS channels(
            channelID SERIAL PRIMARY KEY
        );
        CREATE TABLE IF NOT EXISTS channelParticipants(
            channelID INTEGER REFERENCES channels(channelID) ON DELETE CASCADE,
            userID INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS buddy(
            user INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            buddyUser INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            CONSTRAINT unq_user_buddyUser UNIQUE(user, buddyUser)
        );
        CREATE TABLE IF NOT EXISTS buddyRequests(
            senderID INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            receiverID INTEGER REFERENCES userInfo(userID) ON DELETE CASCADE,
            CONSTRAINT unq_senderID_receiverID UNIQUE(senderID, receiverID)
        );
        CREATE TABLE IF NOT EXISTS tags(
            userID INTEGER UNIQUE REFERENCES userInfo(userID) ON DELETE CASCADE,
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