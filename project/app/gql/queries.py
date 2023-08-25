from graphene import Field, Int, List, ObjectType

from app.gql.types import SpotifyProfileObject
from app.db.db import Session
from app.db.models import SpotifyProfile


class Query(ObjectType):
    spotify_profiles = List(SpotifyProfileObject)
    spotify_profile = Field(SpotifyProfileObject, id=Int(required=True))
    
    @staticmethod
    def resolve_spotify_profiles(root, info):
        with Session() as session:
            return session.query(SpotifyProfile).all()
        
    @staticmethod
    def resolve_spotify_profile(root, info, id):
        with Session() as session:
            return session.query(SpotifyProfile).filter(SpotifyProfile.id == id).first()