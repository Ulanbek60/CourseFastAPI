from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import Course
from course_app.db.schema import CourseSchema
from course_app.db.database import SessionLocal
from typing import List

course_router = APIRouter(prefix='/course', tags=['Course'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@course_router.post('/')
async def course_create(course: CourseSchema, db: Session = Depends(get_db)):
    course_db = Course(**course.dict())
    db.add(course_db)
    db.commit()
    db.refresh(course_db)
    return course_db


@course_router.get('/', response_model=List[CourseSchema])
async def course_list(db: Session = Depends(get_db)):
    return db.query(Course).all()



@course_router.get('/{course_id}/', response_model=CourseSchema)
async def course_detail(course_id: int,db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise  HTTPException(status_code=400, detail='Мындай маалымат жок')
    return course


@course_router.put('/{course_id}', response_model=CourseSchema)
async def course_update(course_id: int, course: CourseSchema, db: Session = Depends(get_db)):
    course_db = db.query(Course).filter(Course.id==course_id).first()

    if course_db is None:
        raise HTTPException(status_code=404, detail='такого курса не существует')
    for course_key, course_value in course.dict().items():
        setattr(course_db, course_key, course_value)

    db.add(course_db)
    db.commit()
    db.refresh(course_db)
    return course_db


@course_router.delete('/{course_id}')
async def course_delete(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id==course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail='такого курса не существует')

    db.delete(course)
    db.commit()
    return {"message": 'This product deleted'}


