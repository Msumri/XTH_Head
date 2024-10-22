from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import json
import os


##### messegses #####
MESSAGE_FILE = 'messages.json'
def load_messages():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, 'r') as file:
            return json.load(file)
    return []


##### messegses #####


# Load existing messages
admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/', methods=['POST','GET'])
def home():
    return render_template('adminhome.html')

@admin.route('/chat', methods=['POST','GET'])
def chat():
    messeges=load_messages()

    if request.method == 'POST':
        # Remove entries with Students_name "mohammed"
        deleteall="false"
        messegeid=request.form['messegeid']
        deleteall=request.form['deleteall']
        print(deleteall)
        messegeid=int(messegeid)
        filtered_data = [entry for entry in messeges if entry["messegeid"] != messegeid]
        if deleteall=="true":
            if os.path.isfile(MESSAGE_FILE):
                os.remove(MESSAGE_FILE)
                print(f"{MESSAGE_FILE} has been deleted.")
            else:
                print(f"{MESSAGE_FILE} does not exist.")
        # Save the modified JSON back to a file (optional)
        else:

            with open('messages.json', 'w') as f:
                json.dump(filtered_data, f, indent=4)

    return render_template('chatadmin.html', messeges=messeges)