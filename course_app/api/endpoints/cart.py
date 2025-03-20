from course_app.db.models import Course, Cart, CartItem
from course_app.db.schema import CourseSchema, CartSchema, CartItemSchema, CartItemCreateSchema
from fastapi import APIRouter, Depends, HTTPException
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session


cart_router = APIRouter(prefix='/cart', tags=['Cart'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@cart_router.get('/', response_model=CartSchema)
async def cart_list(student_cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.student_cart_id==student_cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Такого корзины не существует')

    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()

    total_price = sum(db.query(Course.price).filter(Course.id == item.course_cart_item_id).scalar() for item in cart_items)

    return {
        "id": cart.id,
        "student_cart_id": cart.student_cart_id,
        'items': cart.items,
        'total_price': total_price
    }


@cart_router.post('/create', response_model=CartItemSchema)
async def cart_add(item_data: CartItemCreateSchema, student_cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.student_cart_id == student_cart_id).first()
    if not cart:
        cart = Cart(student_cart_id=student_cart_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    course = db.query(Course).filter(Course.id == item_data.course_cart_item_id).first()
    if not course:
        raise HTTPException(status_code=404, detail='Курс не найден')

    course_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.course_cart_item_id == item_data.course_cart_item_id
    ).first()

    if course_item:
        raise HTTPException(status_code=400, detail='Курс уже в корзине')

    cart_item = CartItem(cart_id=cart.id, course_cart_item_id=item_data.course_cart_item_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item



@cart_router.delete('/{course_cart_item_id}')
async def cart_delete(course_cart_item_id: int, student_cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.student_cart_id == student_cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail='Корзина не найдена')
    cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id,
                              CartItem.course_cart_item_id == course_cart_item_id).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail='Курс отсутствует в корзине')

    db.delete(cart_item)
    db.commit()
    return {"message": 'Курс удален из корзины'}