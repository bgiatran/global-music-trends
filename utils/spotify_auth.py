# utils/spotify_auth.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file (stored securely in project root)
# This avoids hardcoding sensitive credentials like client_id or client_secret
load_dotenv()

# Retrieves an app-level Spotify access token using Client Credentials Flow
def get_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_data = {'grant_type': 'client_credentials'}

    # Load client credentials from environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # Raise an error if credentials are missing or not properly set
    if not client_id or not client_secret:
        raise Exception("Missing Spotify credentials in environment variables or .env file.")

    # Make a POST request to Spotify's authentication endpoint
    auth_response = requests.post(auth_url, data=auth_data, auth=(client_id, client_secret))

    # If the response fails, raise an exception with the returned error message
    if auth_response.status_code != 200:
        raise Exception(f"Spotify auth failed: {auth_response.text}")

    # Extract and return the access token from the JSON response
    return auth_response.json()['access_token']