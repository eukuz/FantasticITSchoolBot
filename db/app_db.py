from db.models import *
from peewee import *

class Database:
    def __init__(self):
        self._db = db
        self._db.connect()
        self._db.create_tables([Teachers, Parents, Tutors, Students, Homework, Groups, StudentsGroups])
        self._db.close()

    def register_parent(self, **fields):
        if 'parent_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('parents')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        new_parent = Parents.get_or_create(**needed_fields)
        return new_parent[0]

    def register_student(self, **fields):
        if 'parent_key' or 'student_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('students')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        p_key = fields['parent_key']
        new_parent = self.register_parent(parent_key=p_key)
        new_student = Students.get_or_create(parent_id=new_parent, **needed_fields)
        return new_student[0]

    def register_teacher(self, **fields):
        if 'teacher_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('teachers')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        new_teacher = Teachers.get_or_create(**needed_fields)
        return new_teacher[0]

    def register_tutor(self, **fields):
        if 'tutor_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('tutors')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        new_tutor = Tutors.get_or_create(**needed_fields)
        return new_tutor[0]

    def register_homework(self, **fields):
        if 'teacher_key' or 'hw_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('homework')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        t_key = fields['teacher_key']
        new_teacher = self.register_teacher(teacher_key=t_key)
        new_hw = Tutors.get_or_create(teacher_id=new_teacher, **needed_fields)
        return new_hw[0]

    def register_group(self, **fields):
        pass

    def register(self, table_name, **fields):
        if table_name == 'groups':
            self.register_group(**fields)
        elif table_name == 'homework':
            self.register_homework(**fields)
        elif table_name == 'parents':
            self.register_parent(**fields)
        elif table_name == 'students':
            self.register_student(**fields)
        elif table_name == 'teachers':
            self.register_teacher(**fields)
        elif table_name == 'tutor':
            self.register_tutor(**fields)
        else:
            raise KeyError
        pass

def main():
    app_db = Database()

main()