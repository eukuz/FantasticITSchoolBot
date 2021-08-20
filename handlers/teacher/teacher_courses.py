from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot, db
from aiogram.utils.markdown import text
from aiogram.types import ParseMode
from aiogram import types
from loader import bot
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from handlers.parent.parent_main import get_group_name_by_id


# Mеню выбора группы для учителя
async def group_menu(teacher_id, message_id, display_text, mode):
    groups = db.get_group(teacher_UID=teacher_id)
    print(groups)
    if groups is None:
        await bot.send_message(teacher_id, "У вас ещё нет курсов")
        return
    if type(groups) is not list:
        groups = [groups]
    groups_kb = InlineKeyboardMarkup()
    for i in range(len(groups)):
        groups_btn = InlineKeyboardButton(groups[i].name, callback_data='group_id|' + str(groups[i].id))
        groups_kb.insert(groups_btn)
    if mode == 'answer':
        await bot.send_message(teacher_id, display_text, parse_mode=ParseMode.MARKDOWN, reply_markup=groups_kb)
    else:
        await bot.edit_message_text(display_text, teacher_id, message_id)
        await bot.edit_message_reply_markup(teacher_id, message_id, reply_markup=groups_kb)


# Показать список "курс + группа" в первый раз при нажатии кнопки "Мои курсы"
@dp.message_handler(state=States.TEACHER_STATE, text='Мои курсы')
async def process_courses_btn(msg: types.Message):
    await group_menu(msg.from_user.id, msg.message_id, display_text="Ваши курсы", mode='answer')


# Показать список "курс + группа" снова, при нажатии кнопки "Назад" из меню выбранного элемента
@dp.callback_query_handler(state=States.TEACHER_STATE, text='Назад в список курсов')
async def process_back_course_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await group_menu(callback_query.from_user.id, callback_query.message.message_id,
                     display_text="Ваши курсы",
                     mode='edit')


# Показать выбранный элемент из списка "курс + группа" и кнопки действий
@dp.callback_query_handler(Text(startswith='group_id'), state=States.TEACHER_STATE)
async def process_one_course_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    group_id = callback_query.data.split('|')[1]
    group_name = await get_group_name_by_id(group_id)

    create_hw_btn = InlineKeyboardButton('Создать ДЗ', callback_data='create_hw|' + group_id)
    send_hw_btn = InlineKeyboardButton('Отправить в рассылку', callback_data='create_massmessage|' + group_id)
    back_btn = InlineKeyboardButton('Назад', callback_data='Назад в список курсов')
    actions_kb = InlineKeyboardMarkup()
    actions_kb.row(create_hw_btn, send_hw_btn)
    actions_kb.row(back_btn)

    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    await bot.edit_message_text(f'Вы выбрали {group_name}', user_id, message_id, reply_markup=actions_kb)
