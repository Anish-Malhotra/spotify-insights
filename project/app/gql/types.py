from graphene import Int, ObjectType, String, DateTime


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    password = String()

class SpotifyProfileObject(ObjectType):
    user_id = Int()
    spotify_username = String()
    authorization_token = String()
    token_expiry = DateTime()
    
    
class SpotifyProfileSavedSongObject(ObjectType):
    spotify_username = String()
    song_id = String()
    name = String()
    artist = String()