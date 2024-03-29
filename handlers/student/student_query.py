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


# Query button
def create_query_kb(main):
    ask_question_btn = InlineKeyboardButton('Задать вопрос', callback_data='question')
    illness_btn = InlineKeyboardButton('Сообщить о болезни', callback_data='sick')
    feedback_btn = InlineKeyboardButton('Получить фидбек', callback_data='feedback')
    query_kb = InlineKeyboardMarkup().add(ask_question_btn).add(illness_btn).add(feedback_btn)
    if not main:
        back_btn = InlineKeyboardButton('Назад', callback_data='back to main')
        query_kb.add(back_btn)
    return query_kb


@dp.message_handler(state=States.STUDENT_STATE, text='Запрос')
async def process_query_btn(msg: types.Message):
    query_kb = create_query_kb(True)
    await msg.answer('Выберите действие: ', reply_markup=query_kb)


# Ask question button
@dp.callback_query_handler(Text(startswith='question'), state=States.STUDENT_STATE)
async def process_question_btn(callback_query: types.CallbackQuery, state: FSMContext):
    # Find role of a user
    s = await state.get_state()
    if s == States.STUDENT_STATE[0]:
        role = 'student'
    else:
        role = 'parent'
    # Change state to a question state
    await state.set_state(States.QUESTION_STATE[0])
    # Remember user's role and message id
    await state.update_data(role=role, msg_id=callback_query.message.message_id)
    # Answer to query
    await callback_query.answer('Задайте вопрос')
    # Answer to user
    query_kb = create_query_kb(False)
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=query_kb)


# Forward message to the admin chat
@dp.message_handler(state=States.QUESTION_STATE)
async def process_student_question(msg: types.Message, state: FSMContext):
    # Change state depending on user's role
    user_data = await state.get_data()
    if user_data['role'] == 'student':
        await state.set_state(States.STUDENT_STATE[0])   # change user's state
    else:
        await state.set_state(States.PARENT_STATE[0])
    query_kb = create_query_kb(True)
    await bot.edit_message_reply_markup(msg.from_user.id, user_data['msg_id'], reply_markup=query_kb)
    await msg.answer('Ваше сообщение направлено администраторам. Ожидайте ответ в ближайшее время.')
    # Forward message to the admins' chat
    user_id = msg.from_user.id
    user_name = msg.from_user.full_name
    alias = msg.from_user.username
    await bot.send_message(chat_id=GROUP,
                           text=text(code(user_id), '.', 'Вопрос от ', user_name, '(@', alias, ').', sep=''),
                           parse_mode=ParseMode.MARKDOWN)
    await msg.forward(chat_id=GROUP)


# Report about sickness
@dp.callback_query_handler(state=States.STUDENT_STATE, text='sick')
async def process_sickness_btn(callback_query: types.CallbackQuery, state: FSMContext):
    # await bot.answer_callback_query(callback_query.id)
    s = await state.get_state()
    if s == States.STUDENT_STATE[0]:
        role = 'student'
    else:
        role = 'parent'
    # Change state to a sick state
    await state.set_state(States.SICK_STATE[0])
    # Remember user's role and message id
    await state.update_data(role=role, msg_id=callback_query.message.message_id)
    # Answer to query
    await callback_query.answer('Пожалуйста, предоставьте подтверждающий документ.')
    query_kb = create_query_kb(False)
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=query_kb)


# Forward evidence to the admins' chat
@dp.message_handler(state=States.SICK_STATE, content_types=['photo', 'document', 'text'])
async def process_sick_evidence(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    # Delete Back button from the inline buttons
    query_kb = create_query_kb(True)
    await bot.edit_message_reply_markup(msg.from_user.id, user_data['msg_id'], reply_markup=query_kb)
    await msg.answer('Принято, ожидайте подтверждения.')
    # Forward message to admins chat
    user_id = msg.from_user.id
    user_name = msg.from_user.full_name
    alias = msg.from_user.username
    await bot.send_message(chat_id=GROUP,
                           text=text(code(user_id), '.', 'Справка от ', user_name, '(@', alias, ').', sep=''),
                           parse_mode=ParseMode.MARKDOWN)
    await msg.forward(chat_id=GROUP)
    # Change state
    await state.finish()
    if user_data['role'] == 'student':
        await state.set_state(States.STUDENT_STATE[0])   # change user's state
    else:
        await state.set_state(States.PARENT_STATE[0])


# Feedback button
@dp.callback_query_handler(state=States.STUDENT_STATE, text='feedback')
async def process_feedback_btn(callback_query: types.CallbackQuery):
    user_name = callback_query.from_user.full_name
    user_id = callback_query.from_user.id
    alias = callback_query.from_user.username
    await callback_query.answer('Запрос отправлен. Ожидайте ответа')
    await bot.send_message(chat_id=GROUP,
                           text=text(code(user_id), '.', 'Требуется фидбек для ', user_name, '(@', alias, ').', sep=''),
                           parse_mode=ParseMode.MARKDOWN)


# Back to the main query menu button
@dp.callback_query_handler(state=States.QUESTION_STATE, text='back to main')
async def process_back_button(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    await state.finish()
    if user_data['role'] == 'student':
        await state.set_state(States.STUDENT_STATE[0])
    else:
        await state.set_state(States.PARENT_STATE[0])
    query_kb = create_query_kb(True)
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id,
                                        reply_markup=query_kb)
