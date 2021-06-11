from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from .unauthorized import dp
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import bot
from utils import States
from aiogram.dispatcher.filters import Text

parent_in_system_btn = InlineKeyboardButton('Мой родитель уже в системе', callback_data='parent in system')
parent_in_system_kb = InlineKeyboardMarkup().insert(parent_in_system_btn)

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

# Parent in system button
@dp.callback_query_handler(state=States.STUDENT_STATE, text='parent in system')
async def process_callback_parent_in_system(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # TODO: what to do?
    await bot.send_message(callback_query.from_user.id, 'Спасибо, мы запомнили :)')


# Schedule button
@dp.message_handler(state=States.STUDENT_STATE, text='Расписание')
async def process_schedule_btn(msg: types.Message):
    # TODO: generate schedule message
    schedule = text(bold('Python'), ' 10:00-10:30', sep='')
    await msg.answer(schedule, parse_mode=ParseMode.MARKDOWN)


# Creates course menu, can edit or answer to message
async def course_menu(user_id, message_id, mode):
    # TODO: generate list of courses
    courses = ['Python', 'Java', 'C++']
    courses_kb = InlineKeyboardMarkup()
    for i in range(len(courses)):
        courses_btn = InlineKeyboardButton(courses[i], callback_data='courses ' + courses[i])
        courses_kb.insert(courses_btn)

    if mode == 'answer':
        await bot.send_message(user_id, 'Ваши курсы: ', parse_mode=ParseMode.MARKDOWN, reply_markup=courses_kb)
    else:
        await bot.edit_message_text('Ваши курсы: ', user_id, message_id)
        await bot.edit_message_reply_markup(user_id, message_id, reply_markup=courses_kb)


# My courses button reply
@dp.message_handler(state=States.STUDENT_STATE, text='Мои курсы')
async def process_courses_btn(msg: types.Message):
    await course_menu(msg.from_user.id, msg.message_id, mode='answer')


# Course inline button
@dp.callback_query_handler(Text(startswith='courses '), state=States.STUDENT_STATE)
async def process_one_course_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    # TODO: generate list of lessons
    course = callback_query.data[7:]
    lessons = ['Урок 1', 'Урок 2', 'Урок 3']
    lessons_kb = InlineKeyboardMarkup()
    for i in range(len(lessons)):
        lesson_btn = InlineKeyboardButton(lessons[i], callback_data='presentation ' + course + ' ' + lessons[i])  # send presentation for this lesson
        get_hw_btn = InlineKeyboardButton('Получить домашнее задание', callback_data='gethw ' + course + ' ' + lessons[i])  # get homework
        send_hw_btn = InlineKeyboardButton('Отправить домашнее задание', callback_data='sendhw ' + course + ' ' + lessons[i])  # send homework
        lessons_kb.row(lesson_btn, get_hw_btn, send_hw_btn)
    back_btn = InlineKeyboardButton('Назад', callback_data='Список курсов')
    lessons_kb.insert(back_btn)

    await bot.edit_message_text('Ваши занятия на курсе ' + course, user_id, message_id)
    await bot.edit_message_reply_markup(user_id, message_id, reply_markup=lessons_kb)


# Come back to all courses
@dp.callback_query_handler(state=States.STUDENT_STATE, text='Список курсов')
async def process_back_course_btn(callback_query: types.CallbackQuery):
    await course_menu(callback_query.from_user.id, callback_query.message.message_id, mode='edit')


# Add new course button
@dp.message_handler(state=States.STUDENT_STATE, text='Добавить курс')
async def process_add_course_btn(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)      # take current state of user
    await state.set_state(States.STUDENT_KEY_STATE[0])      # change user's state
    await msg.answer('Введите пожалуйста ключ')


# Add key
@dp.message_handler(state=States.STUDENT_KEY_STATE)
async def process_student_key(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)     # take current state of user
    await state.set_state(States.STUDENT_STATE[0])      # change user's state
    text_ = msg.text
    if text_ == 'newCourse':
        await msg.answer('Поздравляем вы успешно добавили себе курс ' + text_ + '.')
    else:
        await msg.answer('Такого ключа не существует.')


# Query button
@dp.message_handler(state=States.STUDENT_STATE, text='Запрос')
async def process_query_btn(msg: types.Message):
    ask_question_btn = InlineKeyboardButton('Задать вопрос', callback_data='student question')
    illness_btn = InlineKeyboardButton('Я заболел', callback_data='student sick')
    feedback_btn = InlineKeyboardButton('Получить фидбек', callback_data='student feedback')
    query_kb = InlineKeyboardMarkup().add(ask_question_btn)
    query_kb.add(illness_btn).add(feedback_btn)
    await msg.answer('Выберите действие: ', reply_markup=query_kb)


# Ask question button
@dp.callback_query_handler(state=States.STUDENT_STATE, text='student question')
async def process_question_btn(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)  # take current state of user
    await state.set_state(States.STUDENT_QUESTION_STATE[0])  # change user's state
    await msg.answer('Задайте вопрос')


# Forward message to the admin chat
@dp.message_handler(state=States.STUDENT_QUESTION_STATE)
async def process_student_question(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)  # take current state of user
    await state.set_state(States.STUDENT_STATE[0])   # change user's state
    # TODO: forward message to the admins' chat
    text_ = msg.text
    await msg.answer('Ваше сообщение зарегестрировано под номер 10000. Ожидайте ответа в ближайшее время.')


# Exit button
@dp.message_handler(state=States.STUDENT_STATE, text='Выйти')
async def process_schedule_btn(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)  # take current state
    await state.set_state(States.UNAUTHORIZED_STATE[0])  # unauthorize user
    await msg.answer('Вы успешно вышли из системы.',
                     parse_mode=ParseMode.MARKDOWN,
                     reply_markup=ReplyKeyboardRemove())
