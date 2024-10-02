import requests
import time
import os

ID=0
agentid="0000"
while True:
        # Define the URL for the Flask app
    url = "http://127.0.0.1:5000/agent/"

    # Data to be sent in the POST request
    data = {
        'agens': agentid,  # Use an incorrect Agent ID to trigger the error
    }

    # Send the POST request
    response = requests.post(url, data=data)  # Use `data=` to send form data

    # Check if the request was successful
    if response.status_code == 200:
        printable=response.text

        if printable.find("This Agent ID# doesnt exist")<0:
            os.system('cls')

            print(f"Agent ID is: {agentid}")
            break
        else:
            agentid=int(agentid)
            ID+=1
            if ID% 1000==0:
                time.sleep(1)
            agentid = f"{ID:04}"
            agentid=str(agentid)
            os.system('cls')
            print(agentid)


    else:
        # Only print the error message
        print('Error:', response.text)  # Print the error response directly
        break
