from graphene import Field, ObjectType, Mutation, String
from graphql import GraphQLError

from app.gql.types import SpotifyProfileObject
from app.db.db import Session
from app.db.models import SpotifyProfile


class CreateSpotifyProfile(Mutation):
    class Arguments:
        username = String(required=True)
        client_id = String(required=True)
        client_secret = String(required=True)
        
    spotify_profile = Field(lambda: SpotifyProfileObject)
    
    @staticmethod
    def mutate(root, info, username, client_id, client_secret):
        with Session() as session:
            existing_profile = session.query(SpotifyProfile).filter(SpotifyProfile.username == username).first()
            
            if existing_profile is not None:
                raise GraphQLError(f"Profile for {username} has already been imported")
            
            spotify_profile = SpotifyProfile(
                username=username,
                client_id=client_id,
                client_secret=client_secret,
            )
            session.add(spotify_profile)
            session.commit()
            session.refresh(spotify_profile)
            
            return CreateSpotifyProfile(spotify_profile=spotify_profile)
        


class Mutation(ObjectType):
    create_spotify_profile = CreateSpotifyProfile.Field()