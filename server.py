from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)



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


@app.route("/register")
def register():
    return render_template('registration.html')

@app.route("/register", methods=['POST'])
def register_post():
        global errorname
        fullname = request.form['fullname']
        x = any(char.isdigit() for char in fullname)
        if( x == True ):
            errorname = "Number not allowed!!"
            nameerror = True
            return render_template('registration.html', errorname = errorname)
        else:
            mobile = request.form['mobile']
            y = mobile.isalpha()
            if( y == True ):
                errormob = "No letters!!"
                return render_template('registration.html', errormob = errormob)
            elif( len(mobile) < 10 or len(mobile) > 10 ):
                errormob = "10 digits needed!!"
                return render_template('registration.html', errormob = errormob)
            else:
                okmob = "ok"
                return render_template('registration.html', okmob = ok)


        



@app.route("/addnewnotice")
def adminadd():
    return render_template('admin/add.html')


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
