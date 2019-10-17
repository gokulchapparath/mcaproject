from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(13), unique=True, nullable=False)
    types = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.contact}',)"

@app.route("/masteru")
def user():
    return render_template('user/usermaster.html')


@app.route("/mastera")
def admin():
    return render_template('admin/master.html')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',  methods=['GET', 'POST'])


@app.route("/register")
def register():
    return render_template('registration.html')


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
