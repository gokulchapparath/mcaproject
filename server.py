from flask import Flask, render_template, url_for

app= Flask(__name__, static_url_path='/static')

@app.route("/404")
def master():
    return render_template('master.html')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',  methods=['GET', 'POST'])

@app.route("/masteru")
def user():
    return render_template('user/usermaster.html')

@app.route("/mastera")
def admin():
    return render_template('admin/master.html')

@app.route("/register")
def register():
    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)