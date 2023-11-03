from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO,send, join_room, leave_room
from datetime import timedelta



app = Flask(__name__)
# app.permanent_session_lifetime=timedelta(minutes=10)
socketio = SocketIO(app,cors_allowed_origins="*")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:new_password@localhost/testproject'
db = SQLAlchemy(app)

db.create_all()

from app import routes  
