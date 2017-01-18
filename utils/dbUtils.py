import sqlite3
import hashlib, sys
import time

db = sqlite3.connect("data/mississippi.db", check_same_thread = False)
c = db.cursor()

# USERS FORMAT

#0|user_id|INTEGER|0||0
#1|username|TEXT|0||0
#2|pwd_hash|TEXT|0||0
#3|streak|INTEGER|0||0
#4|max_streak|INTEGER|0||0
#5|last_upload|INTEGER|0||0

# Creates a new user to our lovely site. Returns true if it worked. False if it didn't. I don't know why it wouldn't
# Takes Args: STRING username, STRING pass_hash
# Returns: BOOLEAN
def createUser(username, pass_hash):
    try:
        db = sqlite3.connect("data/mississippi.db")
        c = db.cursor()
        query = "INSERT INTO users VALUES (?, ?, ?, 0, 0, ?)"
        newID = hash(username) % ((sys.maxsize + 1))
        c.execute(query, (newID, username, pass_hash, int(time.time())))
        db.commit()
        db.close()
        return True
    except Exception:
        print Exception
        return False
    
# Returns whether a login is valid
# Takes Args: STRING username, STRING hash_pass
# Returns: BOOLEAN
def checkLogin(username, hash_pass):
    c.execute("SELECT username FROM users WHERE username = ? AND pwd_hash = ?", (username, hash_pass))
    # Returns true if the login is valid
    # Returns false if the login is wrong
    return len(c.fetchall()) > 0

# Checks if a username is taken or not
# Takes Args: STRING username
# Returns: BOOLEAN 
def checkUsername(username):
    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    # Returns true if the username is free
    # Returns false if the username is in use
    return len(c.fetchall()) == 0

# Returns a username based on a user_id
# Takes Args: INT userID
# Returns: STRING
def reverseLookup(userID):
    c.execute("SELECT username FROM users WHERE user_id = ?", (userID,))
    return c.fetchone()[0]

# Returns relevant data about a user based on username
# Takes Args: STRING username
# Returns: DICT
def getUserInfo(username):
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    items = c.fetchone()
    info = { "user_id" : items[0], "streak" : items[3], "max_streak" : items[4], "last_upload" : items[5] }
    return info

# POST FORMAT

#0|post_id|INTEGER|0||0
#1|author|INTEGER|0||0
#2|photo_link|TEXT|0||0
#3|caption|TEXT|0||0
#4|upload_date|INTEGER|0||0

# Converts a tuple from a db call to a dict
# Takes Args: TUPLE items
# Returns: DICT
def dictifyPost(items):
    info = { "post_id" : items[0], "author" : reverseLookup(items[1]), "photo_link" : items[2], "caption" : items[3], "upload_date" : time.strftime("%A, %B %d %Y at %I:%M %p", time.localtime(items[4])) }
    return info

# Creates a post. Returns whether the post is created succesfully or not
# Takes Args: STRING username, STRING image (represents image url), STRING caption
# Returns: BOOLEAN
def createPost(username, image, caption):
    try:
        query = "INSERT INTO posts VALUES (?, ?, ?, ?, ?)"
        newID = hash(image) % ((sys.maxsize + 1))
        timenow = int(time.time())
        userinfo = getUserInfo(username)
        if time.gmtime(timenow)[2] != time.gmtime(userinfo['last_upload'])[2] or len(getPostsForUser(username)) == 0:
            print "new day"
        c.execute(query, (newID, userinfo['user_id'], image, caption, timenow))
        c.execute("UPDATE users SET last_upload = ? WHERE username = ?", (timenow, username))
        if timenow - userinfo['last_upload'] < 60*60*24:
            c.execute("UPDATE users SET streak = ? WHERE username = ?", (userinfo['streak']+1, username))
            userinfo['streak'] += 1
            if userinfo['streak'] > userinfo['max_streak']:
                c.execute("UPDATE users SET max_streak = ? WHERE username = ?", (userinfo['streak'], username))
        else:
            c.execute("UPDATE users SET streak = 0 WHERE username = ?", (username,))
        db.commit()
        #print "Today's Day: " + str(time.gmtime(timenow)[2]) + ", Last Upload's Day: " + str(time.gmtime(userinfo['last_upload'])[2])
        return True
    except Exception:
        print Exception
        return False

# Returns a dictified version of a post with a certain postID
# Takes Args: INT postID
# Returns: DICT
def getPostByID(postID):
    c.execute('SELECT * FROM posts WHERE post_id = ?', (postID,))
    return dictifyPost(c.fetchone())

# Returns a certain number of posts with an option to get them from one user
# Takes Args: INT number (number of posts), INT page [, STRING user (username to get posts from)]
# Returns: DICT
def getSomePosts(number, page, user=None):
    if user != None:
        user = getUserInfo(user)['user_id']
        c.execute('SELECT * FROM posts WHERE author = ? LIMIT ? OFFSET ?', (user, number, page * number))
    else:
        c.execute('SELECT * FROM posts LIMIT ? OFFSET ?', (number, page * number))
    postlist = []
    for item in c.fetchall():
        postlist.append(dictifyPost(item))
    return postlist

def tables():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    stringtable = []
    for table in c.fetchall():
        stringtable.append(sntr(table[0]))
    return stringtable

def columns(tablename):
    c.execute("PRAGMA table_info(%s)" % tablename)
    stringdict = {}
    for tuplet in c.fetchall():
        stringdict[str(tuplet[1])] = str(tuplet[2])
    return stringdict

def getPages(pageLength):
    c.execute("SELECT COUNT(photo_link) FROM posts")
    postcount = c.fetchone()[0]
    if postcount % pageLength == 0 and postcount >= pageLength:
        return postcount / pageLength
    else:
        return postcount / pageLength + 1
