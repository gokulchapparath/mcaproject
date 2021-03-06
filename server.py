from flask import Flask, render_template, url_for, flash, redirect, session
#from flask_sqlalchemy import SQLAlchemy
from flask import request
from datetime import datetime
from pdf2image import convert_from_path
# from dbconnect import connection
import mysql.connector
from werkzeug.utils import secure_filename
#from werkzeug import secure_filename
import re
import os
import socket
import urllib.request

def get_my_ip_address(remote_server="google.com"):
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        """
        Return the/a network-facing IP number for this system.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s: 
            s.connect((remote_server, 80))
            return s.getsockname()[0]
    except:
        return False

if(get_my_ip_address() == False):
    ip = '127.0.0.1'
else:    
    ip = get_my_ip_address()

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'fd5135666bac8fe98033e86b90251504'
UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
mydb = mysql.connector.connect(
    host="localhost",
    user="mca",
    passwd="mca12345678",
    database="wireless"
)
mycursor = mydb.cursor(buffered=True)

# @app.route("/masteru")
# def user():
#     return render_template('user/usermaster.html')


# @app.route("/test")
# def user():
#     return render_template('test.html')


# @app.route("/mastera")
# def admin():
#     return render_template('admin/adminmaster.html')


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
                    name = session['username']
                    return render_template('user/userhome.html', names = name.capitalize())
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
    global errorname
    email = request.form['email']
    fullname = request.form['fullname']    
    myemail = """select count(email) from register where email = %s"""
    mycursor.execute(myemail, (email, ))
    emails = mycursor.fetchone()
    x = any(char.isdigit() for char in fullname)
    if(x == True):
        errorname = "Number not allowed!!"
        nameerror = True
        return render_template('registration.html', errorname=errorname)
    elif(len(fullname) == 0):
        errorname = "please type"
        nameerror = True
        return render_template('registration.html', errorname=errorname)        
    elif(emails[0] > 0):
        errormail = "exsiting email found"
        nameerror = True
        return render_template('registration.html', errormail=errormail)
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
                                """, (fullname, email, mobile, types.lower(), password)
                        mycursor.execute(*mySql)
                        mydb.commit()
                        mySql1 = """INSERT INTO accounts (username, password, type) 
                                VALUES (%s,%s,%s) 
                                """, (fullname, password, types.lower())
                        mycursor.execute(*mySql1)
                        mydb.commit()
                        # return("okay")
                        return render_template('registration.html', ok="Successful")
                    except Exception as e:
                        return(str(e))


@app.route("/display")
def display():
        mydisplay = """select file,ms,type from slidetest where active = %s and status = %s and deleted = %s order by id desc"""
        mycursor.execute(mydisplay, (1, 1, 0, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        totaltime = """select sum(seconds)+4 from slidetest where active = %s and status = %s and deleted = %s """
        mycursor.execute(totaltime, (1, 1, 0, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        file = []
        return render_template('display.html', disp = disps, times = time[0])

@app.route("/mca")
def mca():
        mydisplay = """select file,ms,type from slidetest where active = %s and status = %s and deleted = %s and mca = %s order by id desc"""
        mycursor.execute(mydisplay, (1, 1, 0, 1, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        totaltime = """select sum(seconds)+4 from slidetest where active = %s and status = %s and deleted = %s and mca = %s """
        mycursor.execute(totaltime, (1, 1, 0, 1, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        file = []
        return render_template('screens/mca.html', disp = disps, times = time[0])        

@app.route("/screen1")
def sc1():
        mydisplay = """select file,ms,type from slidetest where active = %s and status = %s and deleted = %s and screen1 = %s order by id desc"""
        mycursor.execute(mydisplay, (1, 1, 0, 1, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        totaltime = """select sum(seconds)+4 from slidetest where active = %s and status = %s and deleted = %s and screen1 = %s """
        mycursor.execute(totaltime, (1, 1, 0, 1, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        file = []
        return render_template('screens/screen1.html', disp = disps, times = time[0])

@app.route("/screen2")
def sc2():
        mydisplay = """select file,ms,type from slidetest where active = %s and status = %s and deleted = %s and screen2 = %s order by id desc"""
        mycursor.execute(mydisplay, (1, 1, 0, 1, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        totaltime = """select sum(seconds)+4 from slidetest where active = %s and status = %s and deleted = %s and screen2 = %s """
        mycursor.execute(totaltime, (1, 1, 0, 1, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        file = []
        return render_template('screens/screen2.html', disp = disps, times = time[0]) 

@app.route("/screen3")
def sc3():
        mydisplay = """select file,ms,type from slidetest where active = %s and status = %s and deleted = %s and screen3 = %s order by id desc"""
        mycursor.execute(mydisplay, (1, 1, 0, 1, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        totaltime = """select sum(seconds)+4 from slidetest where active = %s and status = %s and deleted = %s and screen3 = %s """
        mycursor.execute(totaltime, (1, 1, 0, 1, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        file = []
        return render_template('screens/screen3.html', disp = disps, times = time[0]) 

@app.route("/screen4")
def sc4():
        mydisplay = """select file,ms,type from slidetest where active = %s and status = %s and deleted = %s and screen4 = %s order by id desc"""
        mycursor.execute(mydisplay, (1, 1, 0, 1, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        totaltime = """select sum(seconds)+4 from slidetest where active = %s and status = %s and deleted = %s and screen4 = %s """
        mycursor.execute(totaltime, (1, 1, 0, 1, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        file = []
        return render_template('screens/screen4.html', disp = disps, times = time[0]) 

@app.route("/screen5")
def sc5():
        mydisplay = """select file,ms,type from slidetest where active = %s and status = %s and deleted = %s and screen5 = %s order by id desc"""
        mycursor.execute(mydisplay, (1, 1, 0, 1, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        totaltime = """select sum(seconds)+4 from slidetest where active = %s and status = %s and deleted = %s and screen5 = %s """
        mycursor.execute(totaltime, (1, 1, 0, 1, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        file = []
        return render_template('screens/screen5.html', disp = disps, times = time[0]) 

@app.route("/testdisplay")
def testdisplay():
    try:
        global disps
        mydisplay = """select * from slidetest where deleted = %s"""
        mycursor.execute(mydisplay, (0, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
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
    mca = screen1 = screen2 = screen3 = screen4 = screen5 = 0
    if request.form['formbtn'] == 'img':
        file = request.files['imgfiles']
        if file:
            now = datetime.now().strftime("%d%m%Y%H%M%S")
            dseconds = request.form['duration']
            if dseconds == '':
              return render_template('admin/add.html',msg = "please add duration")
            else:
                op=request.form.getlist('screen')
                for x in op:
                    if(x == "mca"):
                        mca = 1
                    if(x == "screen1"):
                        screen1 = 1
                    if(x == "screen2"):
                        screen2 = 1
                    if(x == "screen3"):
                        screen3 = 1
                    if(x == "screen4"):
                        screen4 = 1
                    if(x == "screen5"):
                        screen5 = 1                            
                ms = int(dseconds) * 1000    
                category = "image"
                filename = secure_filename(file.filename)
                files = now + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],files))
                mySql = """INSERT INTO slidetest (file, active, ms, seconds, type, deleted, who, status, mca, screen1, screen2, screen3, screen4, screen5)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                    """, (files, 1, ms, dseconds, category, 0, "mca_admin", 1, mca, screen1, screen2, screen3, screen4, screen5)
                mycursor.execute(*mySql)
                mydb.commit()
                return render_template('admin/add.html',msg = "Successful")
        else:
            return render_template('admin/add.html',msg = "please select a file")
    elif request.form['formbtn'] == 'vid':
        file = request.files['vidfiles']
        if file:
            now = datetime.now().strftime("%d%m%Y%H%M%S")
            dseconds = request.form['durationvid']
            if dseconds == '':
                return render_template('admin/add.html',msg = "please add duration")
            else:
                op=request.form.getlist('screen')
                for x in op:
                    if(x == "mca"):
                        mca = 1
                    if(x == "screen1"):
                        screen1 = 1
                    if(x == "screen2"):
                        screen2 = 1
                    if(x == "screen3"):
                        screen3 = 1
                    if(x == "screen4"):
                        screen4 = 1
                    if(x == "screen5"):
                        screen5 = 1                      
                ms = int(dseconds) * 1000    
                category = "video"
                filename = secure_filename(file.filename)
                files = now + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],files))
                mySql = """INSERT INTO slidetest (file, active, ms, seconds, type, deleted, who, status, mca, screen1, screen2, screen3, screen4, screen5)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                    """, (files, 1, ms, dseconds, category, 0, "mca_admin", 1, mca, screen1, screen2, screen3, screen4, screen5)
                mycursor.execute(*mySql)
                mydb.commit()
                return render_template('admin/add.html',msg = "Successful added video")
        else:
            return render_template('admin/add.html',msg = "please select a video file")
    elif request.form['formbtn'] == 'pdf':
        file = request.files['pdffiles']
        if file:
            now = datetime.now().strftime("%d%m%Y%H%M%S")
            dseconds = request.form['durationpdf']
            if dseconds == '':
                return render_template('admin/add.html',msg = "please add duration")
            else:
                op=request.form.getlist('screen')
                for x in op:
                    if(x == "mca"):
                        mca = 1
                    if(x == "screen1"):
                        screen1 = 1
                    if(x == "screen2"):
                        screen2 = 1
                    if(x == "screen3"):
                        screen3 = 1
                    if(x == "screen4"):
                        screen4 = 1
                    if(x == "screen5"):
                        screen5 = 1                        
                ms = int(dseconds) * 1000    
                category = "image"
                filename = secure_filename(file.filename)
                files = filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],files))
                pages = convert_from_path(app.config['UPLOAD_FOLDER']+ '/' + files, 500)
                for i, page in enumerate(reversed(pages)):
                    name = str(i) + now + 'pdf' + '.png'
                    page.save(os.path.join(app.config['UPLOAD_FOLDER'],  name), 'PNG')
                mySql = """INSERT INTO slidetest (file, active, ms, seconds, type, deleted, who, status, mca, screen1, screen2, screen3, screen4, screen5)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                    """, (files, 1, ms, dseconds, category, 0, "mca_admin", 1, mca, screen1, screen2, screen3, screen4, screen5)
                mycursor.execute(*mySql)
                mydb.commit()
                os.remove(app.config['UPLOAD_FOLDER']+ '/' + files)
                return render_template('admin/add.html',msg = "Successful added pdf")
        else:
            return render_template('admin/add.html',msg = "please select a pdf file")            
    elif request.form['formbtn'] == 'txt':
        dseconds = request.form['durationtxt']
        if dseconds == '':
            return render_template('admin/add.html',msg = "please add duration for text")
        else:
            ms = int(dseconds) * 1000    
            category = "text"
            file = request.form['textval']
            if file == '':
                return render_template('admin/add.html',msg = "Please add text")
            else:
                op=request.form.getlist('screen')
                for x in op:
                    if(x == "mca"):
                        mca = 1
                    if(x == "screen1"):
                        screen1 = 1
                    if(x == "screen2"):
                        screen2 = 1
                    if(x == "screen3"):
                        screen3 = 1
                    if(x == "screen4"):
                        screen4 = 1
                    if(x == "screen5"):
                        screen5 = 1 
                mySql = """INSERT INTO slidetest (file, active, ms, seconds, type, deleted, who, status, mca, screen1, screen2, screen3, screen4, screen5)
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                    """, (file, 1, ms, dseconds, category, 0, "mca_admin", 1, mca, screen1, screen2, screen3, screen4, screen5)
                mycursor.execute(*mySql)
                mydb.commit()    
            return render_template('admin/add.html',msg = "Successful added text message")
    else:
        return render_template('admin/add.html',msg = "something went wrong")

@app.route("/togglenotice")
def toggles():
    try:
        mydisplay2 = """select id,file,active,type from slidetest where status = %s and deleted = %s  order by id desc"""
        mycursor.execute(mydisplay2, (1, 0, ))
        display2 = mycursor.fetchall()
        disps2 = [row for row in display2]
        return render_template('admin/toggle.html',disp2 = disps2)
    except Exception as e:
        return(str(e))

@app.route("/togglenotice", methods=['POST'])
def toggled():
        btval = request.form['update']
        try:
            ids = btval.split('.')[0]
            if btval.split('.')[1] == '1':
                act = '1'
            else:
                act = '0'    
            mydisplay = """update slidetest set active = %s where id = %s"""
            mycursor.execute(mydisplay, (act, ids, ))
            mydb.commit()
            return redirect(url_for('toggles'))
        except Exception:
            return redirect(url_for('toggles'))            


            
@app.route("/updatenotice")
def updates():
    try:
        mydisplay = """select id,file,active,type from slidetest where active = "%s" and deleted = "%s" and status = "%s"  order by id desc"""
        mycursor.execute(mydisplay, (1, 0, 1, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        mydisplay2 = """select id,file,active,type from slidetest where deleted = "%s"  order by id desc"""
        mycursor.execute(mydisplay2, (0, ))
        display2 = mycursor.fetchall()
        disps2 = [row for row in display2]
        return render_template('admin/updatenotice.html', disp = disps, disp2 = disps2)
    except Exception as e:
        return(str(e))

@app.route("/updatenotice", methods=['POST'])
def deleteform():
        try:
            ids = request.form['update']
            act = 1
            if ids == "select":
                test_msg = "please select id"
                return redirect(url_for('updates'))
            else:
                mydisplay = """update slidetest set deleted = %s where id = %s"""
                mycursor.execute(mydisplay, (act, ids, ))
                mydb.commit()
                test_msg = "Successful"
                return redirect(url_for('updates'))
        except Exception:
            test_msg = "an error occoured"
            return redirect(url_for('updates'))


@app.route("/archives")
def archives():
    try:
        mydisplay = """select id,file,active,type from slidetest where deleted = "%s" order by id"""
        mycursor.execute(mydisplay, (1, ))
        display = mycursor.fetchall()
        disps = [row for row in display]
        return render_template('admin/archives.html', disp = disps)
    except Exception as e:
        return(str(e))


@app.route("/requests")
def approval():
        mydisplay2 = """select id,file,status,type,who,seconds,mca,screen1,screen2,screen3,screen4,screen5 from slidetest where status = "%s" order by id"""
        mycursor.execute(mydisplay2, (0, ))
        display2 = mycursor.fetchall()
        disps2 = [row for row in display2]
        totalreq = """select count(status)from slidetest where status = %s """
        mycursor.execute(totalreq, (0, ))
        times = mycursor.fetchone()
        time = [row for row in times]
        # screens = """select mca,screen1,screen2,screen3,screen4,screen5 from slidetest where status = "%s" order by id"""
        # mycursor.execute(screens, (0, ))
        # scr = mycursor.fetchall()
        # testscreen = [row for row in scr]
        return render_template('admin/requests.html', disp2 = disps2, times = time)

@app.route("/requests", methods=['POST'])
def approvals():
    btval = request.form['approval']
    try:
        ids = btval.split('.')[0]
        if btval.split('.')[1] == '1':
            stat = 1
        else:
            stat = -1
        mydisplay = """update slidetest set status = %s where id = %s"""
        mycursor.execute(mydisplay, (stat, ids, ))
        mydb.commit()
        test_msg = "Successful"
        return redirect(url_for('approval'))               
    except Exception as e:
        test_msg = "an error occoured"
        return redirect(url_for('approval'))


@app.route("/ahome")
def adminhome():
    return render_template('admin/adminhome.html')


@app.route("/urequest")
def userrequest():
    return render_template('user/userrequest.html')

@app.route("/urequest", methods=['POST'])
def userform():
    mca = screen1 = screen2 = screen3 = screen4 = screen5 = 0
    usernames = session['username']
    if request.form['formbtn'] == 'img':
        file = request.files['imgfiles']
        if file:
            now = datetime.now().strftime("%d%m%Y%H%M%S")
            dseconds = request.form['duration']
            if dseconds == '':
              return render_template('user/userrequest.html',msg = "please add duration")
            else:
                op=request.form.getlist('screen')
                for x in op:
                    if(x == "mca"):
                        mca = 1
                    if(x == "screen1"):
                        screen1 = 1
                    if(x == "screen2"):
                        screen2 = 1
                    if(x == "screen3"):
                        screen3 = 1
                    if(x == "screen4"):
                        screen4 = 1
                    if(x == "screen5"):
                        screen5 = 1                                                                                                
                ms = int(dseconds) * 1000    
                category = "image"
                filename = secure_filename(file.filename)
                files = now + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],files))
                mySql = """INSERT INTO slidetest (file, active, ms, seconds, type, deleted, who, status, mca, screen1, screen2, screen3, screen4, screen5) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                    """, (files, 0, ms, dseconds, category, 0, usernames, 0, mca, screen1, screen2, screen3, screen4, screen5)
                mycursor.execute(*mySql)
                mydb.commit()
                return render_template('user/userrequest.html',msg = "Successful")
        else:
            return render_template('user/userrequest.html',msg = "please select a file")
    elif request.form['formbtn'] == 'vid':
        file = request.files['vidfiles']
        if file:
            now = datetime.now().strftime("%d%m%Y%H%M%S")
            dseconds = request.form['durationvid']
            if dseconds == '':
                return render_template('user/userrequest.html',msg = "please add duration")
            else:
                op=request.form.getlist('screen')
                for x in op:
                    if(x == "mca"):
                        mca = 1
                    if(x == "screen1"):
                        screen1 = 1
                    if(x == "screen2"):
                        screen2 = 1
                    if(x == "screen3"):
                        screen3 = 1
                    if(x == "screen4"):
                        screen4 = 1
                    if(x == "screen5"):
                        screen5 = 1 
                ms = int(dseconds) * 1000    
                category = "video"
                filename = secure_filename(file.filename)
                files = now + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],files))
                mySql = """INSERT INTO slidetest (file, active, ms, seconds, type, deleted, who, status, mca, screen1, screen2, screen3, screen4, screen5) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                    """, (files, 0, ms, dseconds, category, 0, usernames, 0, mca, screen1, screen2, screen3, screen4, screen5)
                mycursor.execute(*mySql)
                mydb.commit()
                return render_template('user/userrequest.html',msg = "Successful added video")
        else:
            return render_template('user/userrequest.html',msg = "please select a video file")
    elif request.form['formbtn'] == 'pdf':
        file = request.files['pdffiles']
        if file:
            now = datetime.now().strftime("%d%m%Y%H%M%S")
            dseconds = request.form['durationpdf']
            if dseconds == '':
                return render_template('user/userrequest.html',msg = "please add duration")
            else:
                op=request.form.getlist('screen')
                for x in op:
                    if(x == "mca"):
                        mca = 1
                    if(x == "screen1"):
                        screen1 = 1
                    if(x == "screen2"):
                        screen2 = 1
                    if(x == "screen3"):
                        screen3 = 1
                    if(x == "screen4"):
                        screen4 = 1
                    if(x == "screen5"):
                        screen5 = 1 
                ms = int(dseconds) * 1000    
                category = "image"
                filename = secure_filename(file.filename)
                files = filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],files))
                pages = convert_from_path(app.config['UPLOAD_FOLDER']+ '/' + files, 500)
                for i, page in enumerate(reversed(pages)):
                    name = str(i) + now + 'pdf' + '.png'
                    page.save(os.path.join(app.config['UPLOAD_FOLDER'],  name), 'PNG')
                    mySql = """INSERT INTO slidetest (file, active, ms, seconds, type, deleted, who, status, mca, screen1, screen2, screen3, screen4, screen5) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                    """, (name, 0, ms, dseconds, category, 0, usernames, 0, mca, screen1, screen2, screen3, screen4, screen5)
                    mycursor.execute(*mySql)
                    mydb.commit()
                os.remove(app.config['UPLOAD_FOLDER']+ '/' + files)
                return render_template('user/userrequest.html',msg = "Successful added pdf")
        else:
            return render_template('user/userrequest.html',msg = "please select a pdf file")            
    elif request.form['formbtn'] == 'txt':

        dseconds = request.form['durationtxt']
        if dseconds == '':
            return render_template('user/userrequest.html',msg = "please add duration for text")
        else:
            ms = int(dseconds) * 1000    
            category = "text"
            file = request.form['textval']
            if file == '':
                return render_template('user/userrequest.html',msg = "Please add text")
            else:
                op=request.form.getlist('screen')
                for x in op:
                    if(x == "mca"):
                        mca = 1
                    if(x == "screen1"):
                        screen1 = 1
                    if(x == "screen2"):
                        screen2 = 1
                    if(x == "screen3"):
                        screen3 = 1
                    if(x == "screen4"):
                        screen4 = 1
                    if(x == "screen5"):
                        screen5 = 1
                mySql = """INSERT INTO slidetest (file, active, ms, seconds, type, deleted, who, status, mca, screen1, screen2, screen3, screen4, screen5)
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                """, (file, 0, ms, dseconds, category, 0, usernames, 0, mca, screen1, screen2, screen3, screen4, screen5)
                mycursor.execute(*mySql)
                mydb.commit()    
            return render_template('user/userrequest.html',msg = "Successful added text message")
    else:
        return render_template('user/userrequest.html',msg = "something went wrong") 


@app.route("/uhome")
def userhome():
    name = session['username']
    return render_template('user/userhome.html', names = name.capitalize())

@app.route("/mystatus")
def mystatus():
        usernames = session['username']
        mydisplay2 = """select file,status,type from slidetest where who = %s order by id"""
        mycursor.execute(mydisplay2, (usernames, ))
        display2 = mycursor.fetchall()
        disps2 = [row for row in display2]
        return render_template('user/userstatus.html', disp2 = disps2)

if __name__ == '__main__':
    app.run(host = ip,port=5000,debug=True)
