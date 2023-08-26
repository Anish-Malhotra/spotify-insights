from app.worker import celery
from app.spotify.auth import get_spotify_client
from app.db.models import SpotifyProfileSavedSong
from app.db.db import Session


API_LIMIT = 50


@celery.task(name="import_liked_songs")
def import_liked_songs(auth_token: str, username: str):
    client = get_spotify_client(auth_token)
    
    liked_songs = []
    offset = 0
    
    results = client.current_user_saved_tracks(limit=API_LIMIT, offset=offset)
    while len(results['items']) > 0:
        for item in results['items']:
            track = item['track']
            song = SpotifyProfileSavedSong(
                spotify_username=username,
                song_id=track['id'],
                name=track['name'],
                artist=track['artists'][0]['name']
            )
            liked_songs.append(song)
        offset = len(liked_songs)
        results = client.current_user_saved_tracks(limit=API_LIMIT, offset=offset)
        
    with Session() as session:
        session.bulk_save_objects(liked_songs)
        session.commit()
        