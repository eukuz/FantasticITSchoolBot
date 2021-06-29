from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import dp, bot
from utils import States
from aiogram.dispatcher.filters import Text
from KeyGen import KeyGen
from config import GROUP
from aiogram.dispatcher import FSMContext


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
