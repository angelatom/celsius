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
    return True

def changeDisplayName(userID, newName):
    cursor.execute("UPDATE userInfo SET displayName = %s WHERE userID = %s", (newName, userID,))
    conn.commit()

def changePassword(userID, newPassword):
    cursor.execute("UPDATE userInfo SET password = %s WHERE userID = %s", (newPassword, userID,))
    conn.commit()

def sendMessage(channelID, authorID, content):
    cursor.execute("INSERT INTO messages (channelID, author, content) VALUES (%s, %s, %s)", (channelID, authorID, content,))
    conn.commit()

def inChannel(channelID, userID):
    cursor.execute("SELECT 1 FROM channelParticipants WHERE channelID = %s AND userID = %s LIMIT 1", (channelID, userID,))
    return cursor.rowcount == 1

def createChannel(participants):
    if len(participants) == 0:
        return False
    cursor.execute("INSERT INTO channels DEFAULT VALUES RETURNING channelID")
    channelID = cursor.fetchone()[0]
    argstr = b','.join([cursor.mogrify("(%s, %s)", (channelID, x,)) for x in participants])
    cursor.execute(b"INSERT INTO channelParticipants (channelID, userID) VALUES " + argstr)
    conn.commit()
    return channelID

def leaveChannel(channelID, userID):
    cursor.execute("DELETE FROM channelParticipants WHERE channelID = %s AND userID = %s", (channelID, userID,))
    conn.commit()

def addToChannel(channelID, userID):
    cursor.execute("INSERT INTO channelParticipants (channelID, userID) VALUES (%s, %s)", (channelID, userID,))
    conn.commit()

def getID(username):
    cursor.execute("SELECT userID FROM userInfo WHERE username = %s LIMIT 1", (username,))
    if cursor.rowcount == 0:
        return None
    return cursor.fetchone()[0]

def getTags(userID):
    cursor.execute("SELECT tags FROM tags WHERE userID = %s LIMIT 1", (userID,))
    if cursor.rowcount == 0:
        return None
    return cursor.fetchone()[0]


def updateTags(userID, tags):
    for i in range(len(tags)):
        tags[i] = tags[i].lower()
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
    cursor.execute("INSERT INTO buddy (userID, buddyUser) VALUES (%s, %s), (%s, %s)", (senderID, receiverID, receiverID, senderID))
    conn.commit()
    return True

def getBuddyReq(receiverID):
    cursor.execute("SELECT senderID FROM buddyRequests WHERE receiverID = %s", (receiverID,))
    return cursor.fetchall()

def getBuddies(userID):
    cursor.execute("SELECT buddyUser FROM buddy WHERE userID = %s", (userID,))
    return cursor.fetchall()

def getPendingInvites(userID):
    cursor.execute("SELECT receiverID FROM buddyRequests WHERE senderID = %s", (userID,))
    return cursor.fetchall()

def getChannel(userID, otherUser):
    query = '''
        WITH channelsIn AS (SELECT channelID FROM channelParticipants WHERE userID = %s)
        SELECT channelID FROM channelParticipants
        WHERE
            channelParticipants.userID = %s AND
            channelParticipants.channelID IN (SELECT * FROM channelsIn)
        LIMIT 1
    '''
    cursor.execute(query ,(userID, otherUser,))
    if cursor.rowcount == 0:
        createChannel([userID, otherUser])
        cursor.execute(query ,(userID, otherUser,))
    return cursor.fetchone()[0]

def getMessages(channelID, offset = 0):
    cursor.execute(
        '''
        SELECT author, content FROM messages
        WHERE channelID = %s
        ORDER BY timestamp DESC
        LIMIT 100
        OFFSET %s
        ''',
        (channelID, offset,)
    )
    return cursor.fetchall()

def getUserInfo(userID):
    cursor.execute("SELECT * FROM userInfo WHERE userID = %s LIMIT 1", (userID,))
    if cursor.rowcount == 0:
        return None
    return cursor.fetchone()

def authenticate(username, password):
    cursor.execute("SELECT userID FROM userInfo WHERE username = %s AND password = %s LIMIT 1", (username, password,))
    if cursor.rowcount == 0:
        return None
    return cursor.fetchone()[0]

def matchTags(userID):
    cursor.execute("SELECT tags FROM tags WHERE userID = %s LIMIT 1", (userID,))
    tags = cursor.fetchone()[0]
    cursor.execute(
        '''
        WITH buddiedIDs AS (SELECT buddyUser FROM buddy WHERE userID = %s)
        SELECT userID FROM tags
        WHERE
            userID NOT IN (SELECT * FROM buddiedIDs) AND
            userID != %s AND
            tags && %s
        LIMIT 5
        ''',
        (userID, userID, tags,)
    )
    return cursor.fetchall()

@atexit.register
def saveandexit():
    conn.commit()
    cursor.close()
    conn.close()