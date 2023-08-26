from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(255), nullable=False)


class SpotifyProfile(Base):
    __tablename__ = "spotify_profiles"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    spotify_username = Column(String(100), primary_key=True, unique=True)
    authorization_token = (Column(String(255)))
    token_expiry = Column(DateTime)
    refresh_token = Column(String(255))
    
    
class SpotifyProfileSavedSong(Base):
    __tablename__ = "spotify_profile_saved_songs"
    
    spotify_username = Column(String, ForeignKey("spotify_profiles.spotify_username"), primary_key=True, nullable=False)
    song_id = Column(String(100), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    artist = Column(String(255)) # primary artist for the song
    