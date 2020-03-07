import os, atexit
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
cursor = conn.cursor()

def registerUser(displayName, username, password):
    cursor.execute("SELECT 1 FROM userInfo WHERE username = %s LIMIT 1", (username,))
    if cursor.rowcount == 1:
        return False
    cursor.execute("INSERT INTO userInfo (displayName, username, password) VALUES (%s, %s, %s)", (displayName, username, password,))
    conn.commit()

def changeDisplayName(userID, newName):
    cursor.execute("UPDATE userInfo SET displayName = %s WHERE userID = %s", (newName, userID,))
    conn.commit()

def changePassword(userID, newPassword):
    cursor.execute("UPDATE userInfo SET password = %s WHERE userID = %s", (newPassword, userID,))
    conn.commit()

def sendMessage(channelID, authorID, content):
    conn.execute("INSERT INTO messages (channelID, author, content) VALUES (%s, %s, %s)", (channelID, authorID, content,))
    conn.commit()

def createChannel(participants):
    if len(participants) == 0:
        return False
    cursor.execute("INSERT INTO channels DEFAULT VALUES RETURNING channelID")
    channelID = cursor.fetchone()[0]
    argstr = ','.join(cursor.mogrify("(%s, %s)", (channelID, x,)) for x in participants)
    cursor.execute("INSERT INTO channelParticipants (channelID, userID) VALUES " + argstr)
    conn.commit()

def leaveChannel(channelID, userID):
    cursor.execute("DELETE FROM channelParticipants WHERE channelID = %s AND userID = %s", (channelID, userID,))
    conn.commit()

def addToChannel(channelID, userID):
    cursor.execute("INSERT INTO channelParticipants (channelID, userID) VALUES (%s, %s)", (channelID, userID,))
    conn.commit()

def updateTags(userID, tags):
    cursor.execute(
        '''
        INSERT INTO tags (userID, tags)
        VALUES (%s, %s)
        ON CONFLICT (userID)
        DO UPDATE SET tags = %s
        ''',
        (userID, tags, tags,)
    )
    conn.commit()

def sendBuddyReq(senderID, receiverID):
    cursor.execute("SELECT 1 FROM buddyRequests WHERE senderID = %s AND receiverID = %s LIMIT 1", (receiverID, senderID,))
    if cursor.rowcount == 1:
        acceptReq(receiverID, senderID)
        return
    cursor.execute(
        '''
        INSERT INTO buddyRequests (senderID, receiverID)
        VALUES (%s, %s)
        ON CONFLICT ON CONSTRAINT unq_senderID_receiverID
        DO NOTHING
        ''',
        (senderID, receiverID,)
    )
    conn.commit()

def acceptReq(senderID, receiverID):
    cursor.execute("DELETE FROM buddyRequests WHERE senderID = %s AND receiverID = %s", (senderID, receiverID,))
    if cursor.rowcount != 1:
        return False
    cursor.execute("INSERT INTO buddy (user, buddyUser) VALUES (%s, %s)", (senderID, receiverID))
    cursor.commit()
    return True

def getBuddies(userID):
    cursor.execute("SELECT * FROM buddy WHERE user = %s OR buddyUser = %s", (userID, userID,))
    return [x[0] if x[0] != userID else x[1] for x in cursor.fetchall()]

def getMessages(channelID, offset = 0):
    cursor.execute(
        '''
        SELECT * FROM messages
        WHERE channelID = %s
        ORDER BY timeAdded DESC
        LIMIT 100
        OFFSET %s
        ''',
        (channelID, offset,)
    )
    return cursor.fetchall()

def getUserInfo(userID):
    cursor.execute("SELECT * FROM userInfo WHERE userID = %s LIMIT 1", (userID,))
    return cursor.fetchone()

def authenticate(username, password):
    cursor.execute("SELECT userID FROM userInfo WHERE username = %s AND password = %s LIMIT 1", (username, password,))
    if cursor.rowcount == 0:
        return None
    return cursor.fetchone()[0]

@atexit.register
def saveandexit():
    conn.commit()
    cursor.close()
    conn.close()