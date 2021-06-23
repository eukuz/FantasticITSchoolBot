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
from KeyGen import KeyGen


parent_in_system_btn = InlineKeyboardButton('Мой родитель уже в системе', callback_data='parent in system')
parent_register_btn = InlineKeyboardButton('Сгенерировать ключ для родителя.', callback_data='parent registration')
parent_in_system_kb = InlineKeyboardMarkup().insert(parent_in_system_btn).insert(parent_register_btn)

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


async def get_student_schedule(sql_student_id=0):
    # TODO: generate schedule message
    if sql_student_id == 0:
        return text(bold('Python'), ' 10:00-10:30', sep='')
    else:
        return text(bold('Java'), ' 10:00-10:30', sep='')


# Parent in system button
@dp.callback_query_handler(state=States.STUDENT_STATE, text='parent in system')
async def process_callback_parent_in_system(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(States.PARENT_REGISTRATION_STATE[0])
    await bot.send_message(callback_query.from_user.id, 'Пожалуйста введите ключ вашего родителя.')


# Catch parent's key
@dp.message_handler(state=States.PARENT_REGISTRATION_STATE)
async def process_parent_key(msg: types.Message):
    text_ = msg.text
    # TODO: check that key is correct
    check = True
    if not check:
        await msg.answer('Такого ключа не существует, пожалуйста, попробуйте еще раз.')
    elif text_ == 'PAR':
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(States.STUDENT_STATE[0])
        await msg.answer('Вы успешно зарегестрировали родителя.')
    else:
        await msg.answer('Ошибка. Пожалуйста обратитесь к администрации.')


# Register parent
@dp.callback_query_handler(state=States.STUDENT_STATE | States.PARENT_REGISTRATION_STATE, text='parent registration')
async def process_callback_parent_register(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(States.STUDENT_STATE[0])
    # TODO: generate normal parent code
    parentCode = KeyGen.generateNKeysParents(1).pop()
    await bot.edit_message_reply_markup(callback_query.from_user.id,
                                        callback_query.message.message_id,
                                        reply_markup=None)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id,
                           text('Ключ для вашего родителя: ', code(parentCode), '.', sep=''),
                           parse_mode=ParseMode.MARKDOWN)


# Schedule button
@dp.message_handler(state=States.STUDENT_STATE, text='Расписание')
async def process_schedule_btn(msg: types.Message):
    schedule = await get_student_schedule(msg.chat.id)    #student_id in sql datebase == telegram user id ?
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
    # TODO: check that key is correct
    check = True
    if not check:
        await msg.answer('Такого ключа не существует.')
    elif text_[:3] == 'COU':
        await msg.answer('Поздравляем вы успешно добавили себе курс ' + text_ + '.')
    else:
        await msg.answer('Ошибка. Пожалуйста обратитесь к администрации.')


# Query button
def create_query_kb(main):
    ask_question_btn = InlineKeyboardButton('Задать вопрос', callback_data='question')
    illness_btn = InlineKeyboardButton('Сообщить о болезни', callback_data='sick')
    feedback_btn = InlineKeyboardButton('Получить фидбек', callback_data='feedback')
    query_kb = InlineKeyboardMarkup().add(ask_question_btn).add(illness_btn).add(feedback_btn)
    if not main:
        back_btn = InlineKeyboardButton('Назад', callback_data='back to main')
        query_kb.add(back_btn)
    return query_kb


@dp.message_handler(state=States.STUDENT_STATE | States.PARENT_STATE, text='Запрос')
async def process_query_btn(msg: types.Message):
    query_kb = create_query_kb(True)
    await msg.answer('Выберите действие: ', reply_markup=query_kb)


# Ask question button
@dp.callback_query_handler(state=States.STUDENT_STATE | States.PARENT_STATE, text='question')
async def process_question_btn(callback_query: types.CallbackQuery):
    # await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)  # take current state of user
    s = await state.get_state()
    if s == States.STUDENT_STATE[0]:
        await state.set_state(States.STUDENT_QUESTION_STATE[0])  # change user's state
    else:
        await state.set_state(States.PARENT_QUESTION_STATE[0])

    await callback_query.answer('Задайте вопрос')
    query_kb = create_query_kb(False)
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=query_kb)


# Forward message to the admin chat
@dp.message_handler(state=States.STUDENT_QUESTION_STATE | States.PARENT_QUESTION_STATE)
async def process_student_question(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)  # take current state of user
    s = await state.get_state()
    if s == States.STUDENT_QUESTION_STATE[0]:
        await state.set_state(States.STUDENT_STATE[0])   # change user's state
    else:
        await state.set_state(States.PARENT_STATE[0])
    # TODO: forward message to the admins' chat
    text_ = msg.text
    await msg.answer('Ваше сообщение зарегестрировано под номер 10000. Ожидайте ответ в ближайшее время.')
    # TODO: remove Back button from prev inline message


# Report about sickness
@dp.callback_query_handler(state=States.STUDENT_STATE | States.PARENT_STATE, text='sick')
async def process_sickness_btn(callback_query: types.CallbackQuery):
    # await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)  # take current state of user
    s = await state.get_state()
    if s == States.STUDENT_STATE[0]:
        await state.set_state(States.STUDENT_SICK_STATE[0])  # change user's state
    else:
        await state.set_state(States.PARENT_SICK_STATE[0])

    await callback_query.answer('Пожалуйста, предоставьте подтверждающий документ')
    query_kb = create_query_kb(False)
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=query_kb)


# Forward evidence to the admins' chat
@dp.message_handler(state=States.STUDENT_SICK_STATE | States.PARENT_SICK_STATE)
async def process_sick_evidence(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)  # take current state of user
    s = await state.get_state()
    if s == States.STUDENT_SICK_STATE[0]:
        await state.set_state(States.STUDENT_STATE[0])   # change user's state
    else:
        await state.set_state(States.PARENT_STATE[0])
    # TODO: forward message to the admins' chat
    text_ = msg.text
    await msg.answer('Принято, ожидайте подтверждения.')
    # TODO: remove Back button from prev inline message
    # query_kb = create_query_kb(True)
    # await bot.edit_message_reply_markup()


# Feedback button
@dp.callback_query_handler(state=States.STUDENT_STATE | States.PARENT_STATE, text='feedback')
async def process_feedback_btn(callback_query: types.CallbackQuery):
    # TODO: ask feedback from admins
    await callback_query.answer('Запрос отправлен. Ожидайте ответа')


# Back to the main query menu button
@dp.callback_query_handler(state=States.STUDENT_QUESTION_STATE | States.STUDENT_SICK_STATE |
                                 States.PARENT_QUESTION_STATE | States.PARENT_SICK_STATE |
                                 States.STUDENT_STATE | States.PARENT_STATE, text='back to main')
async def process_back_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)  # take current state of user
    s = await state.get_state()
    if s == States.STUDENT_QUESTION_STATE[0] or s == States.STUDENT_SICK_STATE[0] or s == States.STUDENT_STATE[0]:
        await state.set_state(States.STUDENT_STATE[0])  # change user's state
    else:
        await state.set_state(States.PARENT_STATE[0])
    query_kb = create_query_kb(True)
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=query_kb)


# Exit button
@dp.message_handler(state=States.STUDENT_STATE | States.PARENT_STATE | States.TUTOR_STATE, text='Выйти')
async def process_exit_btn(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)  # take current state
    await state.set_state(States.UNAUTHORIZED_STATE[0])  # unauthorize user
    await msg.answer('Вы успешно вышли из системы.',
                     parse_mode=ParseMode.MARKDOWN,
                     reply_markup=ReplyKeyboardRemove())
