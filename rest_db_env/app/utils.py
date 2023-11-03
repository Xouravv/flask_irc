from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        
    