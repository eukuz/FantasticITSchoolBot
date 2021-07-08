from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp, bot, db
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from aiogram import types
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from .parent_main import sure_kb, send_request_to_group, get_parent_name_by_id
from config import GROUP


# Родитель задаёт вопрос, не выбирая группу или ребёнка
@dp.callback_query_handler(state=States.PARENT_STATE, text='question')
async def process_question_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(States.PARENT_QUESTION_STATE[0])
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(text('Задайте вопрос'),
                                user_id, message_id)


@dp.message_handler(state=States.PARENT_QUESTION_STATE, content_types=['photo', 'document', 'text'])
async def process_post_message(msg: types.Message, state: FSMContext):
    await msg.reply(text('Вы уверены что хотите отправить этот вопрос?'), reply_markup=sure_kb)


@dp.callback_query_handler(state=States.PARENT_QUESTION_STATE, text='yes')
async def process_yes_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(text('Ваш вопрос направлен организаторам, ожидайте ответа в этом боте'),
                                callback_query.from_user.id, callback_query.message.message_id)

    message_id = callback_query.message.reply_to_message.message_id
    parent_id = callback_query.from_user.id

    await send_question_from_parent(parent_id, message_id)

    await state.finish()
    await state.set_state(States.PARENT_STATE[0])


async def send_question_from_parent(parent_id, message_id):
    parent_name = await get_parent_name_by_id(parent_id)
    parent_name_link = f'[{parent_name}](tg://user?id={str(parent_id)})'

    caption = f'Вопрос от родителя {parent_name_link}.'
    await send_request_to_group(parent_id, message_id, GROUP, caption)
