from flask import Flask, render_template, request, session, redirect, url_for, flash
from functools import wraps



app = Flask(__name__)
app.secret_key = 'hakoonamatata'  

#hard code ids --its a bad idea but just for this simulation its fine
agentsid=['6218','7154','9819','5287','8030']
agentpass=['1899','3729','6515','9364','9484']


# Custom decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('login'):
            return redirect(url_for('login_page'))  # Redirect to login if not logged in
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login_page():
    agentid=None
    password=None
    login = session.get('login', False)
    if request.method == 'POST':
        try:
            agentid=request.form['agens']
            password=request.form['password']
        
            
            if agentid in agentsid:
                agentindex=agentsid.index(agentid)
                if password in agentpass and agentpass.index(password)==agentindex:
                    session['login'] = True
                    return redirect(url_for('home'))
                else:
                    flash(f'Incorrect password for Agent ID# {agentid}')

            else :
                session['login'] =False
                flash('This user doesnt exist')
        except:
            login = session.get('login', False)
    else:
        if login:
            return redirect(url_for('home'))
            
    return render_template('loginpage.html',login=login)



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
