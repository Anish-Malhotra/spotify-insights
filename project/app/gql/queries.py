from graphene import Field, Int, List, ObjectType, String
from graphql import GraphQLError

from app.db.db import Session

from app.gql.types import UserObject, SpotifyProfileObject, SpotifyProfileSavedSongObject
from app.db.models import User, SpotifyProfile, SpotifyProfileSavedSong


class Query(ObjectType):
    users = List(UserObject)
    user = Field(UserObject, id=Int(required=True))
    spotify_profiles = List(SpotifyProfileObject)
    spotify_profile = Field(SpotifyProfileObject, user_id=Int(), spotify_username=String())
    spotify_profile_saved_songs = List(SpotifyProfileSavedSongObject, limit=Int(default_value=50), offset=Int(default_value=0))
    
    @staticmethod
    def resolve_users(root, info):
        with Session() as session:
            return session.query(User).all()
        
    @staticmethod
    def resolve_user(root, info, id):
        with Session() as session:
            return session.query(User).filter(User.id == id).first()
    
    @staticmethod
    def resolve_spotify_profiles(root, info):
        with Session() as session:
            return session.query(SpotifyProfile).all()
        
    @staticmethod
    def resolve_spotify_profile(root, info, user_id = None, spotify_username = None):
        if not user_id and not spotify_username:
            raise GraphQLError("Cannot resolve profile without userId or spotifyUsername")
        
        with Session() as session:
            if user_id:
                return session.query(SpotifyProfile).filter(SpotifyProfile.user_id == user_id).first()
            else:
                return session.query(SpotifyProfile).filter(SpotifyProfile.spotify_username == spotify_username).first()
        
    @staticmethod
    def resolve_spotify_profile_saved_songs(root, info, limit, offset):
        with Session() as session:
            return session.query(SpotifyProfileSavedSong).limit(limit).offset(offset).all()