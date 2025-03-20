from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import About
from course_app.db.schema import AboutSchema
from course_app.db.database import SessionLocal
from typing import List

about_router = APIRouter(prefix='/about', tags=['About'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@about_router.post('/')
async def about_create(about: AboutSchema, db: Session = Depends(get_db)):
    about_db = About(**about.dict())
    db.add(about_db)
    db.commit()
    db.refresh(about_db)
    return about_db


@about_router.get('/', response_model=List[AboutSchema])
async def about_list(db: Session = Depends(get_db)):
    return db.query(About).all()


@about_router.put('/', response_model=AboutSchema)
async def about_edit(about_id: int, about: AboutSchema, db: Session = Depends(get_db)):
    about_db = db.query(About).filter(About.id==about_id).first()

    if about_db is None:
        raise HTTPException(status_code=404, detail='такого учителя не существует')
    for about_key, about_value in about.dict().items():
        setattr(about_db, about_key, about_value)

    db.add(about_db)
    db.commit()
    db.refresh(about_db)
    return about_db


@about_router.delete('/')
async def about_delete(about_id: int, db: Session = Depends(get_db)):
    about = db.query(About).filter(About.id==about_id).first()
    if about is None:
        raise HTTPException(status_code=404, detail='такого учителя не существует')

    db.delete(about)
    db.commit()
    return {"message": 'This contact deleted'}

