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
from .teacher_main import sure_kb
from handlers.parent.parent_main import send_request_to_group,get_group_name_by_id
from config import GROUP


async def send_message_to_group(teacher_id, message_id):
    bot.copy_message(chat_id=GROUP,
                     from_chat_id=teacher_id,
                     message_id=message_id)
    # TODO разослать сооьщение по группам
    pass


@dp.callback_query_handler(Text(startswith='create_massmessage'), state=States.TEACHER_STATE)
async def process_publish_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    group_id = callback_query.data.split('|')[1]
    await state.finish()
    await state.set_state(States.TEACHER_CREATE_MASS_MESSAGE_STATE[0])
    await state.update_data(group_id=group_id)
    await bot.send_message(callback_query.from_user.id, 'Введите сообщение для рассылки')


@dp.message_handler(state=States.TEACHER_CREATE_MASS_MESSAGE_STATE, content_types=['text', 'photo', 'document', 'audio','voice', 'video'])
async def process_post_message(msg: types.Message, state: FSMContext):
    await msg.reply(text('Вы уверены что хотите отправить это сообщение?'), reply_markup=sure_kb)


# Запоминаем сообщение и отправляем в рассылку
@dp.callback_query_handler(state=States.TEACHER_CREATE_MASS_MESSAGE_STATE, text='yes')
async def process_yes_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    user_data = await state.get_data()
    group_id = user_data['group_id']
    teacher_id = callback_query.from_user.id
    message_id = callback_query.message.reply_to_message.message_id
    group_name = await get_group_name_by_id(group_id)

    await bot.edit_message_text(f'Сообщение будет отправлено для {group_name}.',
                                callback_query.from_user.id, callback_query.message.message_id)
    await send_message_to_group(teacher_id, message_id)
    await state.finish()
    await state.set_state(States.TEACHER_STATE[0])