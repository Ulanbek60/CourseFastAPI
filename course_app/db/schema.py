from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from course_app.db.models import StatusChoices, StatusLevelChoices, StatusCertificateChoices


class StudentSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    password: str
    hash_password: str
    phone_number: Optional[str]
    age: Optional[int]
    profile_image: Optional[str]
    date_registered: datetime
    status: StatusChoices = StatusChoices.student
    assignment_students: List[int]
    answer_students: List[int]
    student_certificate: List[int]
    review_course_student: List[int]
    student_review_student: List[int]



class TeacherSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    hash_password: str
    phone_number: Optional[str]
    age: Optional[int]
    profile_image: Optional[str]
    date_registered: datetime
    status: StatusChoices = StatusChoices.teacher
    experience: int
    about_teacher: str
    specialization: str
    about_social: List[int]
    created_by_teacher: List[int]
    teacher_review_teacher: List[int]


class AboutSchema(BaseModel):
    about_id: int
    social_network: str
    graduate: str
    teacher_id: int


class CategorySchema(BaseModel):
    id: int
    category_name: str


class CourseSchema(BaseModel):
    id: int
    course_name: str
    description: str
    category_id: int
    level: StatusLevelChoices
    price: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    certificate_course: StatusCertificateChoices
    discount: Optional[int]
    # course_lesson: List[int]
    # course_assignment: List[int]
    # exam_course: List[int]
    # course_certificate: List[int]
    # review_course: List[int]

    class Config:
        from_attributes = True


class LessonSchema(BaseModel):
    id: int
    title: str
    video_url: str
    video: Optional[str]
    content: str
    course_id: int


class AssignmentSchema(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    course_id: int
    student_id: int


class ExamSchema(BaseModel):
    id: int
    title: str
    description: str
    passing_score: Optional[int]
    course_exam_id: int
    exam_questions: List[int]
    answer_exam: List[int]


class QuestionsSchema(BaseModel):
    id: int
    questions: str
    exam_id: int
    option_questions: List[int]
    questions_exam: List[int]


class OptionSchema(BaseModel):
    id: int
    text: str
    test: bool
    question_id: int


class AnswerStudentSchema(BaseModel):
    id: int
    student_answer_id: int
    exam_answer_id: int
    exam_questions_id: int
    exam_option_id: int


class CertificateSchema(BaseModel):
    id: int
    certificate_student_id: int
    certificate_course_id: int
    issued_at: datetime
    certificate_url: Optional[str]


class CourseReviewSchema(BaseModel):
    id: int
    student_review_course_id: int
    course_review_course_id: int
    text: str
    created_date: datetime


class TeacherReviewSchema(BaseModel):
    id: int
    teacher_review_id: int
    student_review_id: int


class CartItemSchema(BaseModel):
    id: int
    course_cart_item_id: int


class CartSchema(BaseModel):
    id: int
    student_cart_id: int
    items: List[CartItemSchema] = []
    total_price: float


class CartItemCreateSchema(BaseModel):
    course_cart_item_id: int




class FavoriteItemSchema(BaseModel):
    id: int
    course_favorite_item_id: int


class FavoriteSchema(BaseModel):
    id: int
    student_favorite_id: int
    items: List[FavoriteItemSchema] = []

    class Config:
        from_attributes = True


class FavoriteItemCreateSchema(BaseModel):
    course_favorite_item_id: int




