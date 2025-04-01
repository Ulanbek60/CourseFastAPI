from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from course_app.db.models import Course, StatusLevelChoices, StatusCertificateChoices
from course_app.db.schema import CourseSchema
from course_app.db.database import SessionLocal
from typing import List, Optional
from sqlalchemy import asc, desc
from fastapi_pagination import Page, paginate


course_router = APIRouter(prefix='/course', tags=['Course'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@course_router.get('/search/', response_model=List[CourseSchema])
async def search_course(course_name: str, db: Session = Depends(get_db)):
    course_db = db.query(Course).filter(Course.course_name.ilike(f'%{course_name}%')).all()
    if not course_db:
        raise HTTPException(status_code=404, detail='Course Not Found')
    return course_db


@course_router.post('/', response_model=CourseSchema)
async def course_create(course: CourseSchema, db: Session = Depends(get_db)):
    course_db = Course(**course.dict())
    db.add(course_db)
    db.commit()
    db.refresh(course_db)
    return course_db


@course_router.get('/', response_model=Page[CourseSchema])
async def list_course(
    min_price: Optional[float] = Query(None, alias='price[from]'),
    max_price: Optional[float] = Query(None, alias='price[to]'),
    level: Optional[StatusLevelChoices] = None,
    certificate_course: Optional[StatusCertificateChoices] = None,
    order_by: Optional[str] = Query(None, regex='^(asc|desc)$'),
    db: Session = Depends(get_db)
):
    query = db.query(Course)

    if min_price is not None:
        query = query.filter(Course.price >= min_price)
    if max_price is not None:
        query = query.filter(Course.price <= max_price)
    if level:
        query = query.filter(Course.level == level)
    if certificate_course:
        query = query.filter(Course.certificate_course == certificate_course)
    if order_by == 'asc':
        query = query.order_by(asc(Course.price))
    elif order_by == 'desc':
        query = query.order_by(desc(Course.price))

    courses = query.all()

    if not courses:
        raise HTTPException(status_code=404, detail='Courses not found')
    return paginate(courses)


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


