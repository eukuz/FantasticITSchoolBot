from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import dp, bot, db
from utils import States
from aiogram.dispatcher.filters import Text
from KeyGen import KeyGen


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
        key_course = KeyGen.generateNKeysCourses(1).pop()
        course = db.get_course(course_key=key_course[3:])
        db.set_course(course, name=name)
        await bot.edit_message_text(text('Курс', name, 'успешно создан.\nКлюч:', code(key_course)),
                                    user_id, message_id,
                                    parse_mode=ParseMode.MARKDOWN)
    else:
        courses = db.get_course()
        if type(courses) is not list:
            courses = [courses]
        courses_kb = InlineKeyboardMarkup()
        for i in range(len(courses)):
            courses_btn = InlineKeyboardButton(courses[i].name, callback_data='courses@' + courses[i].course_key + '@' + name)
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
    _, course, group_name = callback_query.data.split('@')
    key_group = KeyGen.generateNKeysGroups(1).pop()
    course_name = db.get_course(course_key=course).name
    group = db.get_group(group_key=key_group[3:])
    db.set_group(group, name=group_name)
    await bot.edit_message_text(text('Группа', group_name, 'для курса', course_name, 'успешно создана.\nКлюч:', code(key_group)),
                                user_id, message_id,
                                parse_mode=ParseMode.MARKDOWN)


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

