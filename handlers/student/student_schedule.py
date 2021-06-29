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


async def get_student_schedule(sql_student_id=0):
    # TODO: generate schedule message
    if sql_student_id == 0:
        return text(bold('Python'), ' 10:00-10:30', sep='')
    else:
        return text(bold('Java'), ' 10:00-10:30', sep='')


# Schedule button
@dp.message_handler(state=States.STUDENT_STATE, text='Расписание')
async def process_schedule_btn(msg: types.Message):
    schedule = await get_student_schedule(msg.chat.id)    #student_id in sql datebase == telegram user id ?
    await msg.answer(schedule, parse_mode=ParseMode.MARKDOWN)
