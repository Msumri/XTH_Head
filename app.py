from flask import Flask, render_template, request, session, redirect, url_for, flash
from functools import wraps
import json

# Function to read data from JSON file
def read_json_file(filename):
    with open(filename) as f:
        return json.load(f)

app = Flask(__name__)
app.secret_key = 'hakoonamatata'  

#hard code ids --its a bad idea but just for this simulation its fine
agentsid=['6218','7154','9819','5287','8030']
agentpass=['1899','3729','6515','9364','9484']
usernames=['midoshy','mlhart28@gmail.com','maple','natasha']
passwords='022695'
#music code is 253 207 300
#hash code SHA256          3E70217D7ECE1D0C30750387D35B9E394A6D8A4A4D7E5C7E563A7C9EF206CE45
#CDB2FD9D4474CBD635CAC43D18A1441D766EBE024FA4D96DF50640D5B88C1D53
#CDB2FD9D4474CBD635CAC43D18A1441D766EBE024FA4D96DF50640D5B88C1D53
#3E70217D7ECE1D0C30750387D35B9E394A6D8A4A4D7E5C7E563A7C9EF206CE45
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
            return redirect(url_for('agent'))  # Redirect to login if not logged in
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login/', methods=['POST','GET'])
def login_page():

    agentid=None
    password=None
    login = session.get('login', False)
    if request.method == 'POST':
        try:
            agentid=request.form['agens']
            password=request.form['password']
        
            
            if agentid in usernames:
                if password == passwords :
                    session['login'] = True

                    return redirect(url_for('home'))                    
                else:
                    flash('check your user or password')

            else:
                flash('This user doesnt exist')

        except:
            login = session.get('login', False)
    else:
        if login:
            return redirect(url_for('home'))
            
    return render_template('loginpage.html',login=login,page_name="login")

@app.route('/logout/')
def logout():
    session.pop('login', None)  # Remove 'login' from session
    return redirect(url_for('login_page'))  # Redirect to login page after logging out
##########end of normal login ####################

@app.route('/')
@login_required
def home():
    return render_template('index.html',page_name="Dashboard")

### agnet login info####

@app.route('/agent/', methods=['POST','GET'])
@login_required
def agent_page():
    agentid=None
    password=None
    login = session.get('agentlogin', False)
    if request.method == 'POST':
        try:
            agentid=request.form['agens']
            password=request.form['password']
        
            
            if agentid in agentsid:
                agentindex=agentsid.index(agentid)
                if password in agentpass and agentpass.index(password)==agentindex:
                    session['agentlogin'] = True

                    return redirect(url_for('emails'))
                else:
                    flash(f'Incorrect password for Agent ID# {agentid}')

            else :
                session['agentlogin'] =False
                flash('This Agent ID# doesnt exist')
        except:
            login = session.get('agentlogin', False)
    else:
        if login:
            return redirect(url_for('emails'))
            
    return render_template('Agentlogin.html',login=login,page_name="E-mail")


@app.route('/emails/')
@login_required_agent
def emails():
    emails_data = read_json_file('emails.json')  # Load data from JSON file

    # Add your email handling logic here
    return render_template('email.html',emails=emails_data,page_name="E-mail")
@app.route('/emails/<sender>/')
@login_required_agent
def extedemail(sender):
    emails_data = read_json_file('emails.json')  # Load data from JSON file

    return render_template('extedemail.html', emails=emails_data,sender=sender)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
