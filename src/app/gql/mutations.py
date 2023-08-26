from graphene import Field, Int, ObjectType, Mutation, String
from graphql import GraphQLError
import requests

from app.gql.types import UserObject, SpotifyProfileObject
from app.db.db import Session
from app.db.models import User, SpotifyProfile
from app.spotify.util import form_redirect_url_with_username, get_spotify_auth_token, refresh_auth_token


# This mutation creates a new 'user' entry
class CreateUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        
    user = Field(lambda: UserObject)
    
    @staticmethod
    def mutate(root, info, username, email, password):
        with Session() as session:
            existing_user = session.query(User).filter(User.username == username, User.email == email).first()
            if existing_user is not None:
                raise GraphQLError(f"User with email: {email} already exists")
            
            user = User(
                username=username, email=email, password=password
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return CreateUser(user=user)


# This mutation creates a new 'spotify_profile' and serves an OAuth2 login URL to obtain an authorization token
class CreateSpotifyProfile(Mutation):
    class Arguments:
        user_id = Int(required=True)
        spotify_username = String(required=True)
        
    spotify_profile = Field(lambda: SpotifyProfileObject)
    spotify_login_url = String()
    
    @staticmethod
    def mutate(root, info, user_id, spotify_username):
        with Session() as session:
            existing_profile = session.query(SpotifyProfile).filter(SpotifyProfile.user_id == user_id, SpotifyProfile.spotify_username == spotify_username).first()
            if existing_profile is not None:
                raise GraphQLError(f"Profile for {spotify_username} has already been imported")
            
            spotify_profile = SpotifyProfile(
                user_id=user_id,
                spotify_username=spotify_username,
            )
            session.add(spotify_profile)
            session.commit()
            session.refresh(spotify_profile)
            
            login_url = form_redirect_url_with_username(spotify_username)
            
            return CreateSpotifyProfile(spotify_profile=spotify_profile, spotify_login_url=login_url)
        

# This mutation updates a newly created 'spotify_profile' with an authorization token, a refresh token and expiry time for use with the Spotify API        
class UpdateProfileWithAuthToken(Mutation):
    class Arguments:
        code = String(required=True)
        user = String(required=True)
        
    spotify_profile = Field(lambda: SpotifyProfileObject)
    
    @staticmethod
    def mutate(root, info, code, user):
        with Session() as session:
            existing_profile = session.query(SpotifyProfile).filter(SpotifyProfile.spotify_username == user).first()
            if not existing_profile:
                raise GraphQLError("Trying to authenticate user without a linked profile")
            
            token = get_spotify_auth_token(code)
                        
            existing_profile.authorization_token = token['token']
            existing_profile.token_expiry = token['expiry']
            existing_profile.refresh_token = token['refresh']
            session.commit()
            session.refresh(existing_profile)
            return UpdateProfileWithAuthToken(spotify_profile=existing_profile)
        

# This mutation updates an existing 'spotify_profile' with a new authorization token and expiry time using the refresh token
class UpdateProfileWithRefreshedToken(Mutation):
    class Arguments:
        user = String(required=True)
        
    spotify_profile = Field(lambda: SpotifyProfileObject)
    
    @staticmethod
    def mutate(root, info, user):
        with Session() as session:
            existing_profile = session.query(SpotifyProfile).filter(SpotifyProfile.spotify_username == user).first()
            if not existing_profile:
                raise GraphQLError("Trying to refresh user access without a linked profile")
            
            if not existing_profile.refresh_token:
                raise GraphQLError("Cannot refresh authorization without a refresh token")
            
            token = refresh_auth_token(existing_profile.refresh_token)
            
            existing_profile.authorization_token = token['token']
            existing_profile.token_expiry = token['expiry']
            session.commit()
            session.refresh(existing_profile)
            return UpdateProfileWithRefreshedToken(spotify_profile=existing_profile)


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    create_spotify_profile = CreateSpotifyProfile.Field()
    update_profile_with_auth_token = UpdateProfileWithAuthToken.Field()
    update_profile_with_refreshed_token = UpdateProfileWithRefreshedToken.Field()