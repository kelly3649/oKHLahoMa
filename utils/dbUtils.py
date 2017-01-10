import sqlite3
import hashlib, sys

db = sqlite3.connect("data/mississippi.db")
c = db.cursor()

# USERS FORMAT

#0|user_id|INTEGER|0||0
#1|username|TEXT|0||0
#2|pwd_hash|TEXT|0||0
#3|streak|INTEGER|0||0
#4|max_streak|INTEGER|0||0
#5|last_upload|INTEGER|0||0

def createUser(username, pass_hash, timestamp):
    query = "INSERT INTO users VALUES (?, ?, ?, 0, 0, ?)"
    newID = hash(username) % ((sys.maxsize + 1))
    c.execute(query, (newID, username, pass_hash, timestamp))
    db.commit()

def checkLogin(username, hash_pass):
    c.execute("SELECT username FROM users WHERE username = ? AND pwd_hash = ?", (username, hash_pass))
    return len(c.fetchall()) > 0

def checkUsername(username):
    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    # Returns true if the username is free
    # Returns false if the username is in use
    return len(c.fetchall()) == 0

def getUserID(username):
    c.execute("SELECT user_id FROM users where username = ?", (username,))
    return c.fetchone()[0]
 
# POST FORMAT

#0|post_id|INTEGER|0||0
#1|author|INTEGER|0||0
#2|photo_link|TEXT|0||0
#3|caption|TEXT|0||0
#4|upload_date|INTEGER|0||0

def createPost(username, timestamp, image, caption):
    query = "INSERT INTO posts VALUES (?, ?, ?, ?, ?)"
    newID = hash(image) % ((sys.maxsize + 1))
    c.execute(query, (newID, getUserID(username), image, caption, timestamp))
    db.commit()

def getPostsForUser(username):
    c.execute('SELECT * FROM posts WHERE author = ?', (getUserID(username),))
    print c.fetchall()
            
def tables():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    stringtable = []
    for table in c.fetchall():
        stringtable.append(str(table[0]))
    return stringtable

def columns(tablename):
    c.execute("PRAGMA table_info(%s)" % tablename)
    stringdict = {}
    for tuplet in c.fetchall():
        stringdict[str(tuplet[1])] = str(tuplet[2])
    return stringdict
