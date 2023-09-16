from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models.base import Base
from database import SessionLocal, engine
from models.run import Run
from models.errors import Errors
from models.group_run import GroupRun
from models.team import Team
from models.team_type import TeamType
from models.submission import Submission
from models.turn_table import TurnTable
from models.university import University

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API

@app.get("/")
def root():
    return {"message": "Hello World"}