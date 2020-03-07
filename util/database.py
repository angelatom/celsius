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

@atexit.register
def saveandexit():
    conn.commit()
    cursor.close()
    conn.close()