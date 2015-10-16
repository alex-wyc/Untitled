import sqlite3
from time import time

# input: username, hash (hexstring) of user's password
# returns: true if the username is NOT in the database, and a user is created
# returns; false if the username has been taken
def newUser(username, passwordHash):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q="""
    SELECT users.username
    FROM users
    WHERE users.username = "%s"
    """ % (username)
    usernames = c.execute(q).fetchall()
    if len(usernames) == 0:
        q="INSERT INTO users VALUES ('%s','%s')" % (username, passwordHash)
        c.execute(q)
        conn.commit()
        return True
    else:
        return False

# input: username-passwordHash pair
# output: true if the pair match, false if the pair does not
def authenticate(uName, passwordHash):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q="""
    SELECT users.username, users.password
    FROM users
    WHERE users.username = "%s" and users.password = "%s"
    """ % (uName, passwordHash)
    result = c.execute(q).fetchall() # gets it as a list
    if len(result) == 0:
        return False
    else:
        return True;

def getStory(storyID):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """SELECT stories.sentence
           FROM stories
           WHERE stories.id = %d
           ORDER BY time""" % (storyID)
    result = c.execute(q).fetchall()
    if len(result) == 0:
        return ""
    else:
        story = ""
        for i in result:
            story += i + " "
        return story

def addSentence(storyID, sentence, author):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    q = """INSERT INTO stories VALUES (%d, '%s', '%s', %d)""" % (storyID. sentence, author, int(time()))
    c.execute(q)
    conn.commit()

# return a list of favorite stories
def getFavorites(username):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()

    stories = []
    q = """SELECT favorites.id
           FROM favorites
           WHERE favorites.username = '%s'""" % (username)
    result = c.execute(q).fetchall()
    for i in result:
        stories.append(getStory(i))

def addFavorite(storyID, username):
    conn = sqlite3.connect("infos.db")
    c = conn.cursor()
    q="""INSERT INTO favorites VALUES (%d, %s)""" %(storyID, username)
    c.execute(q)
    conn.commit()


#print newUser("yeech", "12345")
#print authenticate("yeech", "12345")
#print authenticate("yeech2", "12345")
#print authenticate("yeech", "11111")