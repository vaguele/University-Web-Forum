from flask import Flask,render_template,request,jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import json
#import time
import mysql.connector
import datetime
#import pandas as pd


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://UCMSocialMediaAp:mysqlpassword@UCMSocialMediaApp.mysql.pythonanywhere-services.com/UCMSocialMediaAp$default"
db = SQLAlchemy(app)
admin_instance = Admin(app)


@dataclass      #TABLE MODEL for LOGININFO. SQLaclhemy way of doing database stuff
class loginInfo(db.Model):
    __tablename__ = 'loginInfo'
    Id = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.String)
    Password = db.Column(db.String)
    children = db.relationship('dashboardPosts', backref='loginInfo', lazy=True)

@dataclass
class dashboardPosts(db.Model):    #TABLE MODEL for dashboardPosts. SQLaclhemy way of doing database stuff
    __tablename__ = 'databasePosts'
    Id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey('loginInfo.Id'))
    Post_Body = db.Column(db.Text)
    time_posted = db.Column(db.Date)
    rating = db.Column(db.Integer)

# class Posts(db.Model): #added by Anirud 9:35pm 5/6/2024
#     __tablename__ = 'Posts'
#     Id = db.Column(db.Integer, primary_key = True)
#     userId = db.Column(db.Integer, db.ForeignKey('loginInfo.Id'))
#     Post_Body = db.Column(db.Text)
#     time_posted = db.Column(db.Date)
#     rating = db.Column(db.Integer)
#     replyTo = db.Column(db.Integer)
#     tag = db.Column(db.String)



@dataclass
class placeSportClassRating(db.Model):
    __tablename__ = 'placeSportClassRating'
    Id = db.Column(db.Integer)
    name = db.Column(db.String, primary_key = True)
    likes = db.Column(db.Integer)

class whoAlreadyLikedPSC(db.Model):
    __tablename__ = 'whoAlreadyLikedPSC'
    UserId = db.Column(db.Integer, db.ForeignKey('loginInfo.Id'), primary_key = True)
    PSCName = db.Column(db.Integer, db.ForeignKey('placeSportClassRating.name'), primary_key = True)


admin_instance.add_view(ModelView(loginInfo, db.session))   #add loginInfo to admin view

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)


def check_db_connection ():
    try:
        conn = mysql.connector.connect( #con stands for connection to database
        host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
        user="UCMSocialMediaAp",                      # last p lost?
        password="mysqlpassword",
        database="UCMSocialMediaAp$default"
        )
        return True
    except mysql.connector.Error as e:
        return False


@app.route('/')
def index():
    is_connected = check_db_connection()
    if is_connected:
        message =  'Successfully Connected'
    else:
        message = 'NOT CONNECTED'
    return render_template('index.html', message = message)  #sends message(second arg)


@app.route('/login',  methods = ['GET', 'POST'])
def login():
    print("login accessed")
    obj = json.loads(request.data.decode('UTF-8'))
    username = obj["username"]
    password = obj["password"]

    conn = mysql.connector.connect( #con stands for connection to database
          host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
          user="UCMSocialMediaAp",                      # last p lost?
          password="mysqlpassword",
          database="UCMSocialMediaAp$default"
    )

    mycursor = conn.cursor()  # set up for database

    mycursor.execute("SELECT * FROM loginInfo")
    myresult = mycursor.fetchall()
    if (request.method == "POST"):
        inside = False
        for row in myresult:
            if row[1] == username:
                inside = True
                conn.close()
                return "Username Already Taken"
        if inside == False:
            #ALREADY SALTS ITSELF
            # salt = ""
            # for x in range(0,10):
            #     salt += (str(random.randint(0, 9)))

            # passAndSalt =  salt + password
            # hash = generate_password_hash(passAndSalt,'sha256')
            # hashAndSalt = "$" + salt + "$" + hash
            # remember to reset passwords
            hash = generate_password_hash(password)     #generate hash
            mycursor.execute("INSERT INTO loginInfo (Username, Password) VALUES (%s, %s);", [username, hash])  #do sql
            conn.commit()
            conn.close()
            return "Account Registered"

    conn.close()
    return "uh oh"

@app.route('/login/<username>/<password>',  methods = ['GET'])
def loginReal(username,password):

    conn = mysql.connector.connect( #con stands for connection to database
          host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
          user="UCMSocialMediaAp",                      # last p lost?
          password="mysqlpassword",
          database="UCMSocialMediaAp$default"
    )
    mycursor = conn.cursor()  # set up for database

    mycursor.execute("SELECT * FROM loginInfo")
    myresult = mycursor.fetchall()
    for row in myresult:
        if row[1] == username:
            # FOUND ISSUE ITS BECAUSE GENERATE PASSWORD HASH AUTOMATICALLY GENERATES A SALT AAAAAAAAA
            saltedPass = row[2]
            #minusSalt = (saltedPass.split("$",3))
            #return (minusSalt[1]+password)
            #return "here!"
            # r = ""
            # for a in minusSalt:
            #     r = r + ":::" + a
            # return (r)

            #return (minusSalt[2]+minusSalt[3] +" ::: " +y +":::" + minusSalt[1]+password)
            if check_password_hash(saltedPass, password):
                #inside = True
                conn.close()
                return username
                #return redirect(url_for('mainpage', username=username))
                #return "Welcome " + username


    return "incorrect password or username"


@app.route('/admin')
def admin():
    return render_template(admin.html)

@app.route('/mainpage/<username>')
def mainpage(username):
    return render_template('mainpage.html', username = username)

@app.route('/places/<username>')
def places(username):
    return render_template('places.html',username = username)

@app.route('/sports/<username>')
def sports(username):
    return render_template('sports.html',username = username)

@app.route('/classes/<username>')
def classes(username):
    return render_template('classes.html',username = username)

# @app.route('/mainpage/addpost/<username>', methods = ['POST'])  #POSTING DATA TO dashboard Database ()
# def mainpageAddPost(username):
#     obj = json.loads(request.data.decode('UTF-8'))                  #LOAD INFO FROM REQUEST BODY
#     username = obj["username"]                                      #LOAD username FROM REQUEST BODY
#     body = obj["body"]                                              #LOAD actual post message FROM REQUEST BODY
#     #times = time.strftime('%Y-%m-%d %H:%M:%S')                      #get todays date
#     times = datetime.datetime.now()
#     tag = obj["tag"] #added by Anirud 9:35pm 5/6/2024




#     conn = mysql.connector.connect(                 #connect to mysql server
#           host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
#           user="UCMSocialMediaAp",
#           password="mysqlpassword",
#           database="UCMSocialMediaAp$default"
#     )
#     mycursor = conn.cursor()                                             # set up for database

#     #mycursor.execute("SELECT * FROM dashboardPosts")
#     mycursor.execute("SELECT Id FROM loginInfo where Username = (%s);",[username])      #mycursor.execute(sql command)  lets you do sql commands
#     myIdRow = mycursor.fetchall()               # get info from sql command
#     for row in myIdRow:
#         myId = row[0]          # get userID from username
#     try:

#         #mycursor.execute("INSERT INTO dashboardPosts (userId, Post_Body,time_posted,rating) VALUES (%s, %s,%s,%s);", [myId, body,times,0])  #insert into database
#         mycursor.execute("INSERT INTO Posts (userId, Post_Body, time_posted, rating, replyTo, tag) VALUES (%s, %s,%s,%s, %s);" [myId, body, times, 0, 0, tag]) #added by Anirud 9:35pm 5/6/2024
#         conn.commit()  #commit to database

#         #mycursor.execute("SELECT * FROM dashboardPosts")
#         mycursor.execute("SELECT * FROM Posts")
#         posts = []
#         # for row in mycursor.fetchall():
#         #     '''
#         #     post = {
#         #             "Id": row[0],
#         #             "userId": row[1],
#         #             "Post_Body": row[2],
#         #             "time_posted": row[3],
#         #             "rating": row[4]
#         #         }
#         #     '''
#         #     post = {
#         #             "Id": row[0],
#         #             "userId": row[1],
#         #             "Post_Body": row[2],
#         #             "time_posted": row[3],
#         #             "rating": row[4],
#         #             "replyTo": row[5],
#         #             "tag": row[6]
#         #         }
#         #     posts.append(post)

#         #df = pd.DataFrame(posts)

#         #df.to_sql('YourTableName', x, if_exists="replace", index=False)
#         #df.to_sql('YourTableName', conn, if_exists='replace', index=False)


#         conn.close()    #close database

#         return json.dumps(posts, cls=CustomJSONEncoder)
#     except Exception as e: #something went wrong
#         conn.close()
#         return str(e)
#         #return "oops something went wrong"
#     #return "executed"

# @app.route('/mainpage/addpost', methods = ['GET'])  #getting data from database    #UNTESTED
# def mainpageGetPost():
#     conn = mysql.connector.connect( #con stands for connection to database    # connect to mysql database
#           host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
#           user="UCMSocialMediaAp",
#           password="mysqlpassword",
#           database="UCMSocialMediaAp$default"
#     )
#     mycursor = conn.cursor()  # set up for database
#     mycursor.execute("SELECT * FROM dashboardPosts")    # mysql command
#     myresult = mycursor.fetchall()      # get result from mysql command
#     allPosts = []  #make list of class objects where each object will be our rows
#     for post in myresult:

#         aPost = {                       # make each row in our table an object
#             "postID": post[0], #commented by Anirud 9:35pm
#             #"Id": post[0],
#             'userId' : post[1],
#             'Post_Body' : post[2],
#             'time_posted' : post[3],
#             'rating' : post[4], #added by Anirud 9:35pm 5/6/2024
#             'reply': post[5], #added by Anirud 9:35pm 5/6/2024
#             'tag': post[6] #added by Anirud 9:35pm 5/6/2024
#         }
#         allPosts.append(aPost) #append that object to our allPost list
#     return json.dumps(allPosts, cls=CustomJSONEncoder)

#     return jsonify(allPosts) #return that object for the javascript to read and put on the html

#//////////
@app.route('/post', methods = ['POST'])
def post():
    conn = mysql.connector.connect( #con stands for connection to database    # connect to mysql database
          host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
          user="UCMSocialMediaAp",
          password="mysqlpassword",
          database="UCMSocialMediaAp$default"
    )
    mycursor = conn.cursor()  # set up for database

    obj = json.loads(request.data.decode('UTF-8'))                  #LOAD INFO FROM REQUEST BODY
    username = obj["username"]                                      #LOAD username FROM REQUEST BODY
    body = obj["body"]
    times = datetime.datetime.now()
    replyTo = obj["replyTo"]
    tag = obj["tag"]

    myId = None
    mycursor.execute("SELECT Id FROM loginInfo where Username = (%s);",[username])      #mycursor.execute(sql command)  lets you do sql commands
    myIdRow = mycursor.fetchall()               # get info from sql command
    for row in myIdRow:
        myId = row[0]

    mycursor.execute("INSERT INTO Posts (userId, Post_Body,time_posted,rating,replyTo,tag) VALUES (%s, %s,%s,%s,%s,%s);", [myId, body,times,0,replyTo,tag])  #insert into database
    conn.commit()  #commit to database


    return "committed"

@app.route('/post/<username>/<tag>', methods = ['GET'])
def getPost(username,tag):
    conn = mysql.connector.connect( #con stands for connection to database    # connect to mysql database
          host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
          user="UCMSocialMediaAp",
          password="mysqlpassword",
          database="UCMSocialMediaAp$default"
    )
    mycursor = conn.cursor()  # set up for database



    mycursor.execute("SELECT * FROM Posts where tag = %s", [tag])    # mysql command
    myresult = mycursor.fetchall()      # get result from mysql command
    allPosts = []  #make list of class objects where each object will be our rows
    for post in myresult:

        aPost = {
            # make each row in our table an object
            "postID": post[0],
            'userId' : post[1],
            'Post_Body' : post[2],
            'time_posted' : post[3],
            'rating' : post[4],
            'Username' : username
        }
        allPosts.append(aPost) #append that object to our allPost list

    return jsonify(allPosts)







#//////////

@app.route('/like/<tag>', methods = ['PUT'])   #untested
def like(tag):

    conn = mysql.connector.connect( #con stands for connection to database    # connect to mysql database
        host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
        user="UCMSocialMediaAp",
        password="mysqlpassword",
        database="UCMSocialMediaAp$default"
    )
    mycursor = conn.cursor()

    obj = json.loads(request.data.decode('UTF-8'))
    change = obj["likeOrDislike"]
    change = int(change)
    username = obj["username"]

    if change == 1:
        posOrNeg = "pos"
    else:
        posOrNeg = "neg"

    mycursor.execute("select Id from loginInfo where Username = (%s)",[username])
    myIdRow = mycursor.fetchall()               # get info from sql command
    for row in myIdRow:
        myId = row[0]

    if (change == 1):
        mycursor.execute("select * from whoAlreadyLikedPSC where UserId = (%s)",[myId])
        myresult = mycursor.fetchall()
        for result in myresult:
            if (result[1] == tag and result[2] == "pos"):
                conn.close()
                return "already upvoted on this"
            if (result[1] == tag and result[2] == "neg"):
                mycursor.execute("delete from whoAlreadyLikedPSC where UserId = (%s)",[myId])

                conn.commit()

                mycursor.execute("Update placeSportClassRating SET likes = likes + %s WHERE name = %s",[change,tag])
                conn.commit()
                conn.close()
                return "downvote removed"

    if (change == -1):
        mycursor.execute("select * from whoAlreadyLikedPSC where UserId = (%s)",[myId])
        myresult = mycursor.fetchall()
        for result in myresult:
            if (result[1] == tag and result[2] == "neg"):
                conn.close()
                return "already downvoted this"
            if (result[1] == tag and result[2] == "pos"):
                mycursor.execute("delete from whoAlreadyLikedPSC where UserId = (%s)",[myId])
                conn.commit()
                mycursor.execute("Update placeSportClassRating SET likes = likes + %s WHERE name = %s",[change,tag])
                conn.commit()
                conn.close()
                return "upvote removed"

    mycursor.execute("Update placeSportClassRating SET likes = likes + %s WHERE name = %s",[change,tag])
    conn.commit()


    mycursor.execute("insert into whoAlreadyLikedPSC (UserId,PSCName,likeOrDislike) Values(%s,%s,%s)", [myId,tag,posOrNeg])
    conn.commit()
    conn.close()

    return "Completed"

@app.route('/like/<tag>', methods = ['GET'])
def getLike(tag):
    conn = mysql.connector.connect( #con stands for connection to database    # connect to mysql database
        host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
        user="UCMSocialMediaAp",
        password="mysqlpassword",
        database="UCMSocialMediaAp$default"
    )
    mycursor = conn.cursor()

    mycursor.execute("select * from placeSportClassRating where name = %s", [tag])

    myresult = mycursor.fetchall()      # get result from mysql command
    allLikes = []  #make list of class objects where each object will be our rows
    for PSC in myresult:
        aPost = {                       # make each row in our table an object
            'likes': PSC[2]
        }
        allLikes.append(aPost) #append that object to our allPost list

    return jsonify(allLikes)

@app.route('/comments/<username>/<tag>')
def getComments(username, tag):
    return render_template('comments.html', username = username)



if __name__ == '__main__':
    #admin_instance.init_app(app)
    app.run(port=5000, debug = True)


