from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup


class States(Helper):
    mode = HelperMode.snake_case
    UNAUTHORIZED_STATE = ListItem()

    STUDENT_STATE = ListItem()
    STUDENT_KEY_STATE = ListItem()
    STUDENT_QUESTION_STATE = ListItem()
    STUDENT_SICK_STATE = ListItem()

    PARENT_STATE = ListItem()
    PARENT_QUESTION_STATE = ListItem()
    PARENT_SICK_STATE = ListItem()
    PARENT_REGISTRATION_STATE = ListItem()

    TEACHER_STATE = ListItem()
    TEACHER_ADD_COURSE_STATE = ListItem()
    TEACHER_MY_COURSES_STATE = ListItem()

    TUTOR_STATE = ListItem()
    CREATE_COURSE_STATE = ListItem()
    CREATE_GROUP_STATE = ListItem()
    GENKEYS_STUDENT_STATE = ListItem()
    GENKEYS_TUTOR_STATE = ListItem()
    GENKEYS_TEACHER_STATE = ListItem()
    PUBLISH_POST_STATE = ListItem()
