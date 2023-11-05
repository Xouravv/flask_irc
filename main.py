
from flask import Flask,render_template,request
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Xourav0here:Initialize MySQL@Xourav0here.mysql.pythonanywhere-services.com/Xourav0here$default' 
db = SQLAlchemy(app)
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
def login():
    if request.method == "POST":
        try:
            username = request.form['name'] 
            email = request.form['email']
            password = request.form['psw']
            secretkey=request.form['pswr']
            new_user = cruduser(username=username, email=email, password=password ,secretkey=secretkey)
            db.session.add(new_user)
            db.session.commit()
            return {"status":"user added"}
        except Exception as e:
            return {"status":"user added" ,'error':str(e)}
    

if __name__ == '__main__':
    socketio.run(app)
    # app.run()