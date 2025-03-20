from sqladmin import ModelView, Admin
from course_app.db.models import *
from course_app.db.database import engine


<<<<<<< HEAD
class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username]
    name = 'User'
    name_plural = 'Users'
=======
class TeacherAdmin(ModelView, model=Teacher):
    column_list = [Teacher.id, Teacher.username]
    name = 'Teacher'
    name_plural = 'Teachers'


class StudentAdmin(ModelView, model=Student):
    column_list = [Student.id, Student.username]
    name = 'Student'
    name_plural = 'Students'
>>>>>>> 1bfeb8a (added favorite)


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]
    name = 'Category'
    name_plural = 'Categories'