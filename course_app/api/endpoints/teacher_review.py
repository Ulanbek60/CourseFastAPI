from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import TeacherReview
from course_app.db.schema import TeacherReviewSchema
from course_app.db.database import SessionLocal
from typing import List

teacher_review_router = APIRouter(prefix='/teacher_review', tags=['TeacherReview'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@teacher_review_router.post('/', response_model=TeacherReviewSchema)
async def teacher_review_create(teacher_review: TeacherReviewSchema, db: Session = Depends(get_db)):
    teacher_review_db = TeacherReview(**teacher_review.dict())
    db.add(teacher_review_db)
    db.commit()
    db.refresh(teacher_review_db)
    return teacher_review_db


@teacher_review_router.get('/', response_model=List[TeacherReviewSchema])
async def teacher_review_list(db: Session = Depends(get_db)):
    return db.query(TeacherReview).all()


@teacher_review_router.get('/{teacher_review_id}/', response_model=TeacherReviewSchema)
async def teacher_review_detail(teacher_review_id: int, db: Session = Depends(get_db)):
    teacher_review = db.query(TeacherReview).filter(TeacherReview.id == teacher_review_id).first()
    if teacher_review is None:
        raise HTTPException(status_code=404, detail='Отзыв о преподавателе не найден')
    return teacher_review


@teacher_review_router.put('/{teacher_review_id}/', response_model=TeacherReviewSchema)
async def teacher_review_update(teacher_review_id: int, teacher_review: TeacherReviewSchema, db: Session = Depends(get_db)):
    teacher_review_db = db.query(TeacherReview).filter(TeacherReview.id == teacher_review_id).first()
    if teacher_review_db is None:
        raise HTTPException(status_code=404, detail='Отзыв о преподавателе не найден')

    for key, value in teacher_review.dict().items():
        setattr(teacher_review_db, key, value)

    db.add(teacher_review_db)
    db.commit()
    db.refresh(teacher_review_db)
    return teacher_review_db


@teacher_review_router.delete('/{teacher_review_id}/')
async def teacher_review_delete(teacher_review_id: int, db: Session = Depends(get_db)):
    teacher_review = db.query(TeacherReview).filter(TeacherReview.id == teacher_review_id).first()
    if teacher_review is None:
        raise HTTPException(status_code=404, detail='Отзыв о преподавателе не найден')

    db.delete(teacher_review)
    db.commit()
    return {"message": "Отзыв удалён"}
