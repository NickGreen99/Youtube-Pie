from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
from pathlib import Path

# Authentication
def oauth():

    token_folder = Path(__file__).parent.parent
    token_file = token_folder / "token.pickle"

    client_secrets_folder = Path(__file__).parent.parent
    client_secrets_file = client_secrets_folder / "client_secrets/client_secrets.json"


    credentials = None
    # token.pickle stores the user's credentials from previously successful login
    token_file = token_file #"../token.pickle"

    if os.path.exists(token_file):
        print("Loading Credentials from File...")
        with open(token_file, "rb") as token:
            credentials = pickle.load(token)

    # if there are no valid credentials available, then either refresh the token or create new one
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token...")
            credentials.refresh(Request())
        else:
            print("Fetching new Tokens...")
        # Select the scopes of our app
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.readonly"])

        # Create server (localhost this time) to prompt users to allow us to view their YoutTube data
        flow.run_local_server(port=8080, prompt="consent")

        # Acquire credentials
        credentials = flow.credentials

        # Save the credentials for the next run
        with open(token_file, "wb") as f:
            print("Saving Credentials for future Use...")
            pickle.dump(credentials, f)
