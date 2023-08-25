from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SpotifyProfile(Base):
    __tablename__ = "spotify_profiles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100))
    client_id = Column(String(255))
    client_secret = Column(String(255))