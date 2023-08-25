from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SpotifyProfile(Base):
    __tablename__ = "spotify_profiles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True)
    client_id = Column(String(255))
    client_secret = Column(String(255))
    
    
class SpotifyProfileSavedSongs(Base):
    __tablename__ = "spotify_profile_saved_songs"
    
    profile_id = Column(Integer, ForeignKey("spotify_profiles.id"), primary_key=True, nullable=False)
    song_id = Column(String(100), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    artist = Column(String(255)) # primary artist for the song
    