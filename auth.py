from flask import request, session, redirect, url_for
from functools import wraps

# Custom decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('login'):
            return redirect(url_for('login_page'))  # Redirect to login if not logged in
        return f(*args, **kwargs)
    return decorated_function

def login_required_agent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('agentlogin'):
            return redirect(url_for('agent_page', next=request.url))  # Redirect to login if not logged in
        return f(*args, **kwargs)
    return decorated_function

