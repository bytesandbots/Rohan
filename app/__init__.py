import flask
import psycopg2
import bcrypt 
import datetime
from datetime import date
import uuid
import json

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
    homeaddress=info.get("adress")
    email=info.get("email")
    phonenumber=info.get("phonenumber")
    
    
    username=flask.session.get("username")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("select * from person_information where username=%s;", (username,))
    info= cursor.fetchall()
    if info == []:

        cursor.execute("INSERT INTO person_information (username, Firstname, Lastname, city, statee, country, age, dob, role, adress, email, phonenumber)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                       (username, fname, lname, city, state, country, age, dob, role, homeaddress, email, phonenumber))
        conn.commit()
    else:
        cursor.execute("update person_information set Firstname=%s, Lastname=%s, city=%s, statee=%s, country=%s, age=%s, dob=%s, role=%s, adress=%s, email=%s, phonenumber=%s where username=%s",
                       ( fname, lname, city, state, country, age, dob, role, homeaddress, email, phonenumber, username))
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
    

    


#mentor check
def mentorcheck():
    if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        cursor.execute("select role from person_information where username=%s;", (username,))
        info= cursor.fetchall()
        mentor=False
        if (info!=None):
            if (info[0][0] == "mentor"):
                mentor=True
        return mentor

#render mentor page
@app.route("/student")
def student():
     if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        
        cursor.execute("select role from person_information where username=%s;", (username,))

        info= cursor.fetchall()

        mentor=False
        if (info!=None):
            if (info[0][0] == "mentor"):
                mentor=True
        info= cursor.fetchall()
        
     
          

        return flask.render_template("/student.html", admin=admincheck, mentor=mentorcheck())
#searching students
@app.route("/searchstudents", methods=["POST"])
def searchstudent():
    info=flask.request.form.get("studentsearch")
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    
    info = "%"+info+"%"
    cursor.execute("select fname, lname, studentid from studentinfo where fname LIKE %s;", (info,))
    info= cursor.fetchall()




    
    return flask.render_template("/student.html", admin=admincheck(), mentor=mentorcheck(), searchstudent=info)

#creating a page for each individual student
@app.route("/studentpage/<studentid>")
def studentpage(studentid):
    
    if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        flask.session["takeid"]= studentid
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        cursor.execute("select * from studentinfo where studentid=%s;", (studentid,))
        info= cursor.fetchone()
        cursor.execute("select * from studentdebrief where studentid=%s;", (studentid,))
        debriefs = cursor.fetchall()
        if debriefs == []:
            debriefs = False
        cursor.execute("select * from studentreport where studentid=%s;", (studentid,))
        reports = cursor.fetchall()
        cursor.execute("select * from checkin where studentid=%s;", (studentid,))
        checkedin = cursor.fetchall()
        if checkedin ==[]:
            checksin = False
        cursor.execute("select * from youtubevideos where studentid=%s order by videoid desc;", (studentid,))
        videos = cursor.fetchall()
        videosuploaded = True
        if videos == []:
            videosuploaded = False
        conn.close()
        if info ==[]:
            return flask.render_template("/studentpage.html", found = False, admin = admincheck(), info = [], mentor=mentorcheck(), debriefs = [], reports = [] ) 
        return flask.render_template("/studentpage.html", videos=videos, videosuploaded = videosuploaded, found =True, admin = admincheck(), info = info, mentor=mentorcheck(), debriefs = debriefs, reports = reports )            

@app.route("/checkin/<studentid>")
def checkin(studentid):
    if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        studentid = flask.session.get("takeid")
        checkintime = datetime.datetime.now()
        cursor.execute("INSERT INTO checkin (studentid, checkintime)VALUES (%s, %s);",(studentid, checkintime))
        conn.commit()
        conn.close()
        return flask.redirect("/studentpage/" + studentid)

@app.route("/checkout/<studentid>")
def checkout(studentid):
    if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        studentid = flask.session.get("takeid")
        cursor.execute("DELETE FROM checkin WHERE studentid = %s ",(studentid, ))
        conn.commit()
        conn.close()
        return flask.redirect("/studentpage/" + studentid)

        
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
        admin=False
        if (info!=None):
            if (info[0][0] == "Admin"):
                admin=True
        info= cursor.fetchall()
        
          

        return flask.render_template("/admin.html", admin=admincheck(), mentor=mentorcheck())
 

@app.route("/creatementor")
def creatementor():
    if flask.session.get("is_logged_in"):
        username=flask.session.get("username")
        conn=psycopg2.connect(URL)
        cursor=conn.cursor()
        cursor.execute("select username from login where username=%s;", (username,))
        info = cursor.fetchall()
        cursor.execute("UPDATE person_information set role = 'Admin' where username=%s;",(project, reportdate, classcategory, studentid))
        conn.commit()
        conn.close()
        return flask.redirect("/admin")


        

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
        return flask.render_template("info_form.html", admin=admincheck(), mentor=mentorcheck())
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
        if info ==[]:
            return flask.render_template("your_info.html", datainfo=info, filled=False)
   
        info=info[0]
        for collum in info:
            if collum == "":
                return flask.render_template("your_info.html", datainfo=info, filled=False, totaltotal=total)
            
        return flask.render_template("your_info.html", datainfo=info, filled=True, mentor=mentorcheck(), admin=admincheck())
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

        flask.session["userinfo"]= json.dumps(info)
        filled=True
        
        if info ==[]:
            filled=False


        
        
   
        return flask.render_template("homepage.html", datainfo=info, filled=filled,mentor=mentorcheck(), admin=admincheck())

    else:
        return flask.render_template("login.html")
#addstudent
@app.route("/enrollment")
def enrollment():
    userinfo=json.loads(flask.session["userinfo"])
    return flask.render_template("enrollment.html", datainfo=userinfo, admin=admincheck(), mentor=mentorcheck())
    
@app.route("/submitenrollment", methods=["POST"])
def submitenrollment():
    info=flask.request.form
    userinfo=json.loads(flask.session["userinfo"])
    fname=info.get("fname")
    lname=info.get("lname")
    dob=info.get("dob")
    grade=info.get("grade")
    school=info.get("school")
    studentid=int(uuid.uuid4())
    
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("INSERT INTO studentinfo (fname, lname, dob, grade, school, studentid)VALUES (%s, %s, %s, %s, %s, %s);",
                       (fname, lname, dob, grade, school, studentid))
    conn.commit()
    conn.close()
    return flask.render_template("homepage.html", datainfo=userinfo, admin=admincheck(), mentor=mentorcheck())    
    


@app.route("/infolocation", methods=["POST"])
def infolocation():
    
    info=flask.request.form
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    cursor.execute("insert * from login where username=%s;", (username,))
    info= cursor.fetchall()
#deleting debriefs
@app.route("/deletedebrief/<debriefid>")
def deletedebrief(debriefid):
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    studentid = flask.session.get("takeid")
    flask.session["takeid"]= studentid

    
    cursor.execute("DELETE FROM studentdebrief where studentid = %s and debriefid=%s;", (studentid, debriefid,))
    conn.commit()
    conn.close()
    return flask.redirect("/studentpage/" + studentid)

#taking info from the debriefs
@app.route("/debrieflocation", methods=["POST"])
def debrieflocation():
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    studentid = flask.session.get("takeid")
    info=flask.request.form
    reportdate = date.today()
    project = info.get("project")
    flask.session["takeid"]= studentid
    cursor.execute("INSERT INTO studentdebrief (mentorname, reportdate, report, studentid, project)VALUES (%s, %s, %s, %s, %s);", (info.get("mentorname"), reportdate, info.get("report"), studentid, project))
    conn.commit()


    conn.close()
    checkout(studentid)
    return flask.redirect("/studentpage/" + studentid)

#Uploading youtube videos for each student
@app.route("/videolocation", methods=["POST"])
def videolocation():
    
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    studentid = flask.session.get("takeid")
    info=flask.request.form
    flask.session["takeid"]= studentid
    
    videourl = info.get("videolink")
    cuturl= videourl[videourl.index("v=")+2:]
    videourl = cuturl[:cuturl.index("&")]

    cursor.execute("INSERT INTO youtubevideos (studentid, videolink)VALUES (%s, %s);", (studentid, videourl))
    conn.commit()
    conn.close()
    return flask.redirect("/studentpage/" + studentid)

@app.route("/reportlocation", methods=["POST"])
def reportlocation():
    conn=psycopg2.connect(URL)
    cursor=conn.cursor()
    
    studentid = flask.session.get("takeid")
    info=flask.request.form
    flask.session["takeid"]= studentid
    cursor.execute("select * from studentreport where studentid = %s;", (studentid,))
    student = cursor.fetchone()
    
    cursor.execute("select project, reportdate from studentdebrief order by reportdate desc;", (studentid, ))
    project, reportdate = cursor.fetchone()#('classcategory', 'parent')
    classcategory =info.get("classcategory")
    if student == None:
        cursor.execute("INSERT INTO studentreport (studentid, project, lastclass, classcategory)VALUES ( %s, %s, %s, %s);",( studentid, project, reportdate, classcategory))
        conn.commit()
    else:
        cursor.execute("UPDATE studentreport set project = %s, lastclass = %s, classcategory =%s where studentid=%s;",(project, reportdate, classcategory, studentid))
    conn.commit()
        
    conn.close()
    return flask.redirect("/studentpage/" + studentid)




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



    


    

