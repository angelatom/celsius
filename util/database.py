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

def changeDisplayName(userID, newName):
    cursor.execute("UPDATE userInfo SET displayName = %s WHERE userID = %s", (newName, userID,))

def changePassword(userID, newPassword):
    cursor.execute("UPDATE userInfo SET password = %s WHERE userID = %s", (newPassword, userID,))

def sendMessage(channelID, authorID, content):
    cursor.execute("INSERT INTO messages (channelID, author, content) VALUES (%s, %s, %s)", (channelID, authorID, content,))

@atexit.register
def saveandexit():
    conn.commit()
    cursor.close()
    conn.close()