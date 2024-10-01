import flask
import psycopg2
import bcrypt 


#addinfo
def addinfo(info):
    
    fname=info.get("fname")
    lname=info.get("lname")
    city=info.get("city")
    state=info.get("statee")
    country=info.get("country")
    age=info.get("age")
    dob=info.get("dob")

    username=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("select * from person_information where username=%s;", (username,))
    info= cursor.fetchall()
    if info == []:

        cursor.execute("INSERT INTO person_information (username, Firstname, Lastname, city, statee, country, age, dob)VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                       (username, fname, lname, city, state, country, age, dob))
        conn.commit()
    else:
        cursor.execute("update person_information set Firstname=%s, Lastname=%s, city=%s, statee=%s, country=%s, age=%s, dob=%s where username=%s",
                       ( fname, lname, city, state, country, age, dob, username))
        conn.commit()
    conn.close()
    return flask.redirect("/")

app = flask.Flask(__name__)
app.config['SECRET_KEY']= 'jhgfds'
URL='postgresql://mathobotix.irvine.lab:VBQRvxA2dP9i@ep-shrill-hill-95052366.us-west-2.aws.neon.tech/neondb?sslmode=require'
salt = bcrypt.gensalt() 

#deleting your account
def deleteuser():
    sername=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("select * from person_information where username=%s;", (username,))
    info= cursor.fetchall()
    
    cursor.execute("DELETE FROM person_information (username, Firstname, Lastname, city, statee, country, age, dob)VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                       (username, fname, lname, city, state, country, age, dob)





    return flask.render_template("login.html")

    
@app.route("/login")
def login():
    if flask.session.get("is_logged_in"):
        return flask.render_template("homepage.html")
    else:
        return flask.render_template("login.html")
@app.route("/signup")
def signup():
    if flask.session.get("is_logged_in"):
        return flask.render_template("homepage.html")
    else:
        return flask.render_template("signup.html")

@app.route("/infoform")
def infoform():
    if flask.session.get("is_logged_in"):
        return flask.render_template("info_form.html")
    else:
        return flask.render_template("login.html")
@app.route("/")
def homepage():
    if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        cursor.execute("select * from person_information where username=%s;", (username,))
        info= cursor.fetchall()

        if info ==[]:
            return flask.render_template("homepage.html", datainfo=info, filled=False)
        info=info[0]
        for collum in info:
            if collum == "":
                return flask.render_template("homepage.html", datainfo=info, filled=False)
            
        return flask.render_template("homepage.html", datainfo=info, filled=True)
    else:
        return flask.render_template("login.html")





@app.route("/infolocation", methods=["POST"])
def infolocation():
    info=flask.request.form
    
    return addinfo(info)


#signup
@app.route("/signup_page", methods=["POST"])
def signups():
    info=flask.request.form
    username=info.get("email")
    password=info.get("psw")

#hashing function    
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("select * from login where username=%s;", (username,))
    info= cursor.fetchall()
    if info != []:
        return "username taken"
    else:
        bytes = password.encode('utf-8') 
        hash = bcrypt.hashpw(bytes, salt)
        hash=hash.decode("utf-8")
        cursor.execute("INSERT INTO login (username, passwords)VALUES (%s, %s);",(username, hash))
        conn.commit()
        
        return flask.render_template("login.html")


#login    
@app.route("/logins", methods=["POST"])
def logins():
    info=flask.request.form
    username=info.get("uname")
    password=info.get("psw")

#hash verification
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("select * from login where username=%s;", (username,))
    info= cursor.fetchall()
    if info == []:
        return "incorrect username or password"
    else:
        hash = info[0][2]
        hash=hash.encode("utf-8")
        userBytes = password.encode('utf-8') 
        if bcrypt.checkpw(userBytes, hash)  :
            flask.session["is_logged_in"]=True
            flask.session["username"]=username
            return flask.redirect("/")
        else:
            return "incorrect username or password"

#signout
@app.route("/signout")
def signout():
    flask.session.clear()
    return flask.render_template("login.html")



    

