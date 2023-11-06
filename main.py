
from flask import Flask,render_template,request,redirect
from flask_socketio import SocketIO, emit
from flask import session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="Xourav0here",
    password="aaWir9rE",
    hostname="Xourav0here.mysql.pythonanywhere-services.com",
    databasename="Xourav0here$new",
)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
from models import cruduser
try:
    db.create_all()
except:
    with app.app_context(): 
        db.create_all()



@app.route('/')
def hello_world():
    return render_template('welcome.html')

@socketio.on('message')
def handle_message(data):
    message = data['message']
    emit('message', {'message': message}, broadcast=True)

@app.route('/chat')
def index():
    return render_template('index.html')

@app.route('/profile')
def login():
    return render_template('login.html')

@app.route('/signin',methods=['GET', 'POST'])
def adddata():
    if request.method == "POST":
        try:
            username = request.form['name'] 
            email = request.form['email']
            password = request.form['psw']
            secretkey=request.form['scKey']
            new_user = cruduser(username=username, email=email, password=password ,secretkey=secretkey)
            db.session.add(new_user)
            db.session.commit()
            return render_template('signedin.html',username=username)
        except Exception as e:
            return {"status":"error" ,'error':str(e)}
        
@app.route('/login',methods=['GET', 'POST'])
def logged():
        if request.method == "POST":
            try:
                username = request.form['name'] 
                password = request.form['psw']
                #check database
                user=cruduser.query.filter_by(username=username).first()
                if user is not None and password == str(user.password) :
                    session['user'] = username
                    return redirect(f'/chat/{username}')
                else:
                    error_message="Username or Password Invalaid"
                    return render_template("login.html",error_message=error_message)
            except Exception as e:
                return {"status":"error" ,'error':str(e)}
        else:
            if "user" in session:
                return render_template("alreadyloggedin.html")
            else:
                return redirect('/profile')

@app.route('/actives')
def active():
    return {'active':str(session)}
        
@app.route('/signout',methods=['GET', 'POST'])
def signout():
    session.clear()
    return redirect('/profile')

def login_required(username_param):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("user")==kwargs.get(username_param):
                return f(*args, **kwargs)
            else:
                return redirect('/profile')
        return decorated_function
    return decorator


@app.route('/chat/<username>' ,methods=['GET', 'POST'])
@login_required("username")
def room_selection(username):
    if session.get('user')==username:
        return render_template('roomselect.html',username=username)
    else:
        return redirect('/profile')


    

if __name__ == '__main__':
    socketio.run(app)
    # app.run()
