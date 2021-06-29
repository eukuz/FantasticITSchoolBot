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


parent_in_system_btn = InlineKeyboardButton('Мой родитель уже в системе', callback_data='parent in system')
parent_register_btn = InlineKeyboardButton('Сгенерировать ключ для родителя.', callback_data='parent registration')
parent_in_system_kb = InlineKeyboardMarkup().insert(parent_in_system_btn).insert(parent_register_btn)


# Parent in system button
@dp.callback_query_handler(state=States.STUDENT_STATE, text='parent in system')
async def process_callback_parent_in_system(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(States.PARENT_REGISTRATION_STATE[0])
    await bot.send_message(callback_query.from_user.id, 'Пожалуйста введите ключ вашего родителя.')


# Catch parent's key
@dp.message_handler(state=States.PARENT_REGISTRATION_STATE)
async def process_parent_key(msg: types.Message):
    text_ = msg.text
    # TODO: check that key is correct
    check = True
    if not check:
        await msg.answer('Такого ключа не существует, пожалуйста, попробуйте еще раз.')
    elif text_[:3] == 'PAR':
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(States.STUDENT_STATE[0])
        await msg.answer('Вы успешно зарегестрировали родителя.')
    else:
        await msg.answer('Ошибка. Пожалуйста обратитесь к администрации.')


# Register parent
@dp.callback_query_handler(state=States.STUDENT_STATE | States.PARENT_REGISTRATION_STATE, text='parent registration')
async def process_callback_parent_register(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(States.STUDENT_STATE[0])
    parent_code = KeyGen.generateNKeysParents(1).pop()
    await bot.edit_message_reply_markup(callback_query.from_user.id,
                                        callback_query.message.message_id,
                                        reply_markup=None)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id,
                           text('Ключ для вашего родителя: ', code(parent_code), '.', sep=''),
                           parse_mode=ParseMode.MARKDOWN)
