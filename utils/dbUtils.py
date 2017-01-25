import sqlite3
import hashlib, sys
import time

db = sqlite3.connect("data/mississippi.db", check_same_thread = False)
c = db.cursor()

# FOLLOWTABLE FORMAT

#0|follower|INTEGER|0||0
#1|following|INTEGER|0||0

# Follows a user. First argument is person doing the following, second is the person being followed.
# Takes Args: STRING following, STRING being_followed
# Returns: BOOLEAN
def followUser(following, being_followed):
    try:
        following = getUserInfo(following)["user_id"]
        being_followed = getUserInfo(being_followed)["user_id"]
        c.execute("INSERT INTO followtable VALUES (?, ?)", (following, being_followed))
        db.commit()
        return True
    except Exception as e:
        return False

# Unfollows a user. Fist argument is person unfollowing, second is target
# Takes Args: STRING following, STRING being_followed
# Returns: Boolean
def unfollowUser(unfollowing, target):
    try:
        following = getUserInfo(unfollowing)["user_id"]
        target = getUserInfo(target)["user_id"]
        c.execute("DELETE FROM followtable WHERE follower = ? AND following = ?", (following, target))
        db.commit()
        return True
    except Exception:
        return False

# Returns a tuple containing the usernames of all the people being followed
# Takes Args: STRING username
# Returns: TUPLE
def getFollowed(username):
    userID = getUserInfo(username)["user_id"]
    c.execute("SELECT following FROM followtable WHERE follower = ?", (userID,))
    return c.fetchall()

# Returns a boolean if username can follow other
# Takes Args: STRING username, STRING other
# Returns: BOOLEAN
def canFollow(username, other):
    userID = getUserInfo(other)["user_id"]
    return (userID,) not in getFollowed(username) and username != other
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
    except Exception as e:
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
    info = { "user_id" : items[0], "streak" : items[3], "max_streak" : items[4], "last_upload" : items[5], "last_upload_formatted": time.strftime("%A, %B %d %Y at %I:%M %p", time.localtime(items[5])) }
    return info

# Deletes a user and all of their posts
# Takes args: STRING username
# Returns: BOOLEAN
def deleteUser(username):
    userinfo = getUserInfo(username)
    c.execute("DELETE FROM posts WHERE author = ?", (userinfo["user_id"],))
    c.execute("DELETE FROM users WHERE username = ?", (username,))
    db.commit()

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
    try:
        info = { "post_id" : items[0], "author" : reverseLookup(items[1]), "photo_link" : items[2], "caption" : items[3], "upload_date" : time.strftime("%A, %B %d %Y at %I:%M %p", time.localtime(items[4])), "raw_upload_date":items[4] }
        return info
    except Exception:
        return {}


# Deletes a post based on postid
# Takes Args: STRING username, INT post_id
# Returns: BOOLEAN
def deletePost(username, post_id):
    try:
        postdata = getPostByID(post_id)
        c.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))
        db.commit()
        if getUserInfo(username)["last_upload"] == postdata["raw_upload_date"]:
            lastPost = getSomePosts(1, 0, username)
            c.execute("UPDATE users SET last_upload = ? WHERE username = ?", (lastPost["raw_upload_date"], username))
            userInfo = getUserInfo(username)
            c.execute("UPDATE users SET streak = ? WHERE username = ?", (getUserInfo(username)["streak"]-1, username))
            if userInfo["streak"] == userInfo["max_streak"]:
                c.execute("UPDATE users SET max_streak = ? WHERE username = ?", (userInfo["streak"]-1, username))                
        return True
    except Exception:
        return False
    
# Checks if a user has posted today
# Takes Args: STRING username
# Returns: BOOLEAN
def canPost(username):
    timenow = int(time.time())
    userinfo = getUserInfo(username)
    try:
        return time.gmtime(timenow)[2] != time.gmtime(userinfo['last_upload'])[2] or len(getSomePosts(10,0,username)) == 0
    except Exception:
        return False

# Creates a post. Returns whether the post is created succesfully or not
# Takes Args: STRING username, STRING image (represents image url), STRING caption
# Returns: BOOLEAN
def createPost(username, image, caption):
    try:
        query = "INSERT INTO posts VALUES (?, ?, ?, ?, ?)"
        newID = hash(image) % ((sys.maxsize + 1))
        timenow = int(time.time())
        userinfo = getUserInfo(username)
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
    except Exception as e:
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
        c.execute('SELECT * FROM posts WHERE author = ? ORDER BY upload_date DESC LIMIT ? OFFSET ?', (user, number, page * number))
    else:
        c.execute('SELECT * FROM posts ORDER BY upload_date DESC LIMIT ? OFFSET ?', (number, page * number))
    postlist = []
    for item in c.fetchall():
        postlist.append(dictifyPost(item))
    #print postlist
    return postlist

# Returns a certain number of posts followed by a user
# Takes Args: INT number (number of posts), INT page [, STRING user (username to get posts from)]
# Returns: DICT
def getFollowedPosts(number, page, user):
    try:
        followedUsers = getFollowed(user)
        query = "SELECT * FROM posts WHERE"
        for user in followedUsers:
            query += " author = %s OR" % user
        query = query[0:len(query)-2]
        query += "ORDER BY upload_date DESC LIMIT ? OFFSET ?"
        try:
            c.execute(query, (number, page*number))
        except Exception as e:
            return []
        postlist = []
        for item in c.fetchall():
            postlist.append(dictifyPost(item))
        return postlist
    except Exception:
        return []


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

def getTime():
    timenow = time.localtime()
    return { "year":timenow[0], "month":timenow[1], "day":timenow[2], "hour":timenow[3], "minute":timenow[4], "second":timenow[5] }
