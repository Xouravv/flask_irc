
from flask import Flask,render_template,request
from flask_socketio import SocketIO, emit
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
with app.app_context(): 
    db.create_all()

from models import cruduser

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/adddata',methods=['GET', 'POST'])
def adddata():
    if request.method == "POST":
        try:
            l=[]
            username = request.form['name'] 
            l.append(username)
            email = request.form['email']
            l.append(email)
            password = request.form['psw']
            l.append(password)
            secretkey=request.form['sckey']
            l.append(secretkey)
            new_user = cruduser(username=username, email=email, password=password ,secretkey=secretkey)
            db.session.add(new_user)
            db.session.commit()
            return {"status":"user added"}
        except Exception as e:
            return {"status":f"user added {l}" ,'error':str(e)}
    

if __name__ == '__main__':
    socketio.run(app)
    # app.run()
