from FantasticITSchoolBot.db.models import *

debug_console_messages = True


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
        zero_group = Groups.get_or_create(group_key='0', teacher=zero_teacher[0], tutor=zero_tutor[0],
                                          course=zero_course[0])

    def register_parent(self, **fields):
        if 'parent_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('parents')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        new_parent = Parents.get_or_create(**needed_fields)
        return new_parent

    def register_student(self, **fields):
        if 'student_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('students')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value

        dummy_parent = fields['parent'] if 'parent' in fields else Parents.get(parent_key='0')
        try:
            new_student = Students.get_or_create(parent=dummy_parent, **needed_fields)
            # return new_student[0]
            self.get_entity_by_key(fields['student_key'], 'student')
        except IntegrityError:
            if debug_console_messages:
                print("Student with key exists, Integrity error.")
            return self.get_entity_by_key(fields['student_key'], 'student')

    def register_teacher(self, **fields):
        if 'teacher_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('teachers')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        new_teacher = Teachers.get_or_create(**needed_fields)
        return new_teacher

    def register_tutor(self, **fields):
        if 'tutor_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('tutors')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        new_tutor = Tutors.get_or_create(**needed_fields)
        return new_tutor

    def register_course(self, **fields):
        if 'course_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('courses')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        new_course = Courses.get_or_create(**needed_fields)
        return new_course

    def register_homework(self, **fields):
        if 'hw_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('homework')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        dummy_teacher = fields['teacher'] if 'teacher' in fields else Teachers.get(teacher_key='0')
        dummy_group = fields['group'] if 'group' in fields else Groups.get(group_key='0')
        new_hw = Homework.get_or_create(teacher=dummy_teacher, group=dummy_group, **needed_fields)
        return new_hw

    def register_group(self, **fields):
        if 'group_key' not in fields.keys():
            raise KeyError
        query = Groups.select().where(Groups.group_key == fields['group_key'])
        if query.exists():
            if debug_console_messages:
                print('Group already exists.')
            existing_group = self.get_entity_by_key(fields['group_key'], 'group')
            # TODO update the given group
            return existing_group

        existing_fields = [i.name for i in self._db.get_columns('groups')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value

        # This will initialize new group with fields provided as arguments
        dummy_teacher = fields['teacher'] if 'teacher' in fields else Teachers.get(teacher_key='0')
        dummy_tutor = fields['tutor'] if 'tutor' in fields else Tutors.get(tutor_key='0')
        dummy_course = fields['course'] if 'course' in fields else Courses.get(course_key='0')

        new_group = Groups.get_or_create(teacher=dummy_teacher, tutor=dummy_tutor, course=dummy_course, **needed_fields)
        return new_group

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

    # Assigns student to group in StudentGroup
    def map_student_group(self, student_key, group_key):
        StudentsGroups.get_or_create(students=self.get_entity_by_key(student_key, 'student'),
                                     groups=self.get_entity_by_key(group_key, 'group'))

    # # Gets group key by student key, returns the first occurence
    # def get_group_key_by_student_key(self, student_key):
    #     # g = StudentsGroups.get(StudentsGroups.students.student_key == student_key)
    #
    #     for g in StudentsGroups:
    #         if g.students.student_key == student_key:
    #             return g.groups

    def tie_parent(self, student_key, parent_key):
        student = self.get_entity_by_key(student_key, 'student')
        student.parent_id = self.get_entity_by_key(parent_key, 'parent')
        student.save()

    def get_students_from_parent(self, parent_key):
        students = []
        for s in Students:
            if s.parent.parent_key == parent_key:
                students.append(s)
        return students

    def get_parent_key_from_student(self, student_key):
        for s in Students:
            if s.student_key == student_key:
                return s.parent_key

    def get_groups_by_student_key(self, student_key):
        groups = []
        for sg in StudentsGroups:
            if sg.students.student_key == student_key:
                groups.append(sg.groups)
        return groups

    def get_groups_of_children_from_parent_key(self, parent_key):
        result = []
        children = self.get_students_from_parent(parent_key)
        for c in children:
            result.append(self.get_groups_by_student_key(c.student_key))
        return result

    def get_homeworks_from_group(self, group_key):
        # TODO homeworks and groups are not tied yet
        pass

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


def test(app_db):
    app_db.register_parent(parent_key='p1')
    app_db.register_parent(parent_key='p2')
    app_db.register_parent(parent_key='p3')
    app_db.register_parent(parent_key='p4')

    app_db.register_student(student_key='s1')
    app_db.register_student(student_key='s2')
    app_db.register_student(student_key='s3')
    app_db.register_student(student_key='s4')
    app_db.register_student(student_key='s5')

    app_db.tie_parent('s1', 'p3')
    app_db.tie_parent('s2', 'p1')
    app_db.tie_parent('s3', 'p4')
    app_db.tie_parent('s4', 'p2')
    app_db.tie_parent('s5', 'p2')

    app_db.register_teacher(teacher_key='teacher1')
    app_db.register_tutor(tutor_key='tutor1')
    app_db.register_course(course_key='course1')
    app_db.register_teacher(teacher_key='teacher2')
    app_db.register_tutor(tutor_key='tutor2')
    app_db.register_course(course_key='course2')

    app_db.register_group(group_key='g1', course='course1', teacher='teacher1', tutor='tutor1')
    app_db.register_group(group_key='g2', course='course2', teacher='teacher2', tutor='tutor2')

    app_db.map_student_group('s2', 'g1')
    app_db.map_student_group('s4', 'g1')
    app_db.map_student_group('s5', 'g1')

    app_db.map_student_group('s1', 'g2')
    app_db.map_student_group('s3', 'g2')
    app_db.map_student_group('s5', 'g2')

    print(app_db.get_students_from_parent('p2'))

    print(app_db.get_groups_by_student_key('s5'))

    print(app_db.get_groups_of_children_from_parent_key('p2'))


def main():
    app_db = Database()
    test(app_db)


main()
