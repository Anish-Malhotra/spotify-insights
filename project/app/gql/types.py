from graphene import Int, ObjectType, String


class SpotifyProfileObject(ObjectType):
    id = Int()
    username = String()
    client_id = String()
    client_secret = String()
    
    
class SpotifyProfileSavedSongsObject(ObjectType):
    profile_id = Int()
    song_id = String()
    name = String()
    artist = String()