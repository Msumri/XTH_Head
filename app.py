from flask import Flask, render_template,request,session
from flask_socketio import SocketIO, send, emit



app = Flask(__name__)
app.secret_key = 'hakoonamatata'  
socketio = SocketIO(app)

#hard code ids --its a bad idea but just for this simulation its fine
agentsid=['6218','7154','9819','5287','8030']
agentpass=['1899','3729','6515','9364','9484']
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map', methods=['POST','GET'])
def map():
    agentid=None
    password=None
    client_ip = request.remote_addr
    if request.method == 'POST':
        try:
            agentid=request.form['agens']
            password=request.form['password']
        
            
            if agentid in agentsid:
                agentindex=agentsid.index(agentid)
                print("TTTTT")
                if password in agentpass and agentpass.index(password)==agentindex:
                    session['login'] = True
            else :
                session['login'] =False

        finally:
            login=session['login']
            print(agentid)
            print(type(agentid))
            print(password)
            print(type(password))
    login = session.get('login', False)
    return render_template('map.html',login=login,client_ip=client_ip)



if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
