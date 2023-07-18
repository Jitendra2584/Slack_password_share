import os
# Use the package we installed
from dotenv import load_dotenv
from slack_bolt import App
load_dotenv()
import json
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Add functionality here
# @app.event("app_home_opened") etc

def send_response(response_url, message):
    payload = {
        'text': message,
        'response_type': 'in_channel'  # Set to 'ephemeral' for a private response
    }
    requests.post(response_url, json=payload)

# Example usage
 






@app.command("/secret")
def handle_hello_command(ack, body, respond,say):
    # Acknowledge the command request
    ack()
    
    # Define the URL of the server you want to send the request to
    server_url = "http://127.0.0.1:8000/secret/"

    # Define the payload data to send with the request
    payload = {
        "key1": body,
    }
    # Set up the headers with the shared secret
    headers = {
        "X-Bot-Secret": os.getenv('shared_token')
    }
    # Send a POST request to the server
    response = requests.post(server_url, json=payload,headers=headers)

    # Check the response status code
    if response.status_code == 200:
        print("Request sent successfully")
        response_url =body['response_url']
        send_response(response_url,json.loads(response.text)['text'] )
    else:
        print(f"Request failed with status code: {response.status_code}, {response.text}")




# Start your app
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
    