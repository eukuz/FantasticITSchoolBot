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
from db.app_db import Database

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
    group = db.get_group(group_key=text_[3:])
    if group is None or text_[:3] != 'GRO':
        await msg.answer('Такого ключа не существует.')
    else:
        await msg.answer('Поздравляем вы успешно добавили себе курс ' + group.name + '.')
        student = db.get_student(UID=msg.from_user.id)
        db.map_student_group(student.student_key, text_[3:])
