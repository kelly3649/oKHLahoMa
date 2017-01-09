import sqlite3
import hashlib, sys

db = sqlite3.connect("data/mississippi.db")
c = db.cursor()

#USERS FORMAT
#{'username': 'TEXT', 'streak': 'INTEGER', 'user_id': 'INTEGER', 'last_upload': 'INTEGER', 'pwd_hash': 'TEXT', 'max_streak': 'INTEGER'}
def createUser(username, pass_hash):
    query = "INSERT INTO users VALUES (?, ?, ?, 0, 0, 0)"
    newID = hash('asdf') % ((sys.maxsize + 1))
    c.execute(query, (newID, username, pass_hash))
    db.commit()

def checkLogin(username, hash_pass):
    c.execute("SELECT username FROM users WHERE username = ? AND pwd_hash = ?", (username, hash_pass))
    return len(c.fetchall()) > 0

def checkUsername(username):
    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    # Returns true if the username is free
    # Returns false if the username is in use
    return len(c.fetchall()) == 0


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
