from app import app,db,socketio
from flask_socketio import SocketIO, join_room, leave_room
# import eventlet  # Import eventlet


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # eventlet.monkey_patch()
    socketio.run(app,debug=True,port=5000)
