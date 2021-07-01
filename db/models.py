from peewee import *

db = SqliteDatabase('ITSchoolBotDB', pragmas={
    'ignore_check_constraints': 0
})


class BaseModel(Model):
    class Meta:
        database = db


class Teachers(BaseModel):
    teacher_key = CharField(unique=True)
    UID = CharField(unique=True)
    full_name = CharField(default='')
    alias = CharField(default='')
    phone_number = CharField(default='')


class Parents(BaseModel):
    parent_key = CharField(unique=True)
    UID = CharField(unique=True)
    full_name = CharField(default='')
    alias = CharField(default='')
    phone_number = CharField(default='')


class Tutors(BaseModel):
    tutor_key = CharField(unique=True)
    UID = CharField(unique=True)
    full_name = CharField(default='')
    alias = CharField(default='')
    phone_number = CharField(default='')


class Students(BaseModel):
    student_key = CharField(unique=True)
    UID = CharField(unique=True)
    full_name = CharField(default='')
    alias = CharField(default='')
    phone_number = CharField(default='')
    parent = ForeignKeyField(Parents, backref='students')


class Courses(BaseModel):
    course_key = CharField(unique=True)
    name = CharField(default='')
    info = TextField(default='')


class Groups(BaseModel):
    group_key = CharField(unique=True)
    name = CharField(default='')
    course = ForeignKeyField(Courses, backref='groups')
    teacher = ForeignKeyField(Teachers, backref='groups')
    tutor = ForeignKeyField(Tutors, backref='groups')


class Homework(BaseModel):
    hw_key = CharField(unique=True)
    subject = CharField(default='')
    date = DateField(default='')
    description = TextField(default='')
    attached = BlobField(default='')
    teacher = ForeignKeyField(Teachers, backref='homework')
    group = ForeignKeyField(Groups, backref='homework')


# Perhaps rename to something like StudentGroupMap? Too long
class StudentsGroups(BaseModel):
    student = ForeignKeyField(Students)
    group = ForeignKeyField(Groups)
