from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from aiogram.utils.markdown import text
from aiogram.types import ParseMode
from aiogram import types
from loader import bot
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

# Главная клавиатура учителя
teacher_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Мои курсы'),
                                                                KeyboardButton('Добавить курс'),
                                                                KeyboardButton('Выйти'))

# Кнопки для подтверждения пользовательского ввода
sure_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data='yes'),
                                     InlineKeyboardButton('Изменить', callback_data='edit'),
                                     InlineKeyboardButton('Отмена', callback_data='cancel'))


# Возвращение пользователя в TEACHER_STATE при отмене ввода
@dp.callback_query_handler(state=States.TEACHER_CREATE_MASS_MESSAGE_STATE
                                 | States.TEACHER_CREATE_HW_1_STATE
                                 | States.TEACHER_CREATE_HW_2_STATE
                                 | States.TEACHER_STATE,
                           text='cancel')
async def process_cancel_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text('Действие отменено.', user_id, message_id)
    await state.finish()
    await state.set_state(States.TEACHER_STATE[0])


# Повтор ввода; состояние (state) не меняется
@dp.callback_query_handler(state=States.TEACHER_CREATE_MASS_MESSAGE_STATE
                                 | States.TEACHER_CREATE_HW_1_STATE
                                 | States.TEACHER_CREATE_HW_2_STATE,
                           text='edit')
async def process_edit_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text('Введите сообщение еще раз.', user_id, message_id)
