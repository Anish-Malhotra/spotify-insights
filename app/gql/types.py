from graphene import Int, ObjectType, String


class SpotifyProfileObject(ObjectType):
    id = Int()
    username = String()
    client_id = String()
    client_secret = String()