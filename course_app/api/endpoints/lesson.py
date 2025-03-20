from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import Lesson
from course_app.db.schema import LessonSchema
from course_app.db.database import SessionLocal
from typing import List

lesson_router = APIRouter(prefix='/lesson', tags=['Lesson'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lesson_router.post('/')
async def lesson_create(lesson: LessonSchema, db: Session = Depends(get_db)):
    lesson_db = Lesson(**lesson.dict())
    db.add(lesson_db)
    db.commit()
    db.refresh(lesson_db)
    return lesson_db


@lesson_router.get('/', response_model=List[LessonSchema])
async def lesson_list(db: Session = Depends(get_db)):
    return db.query(Lesson).all()


@lesson_router.get('/{lesson_id}/', response_model=LessonSchema)
async def lesson_detail(lesson_id: int,db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

    if lesson is None:
        raise  HTTPException(status_code=400, detail='Мындай маалымат жок')
    return lesson


@lesson_router.put('/{lesson_id}', response_model=LessonSchema)
async def lesson_update(lesson_id: int, lesson: LessonSchema, db: Session = Depends(get_db)):
    lesson_db = db.query(Lesson).filter(Lesson.id==lesson_id).first()

    if lesson_db is None:
        raise HTTPException(status_code=404, detail='такого урока не существует')
    for lesson_key, lesson_value in lesson.dict().items():
        setattr(lesson_db, lesson_key, lesson_value)

    db.add(lesson_db)
    db.commit()
    db.refresh(lesson_db)
    return lesson_db


@lesson_router.delete('/{lesson_id}')
async def lesson_delete(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id==lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail='такого урока не существует')

    db.delete(lesson)
    db.commit()
    return {"message": 'This product deleted'}


