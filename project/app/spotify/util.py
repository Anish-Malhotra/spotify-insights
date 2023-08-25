import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta


REDIRECT_URI = "http://localhost:8004/spotify_callback"
SCOPE = "user-library-read"
CLIENT_ID = "07400bfe46634f1f8d7752496b5d8c7e"
CLIENT_SECRET = "0a41f3b4e51a4fc7a9e6c1f30a4c7f89"

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

LOCAL_AUTH = 'http://localhost:8004/spotify_redirect'


def form_login_url():
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
    }
    
    return f"{AUTH_URL}/?{urlencode(payload)}"
    

def form_redirect_url_with_username(spotify_username: str):
    payload = {
        'spotify_username': spotify_username,
    }
    return f"{LOCAL_AUTH}/?{urlencode(payload)}"


def get_spotify_access_token(code: str):
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
        
    return {"token": res_data.get("access_token"), "expiry": expiry}
    