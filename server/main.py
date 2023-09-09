from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models.base import Base
from database import SessionLocal, engine

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