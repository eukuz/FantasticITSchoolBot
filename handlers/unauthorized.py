from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from utils import States
from loader import dp, bot
from .student_buttons import parent_in_system_kb
from .student_buttons import student_main_kb
from .parent import parent_main_kb
from .tutor_main import tutor_main_kb
from .tutor_gen_keys import *
from .tutors_create import *


@dp.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)  # take current state of user
    await state.set_state(States.UNAUTHORIZED_STATE[0])  # user is unauthorized in the very beginning
    await message.answer('Привет, я бот введите пожалуйста ключ :)',
                         reply_markup=ReplyKeyboardRemove())       # write welcome message to user


# Authorization works only in UNAUTHORIZED state
@dp.message_handler(state=States.UNAUTHORIZED_STATE)
async def authorization(msg: types.Message):
    text_ = msg.text                                  # take user's message
    state = dp.current_state(user=msg.from_user.id)  # take current state
    # TODO: check user's authorization code
    if text_ == 'studentCode':
        await state.set_state(States.STUDENT_STATE[0])  # change user's state to STUDENT
        # add main buttons for student
        await msg.answer('Вы успешно авторизовались как ученик.',
                         reply_markup=student_main_kb)

        await msg.answer(text('Пожалуйста, зарегестрируйте родителя.'),
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=parent_in_system_kb)
    elif text_ == 'parentCode':
        await state.set_state(States.PARENT_STATE[0])   # change user's state to PARENT
        # TODO: find children of the parent
        await msg.answer('Вы успешно авторизовались как родитель. Вас добавили дети: ',
                         reply_markup=parent_main_kb)
    elif text_ == 'tutorCode':
        await state.set_state(States.TUTOR_STATE[0])  # change user's state to TUTOR
        await msg.answer('Вы успешно авторизовались как куратор.',
                         reply_markup=tutor_main_kb)
    elif text_ == 'teacherCode':
        await state.set_state(States.TEACHER_STATE[0])  # change user's state to TEACHER
        await msg.answer('Вы успешно авторизовались как учитель.')
    else:
        await msg.answer('Такого ключа не существует, пожалуйста, попробуйте еще раз.')  # code is not correct


@dp.message_handler(state='*')
async def echo_message(msg: types.Message):
    await msg.answer('Я вас не понял. Попробуйте другую команду.')