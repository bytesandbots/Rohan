import flask
import psycopg2

def addinfo(info):

    fname=info.get("fname")
    lname=info.get("lname")
    city=info.get("city")
    state=info.get("statee")
    country=info.get("country")
    age=info.get("age")
    dob=info.get("dob")

    Username=info.get("username")
    ID=info.get("ids")
    Password=info.get("passwords")

    
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("select * from person_information where firstname='Rohan';")
    info= cursor.fetchall()
    cursor.execute("INSERT INTO person_information (Firstname, Lastname, city, statee, country, age, dob)VALUES (%s, %s, %s, %s, %s, %s, %s);",
                   (fname, lname, city, state, country, age, dob))
    conn.commit()

    conn.close()

app = flask.Flask(__name__)
app.config['SECRET_KEY']= 'jhgfds'
URL='postgresql://mathobotix.irvine.lab:VBQRvxA2dP9i@ep-shrill-hill-95052366.us-west-2.aws.neon.tech/neondb?sslmode=require'
@app.route("/login")
def login():
    return flask.render_template("login.html")
@app.route("/signup")
def signup():
    return flask.render_template("signup.html")
@app.route("/")
def home_view():
    if flask.session.get("is_logged_in"):
        return flask.render_template("index.html")
    else:
        return flask.render_template("login.html")
        




@app.route("/infolocation", methods=["POST"])
def infolocation():
    info=flask.request.form
    
    addinfo(info)

@app.route("/logins", methods=["POST"])
def logins():
    info=flask.request.form
    username=info.get("uname")
    password=info.get("psw")

    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("select * from login where username=%s;", (username,))
    info= cursor.fetchall()
    if info == []:
        return "incorrect username or password"
    else:
        if password == info[0][3]:
            flask.session["is_logged_in"]=True
            return flask.render_template("index.html")
        else:
            return "incorrect username or password"
@app.route("/signout")
def signout():
    flask.session.clear()
    return flask.render_template("login.html")



    

