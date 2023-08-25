from graphene import Field, Int, List, ObjectType

from app.db.db import Session

from app.gql.types import SpotifyProfileObject, SpotifyProfileSavedSongsObject
from app.db.models import SpotifyProfile, SpotifyProfileSavedSongs


class Query(ObjectType):
    spotify_profiles = List(SpotifyProfileObject)
    spotify_profile = Field(SpotifyProfileObject, id=Int(required=True))
    spotify_profile_saved_songs = List(SpotifyProfileSavedSongsObject, limit=Int(default_value=50), offset=Int(default_value=0))
    
    @staticmethod
    def resolve_spotify_profiles(root, info):
        with Session() as session:
            return session.query(SpotifyProfile).all()
        
    @staticmethod
    def resolve_spotify_profile(root, info, id):
        with Session() as session:
            return session.query(SpotifyProfile).filter(SpotifyProfile.id == id).first()
        
    @staticmethod
    def resolve_spotify_profile_saved_songs(root, info, limit, offset):
        with Session() as session:
            return session.query(SpotifyProfileSavedSongs).limit(limit).offset(offset).all()