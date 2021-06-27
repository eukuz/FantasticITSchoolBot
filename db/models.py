from peewee import *

db = SqliteDatabase('ITSchoolBotDB')


class BaseModel(Model):
    class Meta:
        database = db


class Teachers(BaseModel):
    teacher_key = CharField(unique=True)
    UID = CharField(default='')
    contact_info = TextField(default='')


class Parents(BaseModel):
    parent_key = CharField(unique=True)
    UID = CharField(default='')
    contact_info = TextField(default='')


class Tutors(BaseModel):
    tutor_key = CharField(unique=True)
    UID = CharField(default='')
    contact_info = TextField(default='')


class Students(BaseModel):
    student_key = CharField(unique=True)
    UID = CharField(default='')
    contact_info = TextField(default='')
    parent = ForeignKeyField(Parents, backref='students')

class Courses(BaseModel):
    course_key = CharField(unique=True)
    course_info = TextField(default='')

class Groups(BaseModel):
    group_key = CharField(unique=True)
    course = ForeignKeyField(Courses, backref='groups')
    teacher = ForeignKeyField(Teachers, backref='groups')
    tutor = ForeignKeyField(Tutors, backref='groups')


class Homework(BaseModel):
    hw_key = CharField(unique=True)
    date = DateField(default='')
    description = TextField(default='')
    attached = BlobField(default='')
    teacher = ForeignKeyField(Teachers, backref='homework')
    group = ForeignKeyField(Groups, backref='homework')


class StudentsGroups(BaseModel):
    students = ForeignKeyField(Students)
    groups = ForeignKeyField(Groups)
