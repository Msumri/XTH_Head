from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import json
import os


connected_ips = {}  # Use a set to store unique IP addresses

# Define the path for the JSON file
MESSAGE_FILE = 'messages.json'
mesgsid=0
def load_messages():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r') as file:
            return json.load(file)
    return []

def save_messages(messages):
    with open(MESSAGE_FILE, 'w') as file:
        json.dump(messages, file)

# Load existing messages
chat_bp = Blueprint('chat_bp', __name__, template_folder='templates')
# Store chat messages in memory (use a database in production)
@chat_bp.route('/', methods=['POST','GET'])
def router():
    if request.method == 'POST':
        router_selection=request.form['router_number']
        name=request.form['name']
        session['name'] = name
        session['router_selection'] = router_selection
        print(router_selection)
        return redirect(url_for('chat_bp.chat',routernum=router_selection))
    else:
        return render_template('router.html')




@chat_bp.route('/<routernum>/')
def chat(routernum):

    user_ip = request.remote_addr
    connected_ips[user_ip] = routernum  # Associate IP with the router selection
    session['router_selection'] = routernum
    
    
    return render_template('chat.html',routernum=routernum)

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    messages = load_messages()

    username = request.remote_addr  # Consider allowing users to input a username
    message = request.form.get('message')
    
    if username and message:
        if len(message) > 0:  # Add validation for message length
            messages.append({'messegeid': len(messages),'username': username, 'message': message, 'router':session.get('router_selection'), 'Students_name':session.get('name'), 'path':'notactive'})
            save_messages(messages)
            return '', 204  # Return empty response with "No Content"
        else:
            return jsonify({'error': 'Message cannot be empty'}), 400
    return jsonify({'error': 'Invalid input'}), 400  # Handle case where username or message is missing

@chat_bp.route('/get_messages', methods=['GET'])
def get_messages():
    messages = load_messages()

    filtered_data = [msg for msg in messages if msg['router'] == session.get('router_selection')]
    return jsonify(filtered_data)

@chat_bp.route('/admintest', methods=['GET'])
def chatadmin():

    return jsonify(load_messages())

@chat_bp.route('/connected_ips', methods=['GET'])
def connected_ips_route():
    current_router = session.get('router_selection')
    filtered_ips = [ip for ip, room in connected_ips.items() if room == current_router]
    return jsonify(filtered_ips)  # Return the list of connected IPs as JSON

@chat_bp.route('/remove_ip', methods=['POST'])
def remove_ip():
    user_ip = request.remote_addr
    connected_ips.discard(user_ip)  # Remove the IP address
    return '', 204