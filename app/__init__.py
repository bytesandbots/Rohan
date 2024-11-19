import flask
import psycopg2
import bcrypt 
import datetime


#addinfo
def addinfo(info):
    
    fname=info.get("fname")
    lname=info.get("lname")
    city=info.get("city")
    state=info.get("statee")
    country=info.get("country")
    age=info.get("age")
    dob=info.get("dob")
    role=info.get("role")
    
    username=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("select * from person_information where username=%s;", (username,))
    info= cursor.fetchall()
    if info == []:

        cursor.execute("INSERT INTO person_information (username, Firstname, Lastname, city, statee, country, age, dob, role)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                       (username, fname, lname, city, state, country, age, dob, role))
        conn.commit()
    else:
        cursor.execute("update person_information set Firstname=%s, Lastname=%s, city=%s, statee=%s, country=%s, age=%s, dob=%s, role=%s where username=%s",
                       ( fname, lname, city, state, country, age, dob, role, username))
        conn.commit()
    conn.close()
    return flask.redirect("/")

app = flask.Flask(__name__)
app.config['SECRET_KEY']= 'jhgfds'
URL='postgresql://mathobotix.irvine.lab:VBQRvxA2dP9i@ep-shrill-hill-95052366.us-west-2.aws.neon.tech/neondb?sslmode=require'
salt = bcrypt.gensalt() 

#deleting your account
@app.route("/deleteuser")
def deleteuser():
    username=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()    
    cursor.execute("DELETE FROM login WHERE username = %s ",
                       (username, ))
    cursor.execute("DELETE FROM person_information WHERE username = %s ",
                       (username, ))
    conn.commit()
    conn.close()

    
    return flask.redirect("/signout")
    

    
    return flask.redirect("/signout")


#def clearhrs
@app.route("/clearhrs")
def clearhrs():
    username=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()    
    cursor.execute("DELETE FROM timeworked WHERE username = %s ",
                       (username, ))

    conn.commit()
    conn.close()

    
    return flask.redirect("/yourinfo")
    

    
#admin check
def admincheck():
    if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        cursor.execute("select role from login where username=%s;", (username,))
        info= cursor.fetchall()
        admin=False
        if (info!=None):
            if (info[0][0] == "Admin"):
                admin=True
        return admin
                   
                
#render admin page
@app.route("/admin")
def admin():
     if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        cursor.execute("select role from login where username=%s;", (username,))
        info= cursor.fetchall()
        print (info)
        admin=False
        if (info!=None):
            if (info[0][0] == "Admin"):
                admin=True
        cursor.execute("select * from person_information;")
        info= cursor.fetchall()
        total=totaltotalhrs()
        if info ==[]:
            return flask.render_template("admin.html", datainfo=info, filled=False, totaltotal=total)
        info=info[0]
        for collum in info:
            if collum == "":
                return flask.render_template("admin.html", datainfo=info, filled=False, totaltotal=total)
            

        return flask.render_template("/admin.html", admin=admincheck())







        

@app.route("/login")
def login():
    if flask.session.get("is_logged_in"):
        return flask.redirect("/")
    else:
        return flask.render_template("login.html")
@app.route("/signup")
def signup():
    if flask.session.get("is_logged_in"):
        return flask.render_template("homepage.html", datainfo=[])
    else:
        return flask.render_template("signup.html")

@app.route("/infoform")
def infoform():
    if flask.session.get("is_logged_in"):
        admincheck
        return flask.render_template("info_form.html", admin=admincheck())
    else:
        return flask.render_template("login.html")
    
@app.route("/yourinfo")
def yourinfo():
    if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        cursor.execute("select * from person_information where username=%s;", (username,))
        info= cursor.fetchall()
        total=totaltotalhrs()
        if info ==[]:
            return flask.render_template("your_info.html", datainfo=info, filled=False, totaltotal=total)
        info=info[0]
        for collum in info:
            if collum == "":
                return flask.render_template("your_info.html", datainfo=info, filled=False, totaltotal=total)
            
        return flask.render_template("your_info.html", datainfo=info, filled=True, totaltotal=total, admin=admincheck())
    else:
        return flask.render_template("login.html")    
    
@app.route("/")
def homepage():
    if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        cursor.execute("select * from person_information where username=%s;", (username,))
        info= cursor.fetchone()
        filled=True
        
        if info ==[]:
            filled=False
        cursor.execute("select timeout from timeworked where username=%s order by timein DESC;", (username,))
        times=cursor.fetchone()

        checkedin=False
        if times==None:
            checkedin=False


        else :
            times = times[0]
            if times==None:
                checkedin=True
        print(times)
        print(checkedin)

        
        
   
        return flask.render_template("homepage.html", datainfo=info, filled=filled, start=checkedin, admin=admincheck())

    else:
        return flask.render_template("login.html")



#time worked

def timein():
    from datetime import datetime
    timeins = datetime.now()
    return timeins



    
def timeout():
    from datetime import datetime
    timeouts = datetime.now()
    return timeouts

def total_hrs():
    total = timeout - timein
    return total




#recording timein
@app.route("/addtime", methods=["POST"])
def addtime():
    username=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()

    t=timein()
    date=datetime.datetime.now().date()
    cursor.execute("INSERT INTO timeworked (username, timein, timeout, total, dates)VALUES (%s, %s, %s, %s, %s);",
                           (username, t, None, None, date))
    conn.commit()
    return flask.redirect("/")

#recording time out
@app.route("/addtimeout", methods=["POST"])
def addtimeout():
    username=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()

    cursor.execute("select timein from timeworked where username=%s order by timein DESC;", (username,))
    timein=cursor.fetchone()
    if timein==None:
            checkedin=True

        
    if (timein == None):
        return flask.redirect("/")
    else :
        timein = timein[0]
        

    
    to=timeout()

    total=to-timein
    date=datetime.datetime.now().date()
    cursor.execute("UPDATE timeworked SET timeout = %s, total= %s WHERE username = %s and timein = %s;",
                           (to,total.seconds/60, username, timein))
    conn.commit()
    return flask.redirect("/")


#recording total hrs
@app.route("/totalhrs", methods=["POST"])
def totalhrs():
    username=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()

    cursor.execute("select total from timeworked where username=%s order by timein DESC;", (username,))
    timein=cursor.fetchone()[0]

    
    total=timeout-timein()
    date=datetime.datetime.now().date()
    cursor.execute("UPDATE timeworked SET total = %s WHERE username = %s and timein = %s and timeout = %s;",
                           (total))

#adding total hrs in total
def totaltotalhrs():
    username=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("select total from timeworked where username=%s", (username, ))
    total=cursor.fetchall()
    totaltotal=0
    for i in total:
        if i[0]==None:
            continue
        else:
            totaltotal+=i[0]
    print (totaltotal/60)
    return totaltotal/60


@app.route("/infolocation", methods=["POST"])
def infolocation():
    info=flask.request.form
    print("here")
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


    


    

