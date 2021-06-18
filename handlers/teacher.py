from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from .unauthorized import dp
from .student_buttons import get_student_schedule
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import bot
from utils import States
from aiogram.dispatcher.filters import Text

teacher_courses_btn = KeyboardButton('Мои курсы')
teacher_add_course_btn = KeyboardButton('Добавить курс')
teacher_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(teacher_courses_btn,
                                                                teacher_add_course_btn)

teacher_cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))


@dp.message_handler(state=States.TEACHER_STATE, text='Добавить курс')
async def process_add_course_btn(msg: types.Message):
    await dp.current_state(user=msg.from_user.id).set_state(States.TEACHER_ADD_COURSE_STATE[0])
    await msg.answer('Введите пожалуйста ключ', reply_markup=teacher_cancel_kb)


@dp.message_handler(state=States.TEACHER_ADD_COURSE_STATE)
async def process_teacher_key(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)     # take current state of user
    text_ = msg.text
    if text_ == 'Отмена':
        await state.set_state(States.TEACHER_STATE[0])      # change user's state
        await msg.answer('Отменено', reply_markup=teacher_main_kb)
    elif text_ == 'newCourse':
        await state.set_state(States.TEACHER_STATE[0])
        await msg.answer('Поздравляем вы успешно добавили себе курс ' + text_ + '.', reply_markup=teacher_main_kb)
    else:
        await msg.answer('Такого ключа не существует.')


@dp.message_handler(state=States.TEACHER_STATE, text='Мои курсы')
async def process_my_courses_btn(msg: types.Message):
    pass