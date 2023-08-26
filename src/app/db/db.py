import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base


DB_URL = os.environ.get("DATABASE_CONN_STRING")

engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)
