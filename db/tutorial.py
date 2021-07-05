# First, import the DB class
# It's located in "app_db.py" and called "Database"
from FantasticITSchoolBot.db.app_db import Database

# initialize the DB
app_db = Database()


# ==============================[DEMO]==============================

def demo():
    app_db.register_parent(parent_key='p1')
    app_db.register_parent(parent_key='p2')
    app_db.register_parent(parent_key='p3')
    app_db.register_parent(parent_key='p4')

    app_db.register_student(student_key='s1', UID='a')
    app_db.register_student(student_key='s2', UID='b')
    app_db.register_student(student_key='s3')
    s4 = app_db.register_student(student_key='s4')

    app_db.register_teacher(teacher_key='teacher1', UID='c')
    app_db.register_tutor(tutor_key='tutor1', UID='d')
    app_db.register_course(course_key='course1')

    app_db.register_teacher(teacher_key='teacher2', UID='z')
    app_db.register_tutor(tutor_key='tutor2', UID='x')
    app_db.register_course(course_key='course2')

    app_db.register_group(group_key='g1', course='course1', teacher='teacher1', tutor='tutor1')
    app_db.register_group(group_key='g2', course='course2', teacher='teacher2', tutor='tutor2')

    p1 = app_db.get_parent(parent_key='p1').parent_key

    app_db.set_student(s4, parent_id=p1, full_name='bratan', alias='@Bratan')

    app_db.set_student(app_db.get_student(student_key='s1'), parent_id=p1)
    app_db.set_student(app_db.get_student(student_key='s2'), parent_id=p1)
    app_db.set_student(app_db.get_student(student_key='s3'), parent_id=p1)

    model_methods()
    common_methods()

    print(app_db.get_group(student_UID='b'))


# ==============================[WORKING WITH MODELS]==============================
def model_methods():
    # Let's look at example of student, but the same logic applies to all models
    # Student Model has following fields:
    #
    #     student_key
    #     UID
    #     full_name
    #     alias
    #     phone_number
    #     parent

    # We can get an instance by any of those fields. If field is unique,
    # an instance will be returned, otherwise -- list

    # Getting student by id
    st = app_db.get_student(student_key='s4')
    print(f'st.student_key by id: {st.student_key}')

    # Getting students by parent_id
    # Since some students have shared parent, method returns list
    st = app_db.get_student(parent_id='p1')
    print(f'st.student_key by parent_id: {st}')

    # Getting student by UID
    st = app_db.get_student(UID='b')
    print(f'st.student_key by UID {st.student_key}')

    # Getting student by Full Name
    st = app_db.get_student(full_name='bratan')
    print(f'st.student_key by full name: {st.student_key}')

    # Getting student by Full Name
    st = app_db.get_student(alias='@Bratan')
    print(f'st.student_key by alias: {st.student_key}')

    # Once we got the student, we can address any of it's fields:
    print(st)
    print(st.student_key)
    print(st.parent_id)
    print(st.UID)
    print(st.full_name)
    print(st.alias)

    # We can as well modify whatever fields we want with the set_student method:

    app_db.set_student(st, alias='@NewBratan')
    # NOTE: we need to actually fetch new set student from db, as previous instance of st
    # will not be updated
    st = app_db.get_student(student_key='s4')

    print(f'new alias: {st.alias}')


# ==============================[COMMON METHODS]==============================
def common_methods():
    # Assigning students to groups: takes student_key and group_key as arguments

    app_db.map_student_group('s1', 'g1')
    app_db.map_student_group('s4', 'g1')

    app_db.map_student_group('s2', 'g2')
    app_db.map_student_group('s3', 'g2')

    # Listing all groups of student by his UID
    app_db.get_group(student_UID='b')


# ==============================[REGISTRATION/CREATION OF USERS]==============================
def registration_of_users():
    # NOTE: This is usually handled by keygen class, so front don't really need this
    # but just in case to know how it works you may check it out

    # If you want to add an entity, either call corresponding method, like
    app_db.register_teacher()

    # You'll need to provide all data that you want the instance to have, for example the Teacher model
    # has the following fields:
    #     teacher_key
    #     UID
    #     full_name
    #     alias
    #     phone_number
    # they are added like
    app_db.register_teacher(teacher_key='teahcer1', UID='UID1', full_name='Teacher1 Full Name', alias='@teacher1',
                            phone_number='+71111111111')

    # Or you might call universal registration method

    app_db.register('teacher', teacher_key='teahcer2', UID='UID2', full_name='Teacher2 Full Name', alias='@teacher2',
                    phone_number='+71111111112')

    # NOTE: fields for all models can be found in models.py.


demo()
