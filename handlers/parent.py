from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from .unauthorized import dp
from .buttons import get_student_schedule
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import bot
from utils import States
from aiogram.dispatcher.filters import Text

parent_schedule_btn = KeyboardButton('Расписание') #
parent_query_btn = KeyboardButton('Запрос')
parent_exit_btn = KeyboardButton('Выйти')
parent_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(parent_schedule_btn,
                                                                parent_query_btn,
                                                               parent_exit_btn)


@dp.message_handler(state=States.PARENT_STATE, text='Расписание')
async def process_schedule_btn(msg: types.Message):
    # TODO: get children data
    for student_id, name in {0: "Алексей", 1: "Мария"}.items():
        schedule = text(bold(name), "\n", await get_student_schedule(student_id))
        await msg.answer(schedule, parse_mode=ParseMode.MARKDOWN)
