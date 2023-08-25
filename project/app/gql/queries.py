from graphene import List, ObjectType

from app.gql.types import SpotifyProfileObject


class Query(ObjectType):
    spotify_profiles = List(SpotifyProfileObject)
    
    @staticmethod
    def resolve_spotify_profiles(root, info):
        return [
            {
                "id": 1,
                "username": "testuser",
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
            }
        ]