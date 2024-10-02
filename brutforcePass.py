import requests
import time
import os

ID=0
agentPass="0000"
while True:
        # Define the URL for the Flask app
    url = "http://127.0.0.1:5000/agent/"

    # Data to be sent in the POST request
    data = {
        'agens': "5287",  # Use an incorrect Agent ID to trigger the error
        'password': 'wrong_password'  # Use an incorrect password
    }

    # Send the POST request
    response = requests.post(url, data=data)  # Use `data=` to send form data

    # Check if the request was successful
    if response.status_code == 200:
        printable=response.text

        if printable.find("Incorrect password for Agent ID#")<0:
            os.system('cls')

            print(f"Agent ID is: {agentPass}")
            break
        else:
            agentPass=int(agentPass)
            ID+=1
            if ID% 1000==0:
                time.sleep(1)
            agentPass = f"{ID:04}"
            agentPass=str(agentPass)
            os.system('cls')
            print(agentPass)


    else:
        # Only print the error message
        print('Error:', response.text)  # Print the error response directly
