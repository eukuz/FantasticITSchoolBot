from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import text
from aiogram.types import ParseMode
from aiogram import types
from loader import bot
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from .teacher_main import teacher_main_kb

teacher_cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))


@dp.message_handler(state=States.TEACHER_STATE, text='Добавить курс')
async def process_add_course_btn(msg: types.Message):
    await dp.current_state(user=msg.from_user.id).set_state(States.TEACHER_ADD_COURSE_STATE[0])
    await msg.answer('Введите пожалуйста ключ', reply_markup=teacher_cancel_kb)


@dp.message_handler(state=States.TEACHER_ADD_COURSE_STATE)
async def process_teacher_key(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    text_ = msg.text
    if text_ == 'Отмена':
        await state.set_state(States.TEACHER_STATE[0])
        await msg.answer('Отменено', reply_markup=teacher_main_kb)
    else:
        # TODO: check user's authorization code
        check = True
        if not check:
            await msg.answer('Такого ключа не существует.')
        elif text_[:3] == 'COU':
            await state.set_state(States.TEACHER_STATE[0])
            await msg.answer('Поздравляем вы успешно добавили себе курс ' + text_ + '.', reply_markup=teacher_main_kb)
        else:
            await msg.answer('Ошибка. Пожалуйста обратитесь к администрации.')

