from main import db

class cruduser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    secretkey = db.Column(db.String(128), nullable=False)
    status=db.Column(db.String(128), nullable=False,default=1)