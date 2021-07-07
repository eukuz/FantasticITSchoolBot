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
from handlers.parent.parent_main import get_group_name_by_id


async def send_hw_to_group(hw_sender_id, group_name, hw_head_text, hw_main_text):
    # TODO отправить сообщение в группу
    # TODO сделать рассылку сразу по всем курсам (добавить кнопку "Всем")
    pass


@dp.callback_query_handler(Text(startswith='create_hw'), state=States.TEACHER_STATE)
async def process_publish_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    group_id = callback_query.data.split('|')[1]  # название выбранного элемента ("курс + группа")
    await state.finish()
    await state.set_state(States.TEACHER_CREATE_HW_1_STATE[0])
    await state.update_data(group_id=await get_group_name_by_id(group_id))
    await bot.send_message(callback_query.from_user.id, 'Введите заголовок урока')


@dp.message_handler(state=States.TEACHER_CREATE_HW_1_STATE)
async def process_post_message(msg: types.Message, state: FSMContext):
    await state.update_data(lesson=msg.text)
    await msg.reply(text('Вы уверены что хотите оставить этот заголовок урока?'), reply_markup=sure_kb)


@dp.message_handler(state=States.TEACHER_CREATE_HW_2_STATE, content_types=['text', 'photo', 'document', 'audio', 'voice', 'video'])
async def process_post_message(msg: types.Message, state: FSMContext):
    await msg.reply(text('Вы уверены что хотите отправить это ДЗ?'), reply_markup=sure_kb)


# Запоминаем заголовок для ДЗ
@dp.callback_query_handler(state=States.TEACHER_CREATE_HW_1_STATE, text='yes')
async def process_post_message(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    state_data = await state.get_data()
    group_id = state_data['group_id']
    lesson = state_data['lesson']
    await state.finish()
    # Пересохраняем данные в новый state
    await state.set_state(States.TEACHER_CREATE_HW_2_STATE[0])
    await state.update_data(group_id=group_id)
    await state.update_data(lesson=lesson)

    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(text('Отправьте файл с ДЗ, можно добавить описание в сообщении с файлом'),
                                user_id, message_id)


# Запоминаем и отправляем ДЗ
@dp.callback_query_handler(state=States.TEACHER_CREATE_HW_2_STATE, text='yes')
async def process_yes_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    group_id = user_data['group_id']
    lesson = user_data['lesson']
    teacher_id = callback_query.from_user.id
    message_id = callback_query.message.reply_to_message.message_id
    group_name = await get_group_name_by_id(group_id)
    await bot.edit_message_text(f'ДЗ с заголовком "{lesson}" будет отправлено для {group_name}.',
                                callback_query.from_user.id, callback_query.message.message_id)
    await send_hw_to_group(teacher_id, message_id, group_id, lesson)
    await state.finish()
    await state.set_state(States.TEACHER_STATE[0])