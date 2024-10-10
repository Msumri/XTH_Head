from flask import Flask, render_template, request, session, redirect, url_for, flash,send_from_directory
from file_upload import upload_bp   # Import the blueprint
from functools import wraps
import json
import os
import time
import hashcheck
# Function to read data from JSON file
def read_json_file(filename):
    with open(filename) as f:
        return json.load(f)

app = Flask(__name__)
app.secret_key = 'hakoonamatata'  

#hard code ids --its a bad idea but just for this simulation its fine
agentsid=['0886','7154','0503','5287','8030',"9801",'8812']
youragentid=agentsid[4] #the index of the id that will acctuly work
usernames=['midoshy','mlhart28@gmail.com','maple','natasha','sumri','aya']
passwords='022695'
#music code is 117 200 320
#hash code SHA256          E2EAFA6A936505D1706D676854A101B04A2FBD84CE52EC840D5E6F13473D0A68
#641B44E5FE100E9F11685E13009928E2BA52544B4E7D7E495AF8000A0A148DC9
#641B44E5FE100E9F11685E13009928E2BA52544B4E7D7E495AF8000A0A148DC9
#E2EAFA6A936505D1706D676854A101B04A2FBD84CE52EC840D5E6F13473D0A68

from auth import login_required, login_required_agent

#this fuctions look at all the files in Dr and add them to json file with all info
def organizefiles():
    with open("safedrive.json", 'r') as file:
        data_dict = json.load(file)
    dicoffiles=data_dict
    files = os.listdir("static/drive")
    for file in files:
        dicoffiles.setdefault(file,{
        "number":files.index(file)+1,
        "url":file,
        "uploadby":"shadow",
        "date":int(time.time())
        })
    with open("safedrive.json", 'w') as file:
        json.dump(dicoffiles, file, indent=4)
    


# Register the upload blueprint

app.register_blueprint(upload_bp, url_prefix='/upload/')

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
                    flash(f'the password for [ {agentid} ] is incorrect')

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
    session.pop('login', None) # Remove 'login' from session
    session.pop('agentlogin', None)  # Remove 'agentlogin' from session
    return redirect(url_for('login_page'))  # Redirect to login page after logging out
##########end of normal login ####################

@app.route('/')
@login_required
def home():
    return render_template('index.html',page_name="Dashboard",url='home')

### agnet login info####

@app.route('/agent/', methods=['POST','GET'])
def agent_page():
    agentid=None
    login = session.get('agentlogin', False)
    if request.method == 'POST':
        try:
            agentid=request.form['agens']
        
            
            if agentid in agentsid:
                if agentid==youragentid:
                    session['agentlogin'] = True
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('home'))
                else:
                    flash('This Agent ID# is not associated with your account please use your ID')
            else :
                session['agentlogin'] =False
                flash('This Agent ID# doesnt exist')
        except:
            login = session.get('agentlogin', False)
    else:
        if login:
            return redirect(url_for('home'))
            
    return render_template('Agentlogin.html',login=login,page_name="E-mail" ,url='agent_page')


@app.route('/emails/')
@login_required
@login_required_agent
def emails():
    emails_data = read_json_file('emails.json')  # Load data from JSON file

    # Add your email handling logic here
    return render_template('email.html',emails=emails_data,page_name="E-mail",url='emails')
@app.route('/emails/<sender>/')
@login_required_agent
def extedemail(sender):
    emails_data = read_json_file('emails.json')  # Load data from JSON file

    return render_template('extedemail.html', emails=emails_data,sender=sender,url='extedemail',page_name="details")

@app.route('/map/')
@login_required
@login_required_agent
def map():

    return render_template('maps.html',page_name="maps",url=map )

@app.route('/drive/')
@login_required
@login_required_agent
def drive():
    organizefiles()
    uploadedfiles = read_json_file('safedrive.json')  # Load data from JSON file

    return render_template('drive.html',files=uploadedfiles,page_name="Safe Drive",url='drive')
@app.route('/drive/<filename>')
@login_required
@login_required_agent
def download_file(filename):
   
    return  send_from_directory('static/drive',filename, as_attachment=True )


@app.route('/prog/')
@login_required
@login_required_agent
def progressreport():
    hashchecker=hashcheck.calculate_file_hash('static/drive/Wake_Me_Up_1.wav')
    return render_template('progressreport.html',hashchecker=hashchecker,page_name="progress reports")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
