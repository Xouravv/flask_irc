
from flask import Flask,render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

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


if __name__ == '__main__':
    socketio.run(app)
    # app.run()