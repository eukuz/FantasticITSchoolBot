from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from .unauthorized import dp
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import bot
from utils import States
from aiogram.dispatcher.filters import Text


@dp.message_handler(state=States.TUTOR_STATE, text='Создать')
async def process_create_btn(msg: types.Message):
    course_btn = InlineKeyboardButton('Курс', callback_data='create course')
    group_btn = InlineKeyboardButton('Группа', callback_data='create group')
    create_kb = InlineKeyboardMarkup().insert(course_btn).insert(group_btn)
    await msg.answer(text='Что будем создавать?', reply_markup=create_kb)


@dp.callback_query_handler(Text(startswith='create'), state=States.TUTOR_STATE)
async def process_create_course_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    await bot.send_message(user_id, text='Введите название.')
    state = dp.current_state(user=user_id)
    if callback_data.find('course') != -1:
        await state.set_state(States.CREATE_COURSE_STATE[0])
    elif callback_data.find('group') != -1:
        await state.set_state(States.CREATE_GROUP_STATE[0])


@dp.message_handler(state=States.CREATE_GROUP_STATE | States.CREATE_COURSE_STATE)
async def process_course_name(msg: types.Message):
    name = msg.text
    yes_btn = InlineKeyboardButton('Да', callback_data='yes' + name)
    edit_btn = InlineKeyboardButton('Изменить', callback_data='edit' + name)
    cancel_btn = InlineKeyboardButton('Отмена', callback_data='cancel' + name)
    sure_kb = InlineKeyboardMarkup().add(yes_btn, edit_btn, cancel_btn)
    await msg.answer(text('Вы хотите оставить название таким', name, '?'), reply_markup=sure_kb)


@dp.callback_query_handler(Text(startswith='yes'), state=States.CREATE_GROUP_STATE | States.CREATE_COURSE_STATE)
async def process_yes_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    name = callback_query.data[3:]
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    state = dp.current_state(user=user_id)
    s = await state.get_state()
    if s == States.CREATE_COURSE_STATE[0]:
        # TODO: create course
        await bot.edit_message_text(text('Курс', name, 'успешно создан.'), user_id, message_id)
    else:
        # TODO: generate list of courses
        courses = ['Python', 'Java', 'C++']
        courses_kb = InlineKeyboardMarkup()
        for i in range(len(courses)):
            courses_btn = InlineKeyboardButton(courses[i], callback_data='courses ' + courses[i] + ' ' + name)
            courses_kb.insert(courses_btn)

        await bot.edit_message_text(text('Выберите курс к которому будет принадлежать группа.'),
                                    user_id, message_id,
                                    reply_markup=courses_kb)
    await state.set_state(States.TUTOR_STATE[0])


@dp.callback_query_handler(Text(startswith='courses'), state=States.TUTOR_STATE)
async def process_course_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    # TODO: create group
    _, course, group = callback_query.data.split()
    await bot.edit_message_text(text('Группа', group, 'для курса', course, 'успешно создана.'),
                                user_id, message_id)


@dp.callback_query_handler(Text(startswith='edit'), state=States.CREATE_COURSE_STATE | States.CREATE_GROUP_STATE)
async def process_edit_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text('Введите название еще раз.', user_id, message_id)


@dp.callback_query_handler(Text(startswith='cancel'), state=States.CREATE_COURSE_STATE | States.CREATE_GROUP_STATE)
async def process_cancel_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    state = dp.current_state(user=user_id)
    await state.set_state(States.TUTOR_STATE[0])
    await bot.edit_message_text('Отменено.', user_id, message_id)

