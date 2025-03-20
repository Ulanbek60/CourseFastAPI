from sqlalchemy import Integer, String, Enum, ForeignKey, Text, DECIMAL, DateTime, Boolean
from course_app.db.database import Base
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from datetime import datetime
from passlib.hash import bcrypt


class StatusChoices(str, PyEnum):
    student = 'student'
    teacher = 'teacher'


<<<<<<< HEAD
class UserProfile(Base):

    __tablename__ = 'user_profile'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
=======

class Student(Base):

    __tablename__ = 'student'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), nullable=False, default=StatusChoices.student)
>>>>>>> 1bfeb8a (added favorite)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(64))
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

<<<<<<< HEAD
    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                        cascade='all, delete-orphan')

    def set_passwords(self, password: str):
        self.hash_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hash_password)


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')


class Student(UserProfile):

    __tablename__ = 'student'
    id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), primary_key=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), nullable=False, default=StatusChoices.student)
=======
    tokens: Mapped[List['RefreshStudentToken']] = relationship('RefreshStudentToken', back_populates='user',
                                                        cascade='all, delete-orphan')

>>>>>>> 1bfeb8a (added favorite)
    assignment_students: Mapped[List['Assignment']] = relationship('Assignment', back_populates='students',
                                                       cascade='all, delete-orphan')
    answer_students: Mapped[List['AnswerStudent']] = relationship('AnswerStudent', back_populates='student_answer',
                                                       cascade='all, delete-orphan')
    student_certificate: Mapped[List['Certificate']] = relationship('Certificate', back_populates='certificate_student',
                                                       cascade='all, delete-orphan')
    review_course_student: Mapped[List['CourseReview']] = relationship('CourseReview', back_populates='student_review_course',
                                                       cascade='all, delete-orphan')
    student_review_student: Mapped[List['TeacherReview']] = relationship('TeacherReview', back_populates='student_review',
                                                       cascade='all, delete-orphan')
<<<<<<< HEAD

class Teacher(UserProfile):

    __tablename__ = 'teacher'
    id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), primary_key=True)
=======
    cart_user: Mapped['Cart'] = relationship('Cart', back_populates='student_cart', cascade='all, delete-orphan',
                                             uselist=False)
    favorite_user: Mapped['Favorite'] = relationship('Favorite', back_populates='student_favorite', cascade='all, delete-orphan',
                                             uselist=False)

    def set_passwords(self, password: str):
        self.hash_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hash_password)



class RefreshStudentToken(Base):
    __tablename__ = 'refresh_token_student'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('student.id'))
    user: Mapped['Student'] = relationship('Student', back_populates='tokens')



class Teacher(Base):

    __tablename__ = 'teacher'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(64))
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
>>>>>>> 1bfeb8a (added favorite)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), nullable=False, default=StatusChoices.teacher)
    experience: Mapped[int] = mapped_column(Integer, nullable=False)
    about_teacher: Mapped[str] = mapped_column(Text)
    specialization: Mapped[str] = mapped_column(String(256), nullable=False)
<<<<<<< HEAD
=======

    tokens: Mapped[List['RefreshTeacherToken']] = relationship('RefreshTeacherToken', back_populates='user',
                                                        cascade='all, delete-orphan')

>>>>>>> 1bfeb8a (added favorite)
    about_social: Mapped[List['About']] = relationship('About', back_populates='about',
                                                       cascade='all, delete-orphan')
    created_by_teacher: Mapped[List['Course']] = relationship('Course', back_populates='created_by',
                                                       cascade='all, delete-orphan')
    teacher_review_teacher: Mapped[List['TeacherReview']] = relationship('TeacherReview', back_populates='teacher_review',
                                                       cascade='all, delete-orphan')

<<<<<<< HEAD
=======
    def set_passwords(self, password: str):
        self.hash_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hash_password)


class RefreshTeacherToken(Base):
    __tablename__ = 'refresh_token_teacher'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('teacher.id'))
    user: Mapped['Teacher'] = relationship('Teacher', back_populates='tokens')

>>>>>>> 1bfeb8a (added favorite)

class About(Base):

    __tablename__ = 'about'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    about_id: Mapped[int] = mapped_column(ForeignKey('teacher.id'))
    about: Mapped['Teacher'] = relationship('Teacher', back_populates='about_social')
    social_network: Mapped[str] = mapped_column(String)
    graduate: Mapped[str] = mapped_column(String)


class Category(Base):

    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_course: Mapped[List['Course']] = relationship('Course', back_populates='category',
                                                           cascade='all, delete-orphan')


class StatusLevelChoices(str, PyEnum):
    beginner = 'beginner'
    middle = 'middle'
    advanced = 'advanced'


class StatusCertificateChoices(str, PyEnum):
    graduation_certificate = 'graduation_certificate'
    the_certificate_is_not_given = 'the_certificate_is_not_given'

class Course(Base):

    __tablename__ = 'course'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_name: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(Category, back_populates='category_course')
    level: Mapped[StatusLevelChoices] = mapped_column(Enum(StatusLevelChoices), nullable=False, default=StatusLevelChoices.beginner)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    created_by_id: Mapped[int] = mapped_column(ForeignKey('teacher.id'))
    created_by: Mapped[Teacher] = relationship(Teacher, back_populates='created_by_teacher')
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    certificate_course: Mapped[StatusCertificateChoices] = mapped_column(Enum(StatusCertificateChoices), default=StatusCertificateChoices.graduation_certificate)
    discount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    course_lesson: Mapped[List['Lesson']] = relationship('Lesson', back_populates='course',
                                                         cascade='all, delete-orphan')
    course_assignment: Mapped[List['Assignment']] = relationship('Assignment', back_populates='assignment_course',
                                                         cascade='all, delete-orphan')
    exam_course: Mapped[List['Exam']] = relationship('Exam', back_populates='course_exam',
                                                         cascade='all, delete-orphan')
    course_certificate: Mapped[List['Certificate']] = relationship('Certificate', back_populates='certificate_course',
                                                         cascade='all, delete-orphan')
    review_course: Mapped[List['CourseReview']] = relationship('CourseReview', back_populates='course_review_course',
                                                         cascade='all, delete-orphan')

class Lesson(Base):

    __tablename__ = 'lesson'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    video_url: Mapped[str] = mapped_column(String, nullable=False)
    video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[str] = mapped_column(Text)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course, back_populates='course_lesson')


class Assignment(Base):

    __tablename__ = 'assignment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    due_date: Mapped[datetime] = mapped_column(DateTime)
    assignment_course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    assignment_course: Mapped[Course] = relationship(Course, back_populates='course_assignment')
    students_id: Mapped[int] = mapped_column(ForeignKey('student.id'))
    students: Mapped[Student] = relationship(Student, back_populates='assignment_students')


class Exam(Base):

    __tablename__ = 'exam'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    course_exam_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course_exam: Mapped[Course] = relationship(Course, back_populates='exam_course')
    passing_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    exam_questions: Mapped[List['Questions']] = relationship('Questions', back_populates='exam',
                                                         cascade='all, delete-orphan')
    answer_exam: Mapped[List['AnswerStudent']] = relationship('AnswerStudent', back_populates='exam_answer',
                                                              cascade='all, delete-orphan')


class Questions(Base):

    __tablename__ = 'questions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    questions: Mapped[str] = mapped_column(String, nullable=False)
    exam_id: Mapped[int] = mapped_column(ForeignKey('exam.id'))
    exam: Mapped[Exam] = relationship(Exam, back_populates='exam_questions')
    option_questions: Mapped[List['Option']] = relationship('Option', back_populates='option',
                                                         cascade='all, delete-orphan')
    questions_exam: Mapped[List['AnswerStudent']] = relationship('AnswerStudent', back_populates='exam_questions',
                                                         cascade='all, delete-orphan')

class Option(Base):

    __tablename__ = 'option'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    option_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    option: Mapped[Questions] = relationship(Questions, back_populates='option_questions')
    text: Mapped[str] = mapped_column(String(200), nullable=False)
    test: Mapped[bool] = mapped_column(Boolean, default=False)
    option_exam: Mapped[List['AnswerStudent']] = relationship('AnswerStudent', back_populates='exam_option',
                                                         cascade='all, delete-orphan')

class AnswerStudent(Base):

    __tablename__ = 'answer'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_answer_id: Mapped[int] = mapped_column(ForeignKey('student.id'))
    student_answer: Mapped[Student] = relationship(Student, back_populates='answer_students')
    exam_answer_id: Mapped[int] = mapped_column(ForeignKey('exam.id'))
    exam_answer: Mapped[Exam] = relationship(Exam, back_populates='answer_exam')
    exam_questions_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    exam_questions: Mapped[Questions] = relationship(Questions, back_populates='questions_exam')
    exam_option_id: Mapped[int] = mapped_column(ForeignKey('option.id'))
    exam_option: Mapped[Option] = relationship(Option, back_populates='option_exam')


class Certificate(Base):
    __tablename__ = 'certificate'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    certificate_student_id: Mapped[int] = mapped_column(ForeignKey('student.id'))
    certificate_student: Mapped[Student] = relationship(Student, back_populates='student_certificate')
    certificate_course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    certificate_course: Mapped[Course] = relationship(Course, back_populates='course_certificate')
    issued_at: Mapped[datetime] = mapped_column(DateTime)
    certificate_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class CourseReview(Base):

    __tablename__ = 'review_course'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_review_course_id: Mapped[int] = mapped_column(ForeignKey('student.id'))
    student_review_course: Mapped[Student] = relationship(Student, back_populates='review_course_student')
    course_review_course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course_review_course: Mapped[Course] = relationship(Course, back_populates='review_course')
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TeacherReview(Base):

    __tablename__ = 'teacher_review'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    teacher_review_id: Mapped[int] = mapped_column(ForeignKey('teacher.id'))
    teacher_review: Mapped[Teacher] = relationship(Teacher, back_populates='teacher_review_teacher')
    student_review_id: Mapped[int] = mapped_column(ForeignKey('student.id'))
    student_review: Mapped[Student] = relationship(Student, back_populates='student_review_student')


<<<<<<< HEAD








=======
class Cart(Base):

    __tablename__ = 'cart'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_cart_id: Mapped[int] = mapped_column(ForeignKey('student.id'), unique=True)
    student_cart: Mapped['Student'] = relationship('Student', back_populates='cart_user')
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')

class CartItem(Base):

    __tablename__ = 'cart_item'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    cart: Mapped['Student'] = relationship('Cart', back_populates='items')
    course_cart_item_id: Mapped['int'] = mapped_column(ForeignKey('course.id'))
    course_cart_item: Mapped['Course'] = relationship('Course')


class Favorite(Base):

    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_favorite_id: Mapped[int] = mapped_column(ForeignKey('student.id'), unique=True)
    student_favorite: Mapped['Student'] = relationship('Student', back_populates='favorite_user')
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    items_favorite: Mapped[List['FavoriteItem']] = relationship('FavoriteItem', back_populates='favorite',
                                                   cascade='all, delete-orphan')

class FavoriteItem(Base):

    __tablename__ = 'favorite_item'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey('favorite.id'))
    favorite: Mapped['Student'] = relationship('Favorite', back_populates='items_favorite')
    course_favorite_item_id: Mapped['int'] = mapped_column(ForeignKey('course.id'))
    course_favorite_item: Mapped['Course'] = relationship('Course')
>>>>>>> 1bfeb8a (added favorite)













