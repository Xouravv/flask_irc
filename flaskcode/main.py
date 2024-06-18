from flask import Flask, render_template, redirect, url_for
from flask_wtf import CSRFProtect
from form import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Ensure this key is set

csrf = CSRFProtect(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("homepage.html")


@app.route('/home/<name>')
def user(name):
    return render_template("homepage.html",name="Welcome "+name)


@app.errorhandler(404)
def pagenotfound(e):
    return render_template("404.html"),404

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data
#         if username != "expected_username" or password != "expected_password":
#             form.username.errors.append("Invalid username or password.")
#             return render_template('login.html', form=form)
            
#         return redirect(url_for('success'))
#     return render_template('login.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = flaker()
    username=None
    if form.validate_on_submit():
        username = ''
        username = form.name.data
        form.name.data=''
    
    return render_template("test.html" ,form=form,name=username)

if __name__ == '__main__':
    app.run(debug=True,port=1234)
