from peewee import *

db = SqliteDatabase('ITSchoolBotDB')

class BaseModel(Model):
    class Meta:
        database = db

class Teachers(BaseModel):
    teacher_key = CharField()
    contact_info = TextField()

class Parents(BaseModel):
    parent_key = CharField()
    contact_info = TextField()


class Tutors(BaseModel):
    tutor_key = CharField()
    contact_info = TextField()


class Students(BaseModel):
    student_key = CharField()
    contact_info = TextField()
    parent = ForeignKeyField(Parents, backref='students')

class Homework(BaseModel):
    hw_key = CharField()
    date = DateField()
    description = TextField()
    attached = BlobField()
    teacher = ForeignKeyField(Teachers, backref='homework')

class Groups(BaseModel):
    group_key = CharField()
    course_key = CharField()
    teacher = ForeignKeyField(Teachers, backref='groups')
    tutor = ForeignKeyField(Tutors, backref='groups')
    students = ManyToManyField(Students, backref='groups')
    homework = ForeignKeyField(Homework, backref='groups')