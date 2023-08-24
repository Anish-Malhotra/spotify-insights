from graphene import Field, ObjectType, Mutation, String

from app.gql.types import SpotifyProfileObject


class CreateSpotifyProfile(Mutation):
    class Arguments:
        username = String(required=True)
        client_id = String(required=True)
        client_secret = String(required=True)
        
    spotify_profile = Field(lambda: SpotifyProfileObject)
    
    @staticmethod
    def mutate(root, info, username, client_id, client_secret):
        spo = {
            "id": 1,
            "username": username,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        return CreateSpotifyProfile(spotify_profile=spo)


class Mutation(ObjectType):
    create_spotify_profile = CreateSpotifyProfile.Field()