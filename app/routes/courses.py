from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models
 
router = APIRouter()
 
# Inject db session using Depends
@router.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).filter(
        models.Course.is_active == True
    ).all()
    return courses