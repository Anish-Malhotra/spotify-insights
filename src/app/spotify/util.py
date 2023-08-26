import os
import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta


# Spotify Application setup
SCOPE = os.environ.get("SCOPE")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# Spotify API URLs
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Local endpoints used with Spotify OAuth2
REDIRECT_URI = "http://localhost:8004/spotify_callback"
LOCAL_AUTH = 'http://localhost:8004/spotify_redirect'


# Used to obtain an access code, which is then used to obtain the authorization token for the user
def form_login_url():
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
    }
    
    return f"{AUTH_URL}/?{urlencode(payload)}"
    

# Used to package the requestor's spotify username as a cookie with the login url
def form_redirect_url_with_username(spotify_username: str):
    payload = {
        'spotify_username': spotify_username,
    }
    return f"{LOCAL_AUTH}/?{urlencode(payload)}"


# Obtains the authorization token for the current user for use with the Spotify API
def get_spotify_auth_token(code: str):
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    
    expiry = datetime.utcnow() + timedelta(seconds=3600)
    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()
    
    if res_data.get('error') or res.status_code != 200:
        raise Exception(
            'Failed to receive token: %s', res_data.get('error', 'No error information received.'),
        )
        
    return {"token": res_data.get("access_token"), "refresh": res_data.get("refresh_token"), "expiry": expiry}


# Obtains a refreshed authorization token for the user
def refresh_auth_token(refresh_token: str):
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    expiry = datetime.utcnow() + timedelta(seconds=3600)
    res = requests.post(
        TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload, headers=headers
    )
    res_data = res.json()
    
    return {"token": res_data.get("access_token"), "expiry": expiry}
    