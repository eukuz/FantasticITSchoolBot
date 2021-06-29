from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

student_schedule_btn = KeyboardButton('Расписание')
student_courses_btn = KeyboardButton('Мои курсы')
student_query_btn = KeyboardButton('Запрос')
student_add_course_btn = KeyboardButton('Добавить курс')
student_exit_btn = KeyboardButton('Выйти')
student_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(student_schedule_btn,
                                                                student_courses_btn,
                                                                student_add_course_btn,
                                                                student_query_btn,
                                                                student_exit_btn)
