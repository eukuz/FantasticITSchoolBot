from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup

class States(Helper):
    mode = HelperMode.snake_case
    UNAUTHORIZED_STATE = ListItem()
    STUDENT_STATE = ListItem()
    PARENT_STATE = ListItem()
    TEACHER_STATE = ListItem()
    TUTOR_STATE = ListItem()
    STUDENT_KEY_STATE = ListItem()
    STUDENT_QUESTION_STATE = ListItem()
    PARENT_QUESTION_STATE = ListItem()
    STUDENT_SICK_STATE = ListItem()
    PARENT_SICK_STATE = ListItem()

