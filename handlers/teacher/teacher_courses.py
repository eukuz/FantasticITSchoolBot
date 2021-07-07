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
from handlers.parent.parent_main import get_group_name_by_id

async def get_student_groups(student_id):
    # TODO get student groups data
    # формат {group_id : group_name}
    return {1: 'Курс/Группа 1',
            2: 'Курс/Группа 2'}


async def coursegroup_menu(user_id, message_id, mode):
    groups = await get_student_groups(user_id)
    groups_kb = InlineKeyboardMarkup()
    for group_id, group_name in groups.items():
        student_btn = InlineKeyboardButton(group_name, callback_data='group_id|' + str(group_id))
        groups_kb.insert(student_btn)
    groups_kb.insert(InlineKeyboardButton("Отмена", callback_data='cancel'))

    if mode == 'answer':
        await bot.send_message(user_id, 'Ваши курсы: ', parse_mode=ParseMode.MARKDOWN, reply_markup=groups_kb)
    else:
        await bot.edit_message_text('Ваши курсы: ', user_id, message_id)
        await bot.edit_message_reply_markup(user_id, message_id, reply_markup=groups_kb)


# Показать список "курс + группа" в первый раз при нажатии кнопки "Мои курсы"
@dp.message_handler(state=States.TEACHER_STATE, text='Мои курсы')
async def process_courses_btn(msg: types.Message):
    await coursegroup_menu(msg.from_user.id, msg.message_id, mode='answer')


# Показать список "курс + группа" снова, при нажатии кнопки "Назад" из меню выбранного элемента
@dp.callback_query_handler(state=States.TEACHER_STATE, text='Назад в список курсов')
async def process_back_course_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await coursegroup_menu(callback_query.from_user.id, callback_query.message.message_id, mode='edit')


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
