from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Store chat messages in memory (use a database in production)
messages = []

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    # Extract data from the form
    username = request.remote_addr

    message = request.form.get('message')
    
    if username and message:
        messages.append({'username': username, 'message': message})
    
    return '', 204  # Return empty response with "No Content"

@app.route('/get_messages', methods=['GET'])
def get_messages():
    # Return the list of messages as JSON
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
