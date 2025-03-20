from course_app.db.models import Course, Favorite, FavoriteItem
from course_app.db.schema import CourseSchema, FavoriteSchema, FavoriteItemSchema, FavoriteItemCreateSchema
from fastapi import APIRouter, Depends, HTTPException
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session


favorite_router = APIRouter(prefix='/favorite', tags=['Favorite'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@favorite_router.get('/', response_model=FavoriteSchema)
async def favorite_list(student_favorite_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.student_favorite_id==student_favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail='Такого избранного не существует')

    favorite_items = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite.id).all()

    return {
        "id": favorite.id,
        "student_favorite_id": favorite.student_favorite_id,
        'items': favorite.items_favorite,
    }


@favorite_router.post('/create', response_model=FavoriteItemSchema)
async def favorite_add(item_data: FavoriteItemCreateSchema, student_favorite_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.student_favorite_id == student_favorite_id).first()
    if not favorite:
        favorite = Favorite(student_favorite_id=student_favorite_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)

    course = db.query(Course).filter(Course.id == item_data.course_favorite_item_id).first()
    if not course:
        raise HTTPException(status_code=404, detail='Курс не найден в избранном')

    course_item = db.query(FavoriteItem).filter(
        FavoriteItem.favorite_id == favorite.id,
        FavoriteItem.course_favorite_item_id == item_data.course_favorite_item_id
    ).first()

    if course_item:
        raise HTTPException(status_code=400, detail='Курс уже в избранном')

    favorite_item = FavoriteItem(favorite_id=favorite.id, course_favorite_item_id=item_data.course_favorite_item_id)
    db.add(favorite_item)
    db.commit()
    db.refresh(favorite_item)

    return favorite_item



@favorite_router.delete('/{course_favorite_item_id}')
async def favorite_delete(course_favorite_item_id: int, student_favorite_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter(Favorite.student_favorite_id == student_favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail='Избранный не найдена')
    favorite_item = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite.id,
                              FavoriteItem.course_favorite_item_id == course_favorite_item_id).first()

    if not favorite_item:
        raise HTTPException(status_code=404, detail='Курс отсутствует в избранном')

    db.delete(favorite_item)
    db.commit()
    return {"message": 'Курс удален из избранного'}