from logging import Logger
import logging,timeit
from app import app,db,socketio,join_room, leave_room 
from app.models import cruduser ,chatdata
import os,json
import datetime
from flask import request,render_template ,redirect,session #type:ignore
import pandas as pd
from functools import wraps

# from app.utils

# logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)  


@app.route('/')
def index():
    return render_template("welcome.html")
    

@app.route('/logs',methods=['GET', 'POST'])
def display_log():
    if request.method == 'POST':
        if 'delete' in request.form:
            with open('app.log', 'w'):
                pass
    try:
        with open('app.log', 'r') as log_file:
            log_content = log_file.read()
        return render_template('table.html', log_content=log_content)
    except FileNotFoundError:
        return "Log file not found"

# @app.route('/rjsldc', methods=['POST'])
# def rjSldc():
#     if(request.method == 'POST'):
#         try:
#             if 'password' in request.form and 'userid' in request.form and 'file' in request.files and "data" in request.form:
#                 reqUserid = request.form['userid']
#                 reqPassword = request.form['password'] 
#                 reqParameter = request.files['file']
#                 reqdata=request.form['data'] 
#                 if not reqUserid or not reqPassword  or not reqParameter or not reqdata:
#                     status={"status":'ERROR',"message" : "Username or Password or file required"}
#                 else:
#                     status={"status":'SUCESSS',"message" : "done"}
#             else: 
#                 status ={"status":'ERROR',"message" : "input 123required"}
#             form_data = request.form.to_dict()
#             execution_time = timeit.timeit(stmt="pass", number=1) 
#             logger.debug(f'Return value of /rjsldc: {status} and EXC TIME : {execution_time}')
#             logger.debug(f'Form data /rjsldc received : {form_data.values()} \n')
#             return status
#         except Exception as e:
#             status={"ERROR":str(e)}
#             return {"status":'ERROR',"message" : "input required"}
            



#------------------------------------------------------------------


@app.route('/db')
def homedb():
    query_result = db.session.query(cruduser).filter(cruduser.status == '1').all()
    return render_template('table_view.html', users=query_result)

@app.route('/crud',methods=['GET', 'POST'])
def crud():
    if request.method == 'GET':
        session["signup"]=False
        return render_template("login.html")
    if request.method == 'POST':
        if session["signup"] is False:
            username = request.form['name'] 
            email = request.form['email']
            password = request.form['psw']
            secretkey=request.form['scKey']
            try:
                email_in_db = cruduser.query.filter_by(email=email).first()
                user_in_db = cruduser.query.filter_by(username=username).first()
                if user_in_db is not None or email_in_db is not None  :
                    error="Username" if user_in_db is not None else 'Email'
                    db.session.rollback()
                    error_message=f'ERROR! Same {error} already exist'
                    return render_template("login.html",error_message=error_message)
                else:
                    new_user = cruduser(username=username, email=email, password=password ,secretkey=secretkey)
                    db.session.add(new_user)
                    db.session.commit()
                    session['signup']= True
                    return render_template("signSucess.html")
            except Exception as e:
                db.session.rollback()
                return f'Signup failed: {str(e)}'
        else:
            return render_template("alreadySign.html",)


def login_required(username_param):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("name")==kwargs.get(username_param):
                return f(*args, **kwargs)
            else:
                return redirect('/crud')
        return decorated_function
    return decorator

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if "name" not in  session:
            name = request.form['name']
            password =request.form['psw']
            user=cruduser.query.filter_by(username=name).first()
            print(user,user.password,password)
            if user is not None and password == str(user.password) :
                session['name'] = name
                return redirect(f"/chat/{name}")
            else:
                error_message="Username or Password Invalaid"
                return render_template("login.html",error_message=error_message)
        else:
            username= session.get('name')
            return render_template("alreadyloggedin.html", username=username)
    else:
        if "name" in  session:
            username= session.get('name')
            return render_template("alreadyloggedin.html", username=username)
        else:
            return redirect('/crud')
        
@app.route('/actives')
def active():
    return {'active':str(session)}

@app.route('/chat/<username>' ,methods=['GET', 'POST'])
@login_required("username")
def room_selection(username):
    if session.get('name')==username:
        return render_template('room_selection.html',username=username)
    else:
        return render_template('relogin.html')
    
def datatodb(data):
    new_message = chatdata(username=data['username'], message=data['message'], timestamp=data['timestamp'],room=data['room'])
    db.session.add(new_message)
    db.session.commit()
    return "SUCESS"


@app.route('/chat/<username>/<room>')
@login_required("username")
def chat(username,room):
    return render_template('chat1.html', username=username, room=room)
    
@socketio.on('join')
def handle_join(data):
    print(data,'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj   ')
    room = data['room']
    join_room(room)
    prevdata=chatdata.query.filter_by(room=room).all()
    if len(prevdata)!=0:
        for rowdata in prevdata:
            prev={"username":rowdata.username,"message":rowdata.message,
                  "timestamp":rowdata.timestamp,"room":rowdata.room}
            socketio.emit('message', prev, room=room)
    else:
        return {'errror':"error"}
    
@socketio.on('leave')
def handle_leave(data):
    print(data)
    room = data['room']
    leave_room(room)
    socketio.emit('message', data, room=room)

@socketio.on('message')
def handle_message(data):
    staus=datatodb(data)
    room = data['room']
    if staus:
        socketio.emit('message', data, room=room)
    else:
        return {'errror':"error"}

@app.route('/fp',methods=['GET', 'POST'])
def forgotPass():
    return render_template('forgot.html')

@app.route('/delete/<id>',methods=['GET', 'POST'])
def delete_data(id):
    if request.method == 'POST':
        user = cruduser.query.get(id)
        print(user)
        if user:
            user.status = 0
            db.session.commit()
            return redirect("/db")

@app.route('/update/<id>',methods=['GET','POST'])
def update_data(id):
    if request.method=='GET':
        return redirect('/crud')
    else:
        username = request.form['name']
        email = request.form['email']
        newpass=request.form['newpws']
        password =request.form['pwsd']
        user = cruduser.query.get(id)
        try:
            user_in_db='dfsf'
            if user_in_db is not None:
                if (password) == (user.password):
                    user.username=username
                    user.email=email
                    user.password=newpass
                    db.session.commit()
                    error_message= 'Success: Your account has been updated'
                    return render_template("update.html",user=user,error_message=error_message)
                else:
                    print((password) , (user.password),'else condtion')
                    error_message= "SORRY Password didnt match"
                    return render_template("update.html",user=user,error_message=error_message)
            else:
                db.session.rollback()
                error_message='SORRY! User not found '
                return render_template("update.html",error_message=error_message)
        except Exception as e:
            db.session.rollback()
            return f'Signup failed: {str(e)}'
        

#-----------------------------------------------------------------------------------------------------


