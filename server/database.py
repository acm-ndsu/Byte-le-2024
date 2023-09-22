from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = 'sqlite:///./byte_server.db'

engine = create_engine(
    DB_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
