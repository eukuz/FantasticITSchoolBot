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
student_question_btn = KeyboardButton('Задать вопрос')
student_add_course_btn = KeyboardButton('Добавить курс')
student_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(student_schedule_btn,
                                                                student_courses_btn,
                                                                student_add_course_btn,
                                                                student_question_btn)


@dp.callback_query_handler(state=States.STUDENT_STATE, text='parent in system')
async def process_callback_parent_in_system(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # TODO: what to do?
    await bot.send_message(callback_query.from_user.id, 'Спасибо, мы запомнили :)')


@dp.message_handler(state='*', text='Расписание')
async def process_schedule_btn(msg: types.Message):
    # TODO: generate schedule message
    schedule = text(bold("Python"), " 10:00-10:30", sep="")
    await msg.answer(schedule, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state='*', text='Мои курсы')
async def process_courses_btn(msg: types.Message):
    # TODO: generate list of courses
    courses = ['Python', 'Java', 'C++']
    courses_kb = InlineKeyboardMarkup()
    for i in range(len(courses)):
        courses_btn = InlineKeyboardButton(courses[i], callback_data=courses[i])
        courses_kb.insert(courses_btn)

    await msg.answer("Ваши курсы: ", parse_mode=ParseMode.MARKDOWN, reply_markup=courses_kb)
