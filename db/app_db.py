from peewee import *

from db.models import *


class Database:
    def __init__(self):
        self._db = db
        self._db.connect()
        self._db.create_tables([Teachers, Parents, Tutors, Students, Homework, Groups, StudentsGroups, Courses])
        self.__create_dummies()
        self._db.close()

    def __create_dummies(self):
        zero_teacher = Teachers.get_or_create(teacher_key='0')
        zero_parent = Parents.get_or_create(parent_key='0')
        zero_tutor = Tutors.get_or_create(tutor_key='0')
        zero_course = Courses.get_or_create(course_key='0')
        zero_group = Groups.get_or_create(group_key='0', teacher=zero_teacher[0], tutor=zero_tutor[0], course=zero_course[0])

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
        if 'student_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('students')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        dummy_parent = Parents.get(parent_key='0')
        new_student = Students.get_or_create(parent=dummy_parent, **needed_fields)
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
        if 'hw_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('homework')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        dummy_teacher = Teachers.get(teacher_key='0')
        dummy_group = Groups.get(group_key='0')
        new_hw = Homework.get_or_create(teacher=dummy_teacher, group=dummy_group, **needed_fields)
        return new_hw[0]

    def register_group(self, **fields):
        if 'group_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('homework')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        dummy_teacher = Teachers.get(teacher_key='0')
        dummy_tutor = Tutors.get(tutor_key='0')
        dummy_course = Courses.get(course_key='0')
        new_group = Groups.get_or_create(teacher=dummy_teacher, tutor=dummy_tutor, course=dummy_course **needed_fields)
        return new_group[0]

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

    def get_user_type_from_key(self, key):
        user_type = ''
        key = key[0:3]
        if key == "STD":
            user_type = "Students"
        elif key == "TEA":
            user_type = "Teachers"
        elif key == "CUR":
            user_type = "Curators"
        elif key == "PAR":
            user_type = "Parents"
        elif key == "COU":
            user_type = "Courses"
        elif key == "GRO":
            user_type = "Groups"
        return user_type

        # Link student to parent by keys

    def tie_parent(self, student_key, parent_key):
        student = self.get_entity_by_key(student_key, 'student')
        student.parent = self.get_entity_by_key(parent_key, 'parent')

    def course_list(self, student_key):
        pass

        # ???

    def course_info(self, course_key):
        for g in StudentsGroups:
            print(g)

    def hw_by_course_and_number(self, course_key, lesson_n):
        pass
        # we actually don't have lesson number...

    def assign_course_to_student(self, student_key, course_key):
        pass

    def get_students_from_parent(self, parent_key):
        students = []
        for s in Students:
            if s.parent.parent_key == parent_key:
                students.append(s)
        return students

    def handle_doesnt_exist_error(self):
        return []

    def get_entity_by_key(self, key, entity_type):
        if entity_type == 'parent':
            try:
                p = Parents.get(Parents.parent_key == key)
                return p
            except DoesNotExist:
                return self.handle_doesnt_exist_error()
        elif entity_type == 'student':
            try:
                p = Students.get(Students.student_key == key)
                return p
            except DoesNotExist:
                return self.handle_doesnt_exist_error()
        elif entity_type == 'teacher':
            try:
                p = Teachers.get(Teachers.teacher_key == key)
                return p
            except DoesNotExist:
                return self.handle_doesnt_exist_error()
        elif entity_type == 'tutor':
            try:
                p = Tutors.get(Tutors.tutor_key == key)
                return p
            except DoesNotExist:
                return self.handle_doesnt_exist_error()
        elif entity_type == 'homework':
            try:
                p = Homework.get(Homework.hw_key == key)
                return p
            except DoesNotExist:
                return self.handle_doesnt_exist_error()
        elif entity_type == 'group':
            try:
                p = Groups.get(Groups.group_key == key)
                return p
            except DoesNotExist:
                return self.handle_doesnt_exist_error()
        else:
            return self.handle_doesnt_exist_error()


def main():
    app_db = Database()

main()
