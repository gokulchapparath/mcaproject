from flask import Flask, render_template, url_for

app = Flask(__name__, static_url_path='/static')


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
