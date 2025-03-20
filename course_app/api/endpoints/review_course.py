from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import CourseReview
from course_app.db.schema import CourseReviewSchema
from course_app.db.database import SessionLocal
from typing import List

course_review_router = APIRouter(prefix='/course_review', tags=['CourseReview'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@course_review_router.post('/', response_model=CourseReviewSchema)
async def review_create(review: CourseReviewSchema, db: Session = Depends(get_db)):
    review_db = CourseReview(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@course_review_router.get('/', response_model=List[CourseReviewSchema])
async def review_list(db: Session = Depends(get_db)):
    return db.query(CourseReview).all()


@course_review_router.get('/{review_id}/', response_model=CourseReviewSchema)
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    review = db.query(CourseReview).filter(CourseReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='Отзыв о курсе не найден')
    return review


@course_review_router.put('/{review_id}/', response_model=CourseReviewSchema)
async def review_update(review_id: int, review: CourseReviewSchema, db: Session = Depends(get_db)):
    review_db = db.query(CourseReview).filter(CourseReview.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail='Отзыв о курсе не найден')

    for key, value in review.dict().items():
        setattr(review_db, key, value)

    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@course_review_router.delete('/{review_id}/')
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    review = db.query(CourseReview).filter(CourseReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='Отзыв о курсе не найден')

    db.delete(review)
    db.commit()
    return {"message": "Отзыв удалён"}
