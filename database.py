import psycopg2

def addinfo():
    cursor.execute("INSERT INTO person_information (Firstname, Lastname, city, age, dob)VALUES ('Rohan', 'uhguisdhg', 'wrfgysegfusidhgfiulewyti', '99', '12/34/5678');")
    conn.commit()

def getinfo():
    cursor.execute("select * from information")
    searchinfo= cursor.fetchall()
    for searchinfo in info:
        for information in searchinfo:
            print(information)




URL='postgresql://mathobotix.irvine.lab:VBQRvxA2dP9i@ep-shrill-hill-95052366.us-west-2.aws.neon.tech/neondb?sslmode=require'
conn=psycopg2.connect(URL)
cursor=conn.cursor()
cursor.execute("select * from login where firstname='Rohan';")
info= cursor.fetchall()
for userdata in info:
    for information in userdata:
        print(information)
#addinfo()
