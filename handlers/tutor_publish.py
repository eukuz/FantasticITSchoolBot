from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from .unauthorized import dp
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import bot
from utils import States
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


@dp.message_handler(state=States.TUTOR_STATE, text='Опубликовать пост')
async def process_publish_btn(msg: types.Message):
    # TODO: get courses or all courses
    groups = ['Python Group 1', 'Java Group 2', 'C++ Group 3', 'всех']
    groups_kb = InlineKeyboardMarkup()
    for i in range(len(groups)):
        group_btn = InlineKeyboardButton(groups[i], callback_data='groups ' + groups[i])
        groups_kb.insert(group_btn)

    await msg.answer('Для кого?', reply_markup=groups_kb)


@dp.callback_query_handler(Text(startswith='groups'), state=States.TUTOR_STATE)
async def process_group_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    group = ''
    name = callback_query.data.split()
    for i in range(1, len(name)):
        group = group + ' ' + name[i]
    await state.update_data(group=group)
    await state.set_state(States.PUBLISH_POST_STATE[0])
    await bot.send_message(callback_query.from_user.id, 'Введите сообщение для ' + group)


@dp.message_handler(state=States.PUBLISH_POST_STATE)
async def process_post_message(msg: types.Message, state: FSMContext):
    text_ = msg.text
    await state.update_data(text=text_)
    yes_btn = InlineKeyboardButton('Да', callback_data='yes')
    edit_btn = InlineKeyboardButton('Изменить', callback_data='edit')
    cancel_btn = InlineKeyboardButton('Отмена', callback_data='cancel')
    sure_kb = InlineKeyboardMarkup().add(yes_btn, edit_btn, cancel_btn)
    await msg.answer(text('Вы уверены что хотите отправить это сообщение?'), reply_markup=sure_kb)


@dp.callback_query_handler(state=States.PUBLISH_POST_STATE, text='yes')
async def process_yes_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    await bot.edit_message_text(text('Сообщение: "', user_data['text'], '" будет отправлено для ',
                     user_data['group'], '.', sep=''),
                     callback_query.from_user.id, callback_query.message.message_id)
    await state.finish()
    await state.set_state(States.TUTOR_STATE[0])


@dp.callback_query_handler(state=States.PUBLISH_POST_STATE, text='edit')
async def process_edit_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text('Введите сообщение еще раз.', user_id, message_id)


@dp.callback_query_handler(state=States.PUBLISH_POST_STATE, text='cancel')
async def process_cancel_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text('Отменено.', user_id, message_id)
    await state.finish()
    await state.set_state(States.TUTOR_STATE[0])