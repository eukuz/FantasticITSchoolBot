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
import gspread


credentials = {
  "type": "service_account",
  "project_id": "schedule-318913",
  "private_key_id": "bac2dab3c6c52577808549e47538fc1a1729c540",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDBRW/rglhIbsCe\nqXEwpu9KF8SK7Sjld8tf5n/Cg2Q2gpxwKVTJMqYPF0cThV/akpCCE97adXO9XZn6\nU0eORdZ2IiIVEmJExK2Z1+6Tr5dxISmYiN2/k1LmwlmUytNubEh9n1ycxa7Gl1SD\nomvF10LOnm34XoCpB3308/Zw2ZSOjK1iFqQ2NL8zT9NRQC2xGSt38mGy2uhy+hbU\n8gRjvARAor3u6GL4nxtWlif/KcNrz3BEWAnm08nnfEDVG7cUiZBT0EwKcAr+OHxw\n+Gzo9oK3Ala0hIy8ba+eLSulUf1JzvR+VLFVxmbFk+lawKLdXkhOW/dAhUBsEsHT\nucgqwbCJAgMBAAECggEADKB2ZRg5SlTUssj2gyuKMKNdjNyyXPjhnvIBNiUSvq5J\nKC7FwktT0WKU8IU4iPV7CXSLjRGQA+GB9iUguf59ZMRqyPOlhev6POCATsJxuMtm\nMKKofM6pjjfzqvvr/6faveepIPjtUpN/ywXT2AjDQu/TgXQzIFfuoQ/wnC4q6CZ9\ndDGMxpzTImbCpu7NeIurm3lG3MZ2oYhI50/YI4VA8O+An6e9vu00ngb2RJFG79uJ\nVTNjVhAIXqV5i2TiQg7GnrtnYU4egMMWn0q2O+2O9w64XKFqG9Zd2RJFBoqIrPua\nJ6vEfw8mOnhDChSLTSnfHArtCTgQ0J89MS5BzdTZPQKBgQD5vy3h0JQtnwaHFZ/a\nuX7UmXG3nszIJlKHJxAYTkMvZM4oGaARrXUFvfNixW9md6798QDL168Y7bD6A2zC\nrzYtP7aFlcem3eaoj9H0RBS3p+anVSU1pm+7ojzA4TbMbDd8B0YVXUiO4z4JsYXS\nhBKaJ77O+mG1OLPv2lCuNJSfYwKBgQDGHEMp0tjix7tVa0V/yeo/zTXY5AEq17Xx\nzGkKRp2dTXv2mny/yPwnOGY+2J3ffJQg4ztO8+WgiGbrAnxz/aDVhpOo9PTu/DYK\n0tITj6ERMgtRQyo+FCZjyOlWDNtcvYcZj/RFlbM9Au5yXWGibYOgkFH0/E/yE+XW\nMbnCPqRiIwKBgCpxxVh1XFmMh0157Vr834M+OMdeI6t4Z9o0V1XqJxzs4uSJxlx6\nwEKjj7OfnlkpygG6bco287km3EcBQgCsSmbSRzDYzb+cQtEu8B21XFgCHv8dR1+g\n06ht4ClfnTKMybk4ez6yRdyS3j5Df1zRuV+dlZ4Ti3uDEYGX9tJEeWXFAoGBALfH\naBbYXhKiroojJSnSqdfeCmHVwa94xHQ26Ap8T6KpSqIN1kQjsqa/jzolwO6dptyL\nb21inFY7sx24BLOlSRpL6ZcHBmDc31VTFUbIKubEwfL0l69XCfXvX2ZQLv7tYvK3\ntCcJJGko2wKE1hnT9hNxTlYx6gfrpX76ShSEAAJ5AoGAKRUiYyzLKgF8LHLqxJZQ\n3SULl402iiuayYD/2rOKBwE97awP3fl+tXw0YAy/5V6r5F8hhfdqQVtpkCygYwL7\nrmG30wFpZUnXUWT8HOR8lT9E+j5LtLpM4R1b4bQeMXVfvFfiVF8/NPITFeiST8em\ndDo6lu/mA7VMuuafvYyYY+g=\n-----END PRIVATE KEY-----\n",
  "client_email": "schedule-account@schedule-318913.iam.gserviceaccount.com",
  "client_id": "103150586629084413264",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/schedule-account%40schedule-318913.iam.gserviceaccount.com"
}

gc = gspread.service_account_from_dict(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1yWwQ4HcnUKgiWq5WOXmHXdNhD2r0pZe3ddWyhrrzVsE/edit?usp=sharing')
worksheet = sh.sheet1

list_of_lists = worksheet.get_all_values()


def add_new_column(value):
    cell_2 = len(list_of_lists[0]) + 1
    worksheet.update_cell(1, cell_2, value)


@dp.message_handler(state=States.TUTOR_STATE, text='Создать')
async def process_create_btn(msg: types.Message):
    course_btn = InlineKeyboardButton('Курс', callback_data='create course')
    group_btn = InlineKeyboardButton('Группа', callback_data='create group')
    back_btn = InlineKeyboardButton('Назад', callback_data='back')
    create_kb = InlineKeyboardMarkup().insert(course_btn).insert(group_btn).insert(back_btn)
    await msg.answer(text='Что будем создавать?', reply_markup=create_kb)


@dp.callback_query_handler(Text(startswith='create'), state=States.TUTOR_STATE | States.CREATE_GROUP_STATE | States.CREATE_COURSE_STATE)
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


@dp.callback_query_handler(state=States.TUTOR_STATE | States.CREATE_GROUP_STATE | States.CREATE_COURSE_STATE, text='back')
async def process_back_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(States.TUTOR_STATE[0])
    # print(await state.get_state())


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
    add_new_column(group_name + '-' + key_group[3:])
    db.set_group(group, name=group_name, course=db.get_course(course_key=course))
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

