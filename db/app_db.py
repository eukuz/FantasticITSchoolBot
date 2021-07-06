from peewee import Expression

from db.models import *

debug_console_messages = True


class Database:
    def __init__(self):
        self._db = db
        self._db.connect()
        self._db.create_tables([Teachers, Parents, Tutors, Students, Homework, Groups, StudentsGroups, Courses])
        self.__create_dummies()
        self._db.close()

    def __create_dummies(self):
        zero_teacher = Teachers.get_or_create(teacher_key='0', UID='0')
        zero_parent = Parents.get_or_create(parent_key='0', UID='0')
        zero_tutor = Tutors.get_or_create(tutor_key='0', UID='0')
        zero_student = Students.get_or_create(student_key='0', UID='0', parent=zero_parent[0])
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
        if 'UID' not in needed_fields.keys():
            needed_fields['UID'] = needed_fields['parent_key']
        check = Parents.get_or_none(parent_key=needed_fields['parent_key'])
        if check is not None:
            return check
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
        if 'UID' not in needed_fields.keys():
            needed_fields['UID'] = needed_fields['student_key']
        check = Students.get_or_none(student_key=needed_fields['student_key'])
        if check is not None:
            return check
        dummy_parent = Parents.get(parent_key=fields['parent']) if 'parent' in fields else Parents.get(parent_key='0')
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
        if 'UID' not in needed_fields.keys():
            needed_fields['UID'] = needed_fields['teacher_key']
        check = Teachers.get_or_none(teacher_key=needed_fields['teacher_key'])
        if check is not None:
            return check
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
        if 'UID' not in needed_fields.keys():
            needed_fields['UID'] = needed_fields['tutor_key']
        check = Tutors.get_or_none(tutor_key=needed_fields['tutor_key'])
        if check is not None:
            return check
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
        check = Courses.get_or_none(course_key=needed_fields['course_key'])
        if check is not None:
            return check
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
        check = Homework.get_or_none(hw_key=needed_fields['hw_key'])
        if check is not None:
            return check
        dummy_teacher = Teachers.get(teacher_key=fields['teacher']) if 'teacher' in fields else Teachers.get(teacher_key='0')
        dummy_group = Groups.get(group_key=fields['group']) if 'group' in fields else Groups.get(group_key='0')
        new_hw = Homework.get_or_create(teacher=dummy_teacher, group=dummy_group, **needed_fields)
        return new_hw

    def register_group(self, **fields):
        if 'group_key' not in fields.keys():
            raise KeyError
        existing_fields = [i.name for i in self._db.get_columns('groups')]
        needed_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                needed_fields[key] = value
        check = Groups.get_or_none(group_key=needed_fields['group_key'])
        if check is not None:
            return check
        dummy_teacher = Teachers.get(teacher_key=fields['teacher']) if 'teacher' in fields else Teachers.get(teacher_key='0')
        dummy_tutor = Tutors.get(tutor_key=fields['tutor']) if 'tutor' in fields else Tutors.get(tutor_key='0')
        dummy_course = Courses.get(course_key=fields['course']) if 'course' in fields else Courses.get(course_key='0')
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
        elif table_name == 'tutors':
            self.register_tutor(**fields)
        elif table_name == 'courses':
            self.register_course(**fields)
        else:
            raise KeyError

    def get_parent(self, **fields):
        """ Gets a list of parents (or a single one) by filters

        Args:
            **fields - kwargs filters (parent fields, student primary keys)

        Returns:
            list of <Model: Parents> instances, if founds more than one
            a single <Model: Parents> instance, if founds one
            None, if founds nothing

        """
        existing_fields = [i.name for i in self._db.get_columns('parents')] # Gets all columns of the table
        parent_fields = {}
        for key, value in fields.items(): # Filters incorrect args
            if key in existing_fields:
                parent_fields[key] = value
        additional_fields = ['student_UID', 'student_key'] # Additional fields that could be passed in args
        student_fields = {}
        for key, value in fields.items(): # Filters student fields from args
            if key in additional_fields:
                if key == 'student_UID':
                    student_fields['UID'] = value
                else:
                    student_fields[key] = value
        student = None if len(student_fields) == 0 else Students.get_or_none(**student_fields) # Gets a student
        if student is not None:
            parents = [i for i in Parents.select().where(student.parent == Parents.id).filter(**parent_fields)] # Selects a parent of a student and checks requirements
        else:
            parents = [i for i in Parents.select().filter(**parent_fields)] # Selects a parent of a student and checks requirements
        # Expect single value if search by unique fields, list if search by non-unique fields
        return parents if len(parents) > 1 else parents[0] if len(parents) == 1 else None

    def get_student(self, **fields):
        """ Gets a list of students (or a single one) by filters. Works similar to get_parent(**fields)

        Args:
            **fields - kwargs filters (student fields, parent primary keys)

        Returns:
            list of <Model: Students> instances, if founds more than one
            a single <Model: Students> instance, if founds one
            None, if founds nothing
        """
        existing_fields = [i.name for i in self._db.get_columns('students')]
        student_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                student_fields[key] = value
        additional_fields = ['parent_UID', 'parent_key'] # Additional fields that could be passed in args
        parent_fields = {}
        group_key = None
        for key, value in fields.items():
            if key == 'group_key':
                group_key = value
            if key in additional_fields:
                if key == 'parent_UID':
                    parent_fields['UID'] = value
                else:
                    parent_fields[key] = value
        parent = None if len(parent_fields) == 0 else Parents.get_or_none(**parent_fields)
        query = Students.select().filter(**student_fields)
        if group_key is not None:
            query = query.join(StudentsGroups).join(Groups).where(Groups.group_key == group_key)
        if parent is not None:
            query = query.where(Students.parent == parent)
        students = [i for i in query]
        # Expect single value if search by unique fields, list if by non-unique or by parent
        return students if len(students) > 1 else students[0] if len(students) == 1 else None

    def get_teacher(self, **fields):
        """ Gets a list of teachers (or a single one) by filters
        Args:
           **fields - kwargs filters (teacher fields)

        Returns:
           list of <Model: Teachers> instances, if founds more than one
           a single <Model: Teachers> instance, if founds one
           None, if founds nothing
        """
        existing_fields = [i.name for i in self._db.get_columns('teachers')]
        teacher_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                teacher_fields[key] = value
        teachers = [i for i in Teachers.select().filter(**teacher_fields)]
        # Expect single value if search by unique fields, list if by non-unique
        return teachers if len(teachers) > 1 else teachers[0] if len(teachers) == 1 else None

    def get_tutor(self, **fields):
        """ Gets a list of tutors (or a single one) by filters
        Args:
           **fields - kwargs filters (tutor fields)

        Returns:
           list of <Model: Tutors> instances, if founds more than one
           a single <Model: Tutors> instance, if founds one
           None, if founds nothing
        """
        existing_fields = [i.name for i in self._db.get_columns('tutors')]
        tutor_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                tutor_fields[key] = value
        tutors = [i for i in Tutors.select().filter(**tutor_fields)]
        # Expect single value if search by unique fields, list if by non-unique
        return tutors if len(tutors) > 1 else tutors[0] if len(tutors) == 1 else None

    def get_course(self, **fields):
        """ Gets a list of courses (or a single one) by filters
        Args:
           **fields - kwargs filters (tutor fields, group unique fields)

        Returns:
           list of <Model: Courses> instances, if founds more than one
           a single <Model: Courses> instance, if founds one
           None, if founds nothing
        """
        existing_fields = [i.name for i in self._db.get_columns('courses')]
        course_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                course_fields[key] = value
        additional_fields = ['group_key'] # Additional fields that could be passed in args
        group_fields = {}
        for key, value in fields.items():
            if key in additional_fields:
                group_fields[key] = value
        group = None if len(group_fields) == 0 else self.get_group(**group_fields)
        if group is not None:
            courses = [i for i in Courses.select().where(Courses.id == group.course).filter(**course_fields)]
        else:
            courses = [i for i in Courses.select().filter(**course_fields)]
        # Expect single value if search by group or unique fields, list if by non-unique
        return courses if len(courses) > 1 else courses[0] if len(courses) == 1 else None

    def get_homework(self, **fields):
        """ Gets a list of homework (or a single one) by filters
        Args:
           **fields - kwargs filters (homework fields, group or teacher unique fields)

        Returns:
           list of <Model: Homework> instances, if founds more than one
           a single <Model: Homework> instance, if founds one
           None, if founds nothing
        """
        existing_fields = [i.name for i in self._db.get_columns('homework')]
        hw_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                hw_fields[key] = value
        additional_fields = ['group_key', 'teacher_key', 'teacher_UID'] # Additional fields that could be passed in args
        group_teacher_fields = {}
        for key, value in fields.items():
            if key in additional_fields:
                if key == 'teacher_UID':
                    group_teacher_fields['UID'] = value
                else:
                    group_teacher_fields[key] = value
        group = None if len(group_teacher_fields) == 0 else self.get_group(**group_teacher_fields)
        teacher = None if len(group_teacher_fields) == 0 else self.get_teacher(**group_teacher_fields)
        query = Homework.select().filter(**hw_fields)
        if group is not None:
            query = query.where(Homework.group == group)
        if teacher is not None:
            query = query.where(Homework.teacher == teacher)
        hws = [i for i in query]
        # Expect a single value if search by unique fields, list if by non-unique, by group or by teacher
        return hws if len(hws) > 1 else hws[0] if len(hws) == 1 else None

    def get_group(self, **fields):
        """ Gets a list of groups (or a single one) by filters
        Args:
           **fields - kwargs filters (group fields, student, tutor or teacher UID (unique))

        Returns:
           list of <Model: Groups> instances, if founds more than one
           a single <Model: Groups> instance, if founds one
           None, if founds nothing
        """
        existing_fields = [i.name for i in self._db.get_columns('groups')]
        group_fields = {}
        for key, value in fields.items():
            if key in existing_fields:
                group_fields[key] = value
        additional_fields = ['student_UID', 'tutor_UID', 'teacher_UID'] # Additional fields that could be passed in args
        other_fields = {}
        for key, value in fields.items():
            if key in additional_fields:
                other_fields[key] = value
        student = self.get_student(UID=other_fields['student_UID']) if 'student_UID' in other_fields.keys() else None
        teacher = self.get_teacher(UID=other_fields['teacher_UID']) if 'teacher_UID' in other_fields.keys() else None
        tutor = self.get_tutor(UID=other_fields['tutor_UID']) if 'tutor_UID' in other_fields.keys() else None
        query = Groups.select()
        if student is not None:
            query = query.join(StudentsGroups).join(Students).where(Students.UID == student.UID)
        if teacher is not None:
            query = query.where(Groups.teacher == teacher)
        if tutor is not None:
            query = query.where(Groups.tutor == tutor)
        groups = [i for i in query.filter(**group_fields)]
        # Expect a single value if search by unique fields, list if by student, teacher, tutor UIDs or by non-unique
        return groups if len(groups) > 1 else groups[0] if len(groups) == 1 else None

    def get(self, table_name, **fields):
        """
        Wrapper for all get_smth() methods
        """
        if table_name == 'groups':
            self.get_group(**fields)
        elif table_name == 'homework':
            self.get_homework(**fields)
        elif table_name == 'parents':
            self.get_parent(**fields)
        elif table_name == 'students':
            self.get_student(**fields)
        elif table_name == 'teachers':
            self.get_teacher(**fields)
        elif table_name == 'tutors':
            self.get_tutor(**fields)
        elif table_name == 'courses':
            self.get_course(**fields)
        else:
            raise KeyError('No such table')

    def set_parent(self, entity, **fields):
        if type(entity) is not Parents:
            raise KeyError('Given entity is not <Model: Parents>, please re-check your query')
        attributes = {}
        for key, value in fields.items():
            if hasattr(entity, key):
                attributes[key] = value
        Parents.update(**attributes).where(Parents.parent_key == entity.parent_key).execute()

    def set_student(self, entity, **fields):
        if type(entity) is not Students:
            raise KeyError('Given entity is not <Model: Students>, please re-check your query')
        attributes = {}
        for key, value in fields.items():
            if hasattr(entity, key):
                attributes[key] = value
        Students.update(**attributes).where(Students.student_key == entity.student_key).execute()

    def set_teacher(self, entity, **fields):
        if type(entity) is not Teachers:
            raise KeyError('Given entity is not <Model: Teachers>, please re-check your query')
        attributes = {}
        for key, value in fields.items():
            if hasattr(entity, key):
                attributes[key] = value
        Teachers.update(**attributes).where(Teachers.teacher_key == entity.teacher_key).execute()

    def set_tutor(self, entity, **fields):
        if type(entity) is not Tutors:
            raise KeyError('Given entity is not <Model: Tutors>, please re-check your query')
        attributes = {}
        for key, value in fields.items():
            if hasattr(entity, key):
                attributes[key] = value
        Tutors.update(**attributes).where(Tutors.tutor_key == entity.tutor_key).execute()

    def set_course(self, entity, **fields):
        if type(entity) is not Courses:
            raise KeyError('Given entity is not <Model: Courses>, please re-check your query')
        attributes = {}
        for key, value in fields.items():
            if hasattr(entity, key):
                attributes[key] = value
        Courses.update(**attributes).where(Courses.course_key == entity.course_key).execute()

    def set_homework(self, entity, **fields):
        if type(entity) is not Homework:
            raise KeyError('Given entity is not <Model: Homework>, please re-check your query')
        attributes = {}
        for key, value in fields.items():
            if hasattr(entity, key):
                attributes[key] = value
        Homework.update(**attributes).where(Homework.hw_key == entity.hw_key).execute()

    def set_group(self, entity, **fields):
        if type(entity) is not Groups:
            raise KeyError('Given entity is not <Model: Groups>, please re-check your query')
        attributes = {}
        for key, value in fields.items():
            if hasattr(entity, key):
                attributes[key] = value
        Groups.update(**attributes).where(Groups.group_key == entity.group_key).execute()

    def set(self, table_name, entity, **fields):
        if table_name == 'groups':
            self.set_group(entity, **fields)
        elif table_name == 'homework':
            self.set_homework(entity, **fields)
        elif table_name == 'parents':
            self.set_parent(entity, **fields)
        elif table_name == 'students':
            self.set_student(entity, **fields)
        elif table_name == 'teachers':
            self.set_teacher(entity, **fields)
        elif table_name == 'tutor':
            self.set_tutor(**fields)
        else:
            raise KeyError('No such table')

    def get_user_type_from_key(self, key):
        user_type = ''
        key = key[0:3]
        if key == "STD":
            user_type = "Students"
        elif key == "TEA":
            user_type = "Teachers"
        elif key == "TUT":
            user_type = "Tutors"
        elif key == "PAR":
            user_type = "Parents"
        elif key == "COU":
            user_type = "Courses"
        elif key == "GRO":
            user_type = "Groups"
        elif key == "HOM":
            user_type = "Homework"
        return user_type


    # Assigns student to group in StudentGroup
    def map_student_group(self, student_key, group_key):
        StudentsGroups.get_or_create(student=self.get_student(student_key=student_key),
                                     group=self.get_group(group_key=group_key))

