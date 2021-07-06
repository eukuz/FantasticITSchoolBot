from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import dp, db, bot
from utils import States
from aiogram.dispatcher.filters import Text
from KeyGen import KeyGen
from config import GROUP
from aiogram.dispatcher import FSMContext


# Creates course menu, can edit or answer to message
async def course_menu(user_id, message_id, mode):
    courses = db.get_group(student_UID=user_id)
    if type(courses) is not list:
        courses = [courses]
    courses_kb = InlineKeyboardMarkup()
    for i in range(len(courses)):
        courses_btn = InlineKeyboardButton(courses[i].name, callback_data='courses ' + courses[i].group_key)
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
    course = callback_query.data.split()[1]
    lessons = db.get_homework(group_key=course)
    lessons_kb = InlineKeyboardMarkup()
    if lessons is not None:
        if type(lessons) is not list:
            lessons = [lessons]
        for i in range(len(lessons)):
            lesson_btn = InlineKeyboardButton(str(i + 1), callback_data='presentation')  # send presentation for this lesson
            get_hw_btn = InlineKeyboardButton('Получить домашнее задание', callback_data='gethw ' + course + ' ' + lessons[i].hw_key)     # get homework
            send_hw_btn = InlineKeyboardButton('Отправить домашнее задание', callback_data='sendhw ' + course + ' ' + lessons[i].hw_key)  # send homework
            lessons_kb.row(lesson_btn, get_hw_btn, send_hw_btn)
    back_btn = InlineKeyboardButton('Назад', callback_data='Список курсов')
    lessons_kb.insert(back_btn)
    course_name = db.get_group(group_key=course).name
    await bot.edit_message_text('Ваши занятия на курсе ' + course_name, user_id, message_id)
    await bot.edit_message_reply_markup(user_id, message_id, reply_markup=lessons_kb)


# Send homework to the student
@dp.callback_query_handler(Text(startswith='gethw'), state=States.STUDENT_STATE)
async def process_get_hw_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    _, course, lesson = callback_query.data.split()
    # hw = db.get_homework(hw_key=lesson)


# Come back to all courses
@dp.callback_query_handler(state=States.STUDENT_STATE, text='Список курсов')
async def process_back_course_btn(callback_query: types.CallbackQuery):
    await course_menu(callback_query.from_user.id, callback_query.message.message_id, mode='edit')


# Send homework to the admins' chat
@dp.callback_query_handler(Text(startswith='sendhw'), state=States.STUDENT_STATE)
async def process_send_hw_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer('Пожалуйста отправьте домашнее задание')
    await state.set_state(States.STUDENT_HW_STATE[0])
    _, course, lesson = callback_query.data.split()
    await state.update_data(course=course, lesson=lesson)


@dp.message_handler(state=States.STUDENT_HW_STATE, content_types=['photo', 'document', 'text'])
async def catch_hw(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = msg.from_user.id
    user_name = msg.from_user.full_name
    alias = msg.from_user.username
    course = db.get_group(group_key=user_data['course']).name
    lesson = db.get_homework(hw_key=user_data['lesson']).id
    await bot.send_message(chat_id=GROUP,
                           text=text(code(user_id), '. Домашнее задание от ', user_name, ' (@', alias, ')',
                                     '. Курс ', course, '. Занятие ', lesson, sep=''),
                           parse_mode=ParseMode.MARKDOWN)
    await msg.forward(chat_id=GROUP)
    await state.finish()
    await state.set_state(States.STUDENT_STATE[0])


# Answer to callback query
@dp.callback_query_handler(Text(startswith='presentation'), state=States.STUDENT_STATE)
async def process_lesson_btn(callback_query: types.CallbackQuery):
    await callback_query.answer()
