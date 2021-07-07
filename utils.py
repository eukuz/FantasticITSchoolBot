from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup


class States(Helper):
    mode = HelperMode.snake_case
    UNAUTHORIZED_STATE = ListItem()

    STUDENT_STATE = ListItem()
    STUDENT_KEY_STATE = ListItem()
    STUDENT_HW_STATE = ListItem()

    QUESTION_STATE = ListItem()
    SICK_STATE = ListItem()

    PARENT_STATE = ListItem()
    PARENT_REGISTRATION_STATE = ListItem()

    PARENT_QUESTION_STATE = ListItem()
    PARENT_SICK_STATE = ListItem()
    PARENT_FEEDBACK_STATE = ListItem()

    TEACHER_STATE = ListItem()
    TEACHER_ADD_COURSE_STATE = ListItem()
    TEACHER_CREATE_MASS_MESSAGE_STATE = ListItem()
    TEACHER_CREATE_HW_1_STATE = ListItem()  # Для ввода заголовка для ДЗ
    TEACHER_CREATE_HW_2_STATE = ListItem()  # Для ввода ДЗ

    TUTOR_STATE = ListItem()
    CREATE_COURSE_STATE = ListItem()
    CREATE_GROUP_STATE = ListItem()
    GENKEYS_STATE = ListItem()
    PUBLISH_POST_STATE = ListItem()
