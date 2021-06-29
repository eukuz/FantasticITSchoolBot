from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp
from handlers.student.student_schedule import get_student_schedule
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from aiogram import types
from utils import States

parent_schedule_btn = KeyboardButton('Расписание')  #
parent_query_btn = KeyboardButton('Запрос')
parent_exit_btn = KeyboardButton('Выйти')
parent_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(parent_schedule_btn,
                                                               parent_query_btn,
                                                               parent_exit_btn)


@dp.message_handler(state=States.PARENT_STATE, text='Расписание')
async def process_schedule_btn(msg: types.Message):
    # TODO: get children data
    students = {0: "Алексей", 1: "Мария"}
    for student_id, name in students.items():
        schedule = text(bold(name), "\n", await get_student_schedule(student_id))
        await msg.answer(schedule, parse_mode=ParseMode.MARKDOWN)
