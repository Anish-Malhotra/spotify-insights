from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base


DB_URL = "postgresql+psycopg://root:secret@localhost:5432/spotify-insights-db"

engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)


def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)