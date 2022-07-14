import flask_restful
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
    id: int
    userId: int
    title: str
    body: str
