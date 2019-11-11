from flask import Flask, render_template, url_for, flash, redirect, session
#from flask_sqlalchemy import SQLAlchemy
from flask import request
from datetime import datetime
# from dbconnect import connection
import mysql.connector
from werkzeug import secure_filename
import re
import os

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'fd5135666bac8fe98033e86b90251504'
UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
mydb = mysql.connector.connect(
    host="localhost",
    user="aru",
    passwd="aru12345678",
    database="wireless"
)
mycursor = mydb.cursor(buffered=True)


@app.route("/masteru")
def user():
    return render_template('user/usermaster.html')


@app.route("/mastera")
def admin():
    return render_template('admin/adminmaster.html')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',  methods=['GET', 'POST'])


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home_post():
    if request.method == 'POST' and 'wnduser' in request.form and 'wndpass' in request.form:
        wnduser = request.form['wnduser']
        wndpass = request.form['wndpass']
        try:
            myuser = """select * from accounts where password = %s and username = %s """
            mycursor.execute(myuser, (wndpass, wnduser))
            account = mycursor.fetchone()
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
            # Redirect to home page
                if(account[3] == "user"):
                    return render_template('user/userhome.html')
                else:
                    return render_template('admin/adminhome.html')
            else:
                # Account doesnt exist or username/password incorrect
                erroruser = "Incorrect username or password"
                return render_template('home.html',  methods=['GET', 'POST'], erroruser=erroruser)
        except Exception as e:
            return(str(e))


@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('home'))


@app.route("/register")
def register():
    return render_template('registration.html')


@app.route("/register", methods=['POST'])
def register_post():
        #global fullname, email, mobile, types, password
    global errorname
    email = request.form['email']
    fullname = request.form['fullname']
    x = any(char.isdigit() for char in fullname)
    if(x == True):
        errorname = "Number not allowed!!"
        nameerror = True
        return render_template('registration.html', errorname=errorname)
    elif(len(fullname) == 0):
        errorname = "please type"
        nameerror = True
        return render_template('registration.html', errorname=errorname)
    else:
        mobile = request.form['mobile']
        y = mobile.isdigit()
        if(y == False):
            errormob = "No letters!!"
            return render_template('registration.html', errormob=errormob)
        elif(len(mobile) < 10 or len(mobile) > 10):
            errormob = "10 digits needed!!"
            return render_template('registration.html', errormob=errormob)
        else:
            types = request.form['type']
            if(types == "Select-Type"):
                errortype = "choose a type!"
                return render_template('registration.html', errortype=errortype)
            else:
                password = request.form['password']
            if not password:
                errorpass = "password should not be blank!!"
                return render_template('registration.html', errorpass=errorpass)
            elif(len(password) < 8):
                errorpass = "minimum 8 chars required!!"
                return render_template('registration.html', errorpass=errorpass)
            else:
                confirm = request.form['confirm']
                if(password != confirm):
                    errorconfirm = "password doesnot match!!"
                    return render_template('registration.html', errorconfirm=errorconfirm)
                else:
                    try:
                        mySql = """INSERT INTO register (name, email, phone, types, password) 
                                VALUES (%s,%s,%s,%s,%s) 
                                """, (fullname, email, mobile, types, password)
                        mycursor.execute(*mySql)
                        mydb.commit()
                        mySql1 = """INSERT INTO accounts (username, password, type) 
                                VALUES (%s,%s,%s) 
                                """, (fullname, password, types)
                        mycursor.execute(*mySql1)
                        mydb.commit()


                        # return("okay")
                        return render_template('registration.html', ok="Successful")
                    except Exception as e:
                        return(str(e))


@app.route("/display")
def display():
    try:
        mydisplay = """select file,ms,type from slidetest where active = %s order by id desc"""
        mycursor.execute(mydisplay, (1, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        totaltime = """select sum(seconds)+4 from slidetest where active = %s """
        mycursor.execute(totaltime, (1, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        file = []

        return render_template('display.html', disp = disps, times = time[0])
    except Exception as e:
        return(str(e))

@app.route("/testdisplay")
def testdisplay():
    try:
        global disps
        mydisplay = """select * from slidetest"""
        mycursor.execute(mydisplay)
        display = mycursor.fetchall()
        disps = [row for row in display]
        # print(disps)
        # mycount = mycursor.execute("""select count(*) from slidetest""")
        # mycursor.execute(mycount)
        # count =mycursor.fetchone()
        # x = count[0]
        # print("x is" + str(x))
        # disps = []
        # for row in display:
        #     print(row[0])
        #     disps = row[0]
        # print(disps)
        return render_template('test_disp.html', disp=disps)
    except Exception as e:
        return(str(e))


@app.route("/testdisplay", methods=['POST'])
def testdisplay_post():
    global test_msg
    try:
        ids = request.form['idsel']
        act = request.form['activesel']
        if ids == "select":
            test_msg = "please select id"
            return render_template('test_disp.html', disp=disps, msg=test_msg)
        else:
            mydisplay = """update slidetest set active = %s where id = %s"""
            mycursor.execute(mydisplay, (act, ids, ))
            mydb.commit()
            test_msg = "Successful"
            return render_template('test_disp.html', disp=disps, msg=test_msg)
    except Exception as e:
        test_msg = "an error occoured"
        return render_template('test_disp.html', disp=disps, msg=test_msg)


@app.route("/addnewnotice")
def adminadd():
    return render_template('admin/add.html')

@app.route("/addnewnotice", methods=['POST'])
def imgform():
    file = request.files['imgfiles']
    if file:
        now = datetime.now().strftime("%d%m%Y%H%M%S")
        dept = request.form['dept']
        dseconds = request.form['duration']
        if dseconds == '':
            return render_template('admin/add.html',msg = "please add duration")
        else:
            ms = int(dseconds) * 1000    
            category = "image"
            filename = secure_filename(file.filename)
            files = now + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],files))
            mySql = """INSERT INTO slidetest (file, active, ms, seconds, type) 
                                VALUES (%s,%s,%s,%s,%s) 
                                """, (files, 1, ms, dseconds, category)
            mycursor.execute(*mySql)
            mydb.commit()
            return render_template('admin/add.html',msg = "Successful")
    else:
        return render_template('admin/add.html',msg = "please select a file")   


@app.route("/requests")
def adminrequest():
    return render_template('admin/requests.html')


@app.route("/ahome")
def adminhome():
    return render_template('admin/adminhome.html')


@app.route("/urequest")
def userrequest():
    return render_template('user/userrequest.html')


@app.route("/uhome")
def userhome():
    return render_template('user/userhome.html')


if __name__ == '__main__':
    app.run(debug=True)
