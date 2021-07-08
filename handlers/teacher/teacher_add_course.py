from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import text
from aiogram.types import ParseMode
from aiogram import types
from loader import bot
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
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
        if text_[:3] == 'COU':
            course = db.get_course(course_key=text_[3:])
            if course is not None:
                    await state.set_state(States.TEACHER_STATE[0])
                    groups = db.get_group(course_id=course.id)
                    if groups is None:
                        return
                    if type(groups) is not list:
                        groups = [groups]
                    for i in range(len(groups)):
                        db.set_group(groups[i], teacher_id=db.get_teacher(UID=msg.from_user.id).id)
                    await msg.answer('Поздравляем вы успешно добавили себе курс ' + str(course.name) + '.',
                                     reply_markup=teacher_main_kb)
            else:
                await msg.answer('Такого ключа не существует.')
        else:
            await msg.answer('Ошибка. Пожалуйста обратитесь к администрации.')

