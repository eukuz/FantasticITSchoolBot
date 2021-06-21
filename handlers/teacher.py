from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from .unauthorized import dp
from .student_buttons import get_student_schedule
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import bot
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

teacher_courses_btn = KeyboardButton('Мои курсы')
teacher_add_course_btn = KeyboardButton('Добавить курс')
teacher_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(teacher_courses_btn,
                                                                teacher_add_course_btn)
teacher_cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))

yes_btn = InlineKeyboardButton('Да', callback_data='yes')
edit_btn = InlineKeyboardButton('Изменить', callback_data='edit')
cancel_btn = InlineKeyboardButton('Отмена', callback_data='cancel')
sure_kb = InlineKeyboardMarkup().add(yes_btn, edit_btn, cancel_btn)


async def check_course_exists(course_key: str):
    return course_key == "newCourse"


async def send_message_to_group(user_message_id):
    pass


async def send_hw_to_group(user_message_id):
    pass


@dp.message_handler(state=States.TEACHER_STATE, text='Добавить курс')
async def process_add_course_btn(msg: types.Message):
    await dp.current_state(user=msg.from_user.id).set_state(States.TEACHER_ADD_COURSE_STATE[0])
    await msg.answer('Введите пожалуйста ключ', reply_markup=teacher_cancel_kb)


@dp.message_handler(state=States.TEACHER_ADD_COURSE_STATE)
async def process_teacher_key(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    text_ = msg.text
    if text_ == 'Отмена':
        await state.set_state(States.TEACHER_STATE[0])
        await msg.answer('Отменено', reply_markup=teacher_main_kb)
    elif check_course_exists('newCourse'):
        await state.set_state(States.TEACHER_STATE[0])
        await msg.answer('Поздравляем вы успешно добавили себе курс ' + text_ + '.', reply_markup=teacher_main_kb)
    else:
        await msg.answer('Такого ключа не существует.')


# Генерация списка "курс + группа"
async def coursegroup_menu(user_id, message_id, mode):
    coursegroup = ['Python Group 1', 'Java Group 2', 'C++ Group 3']
    courses_kb = InlineKeyboardMarkup()
    for i in range(len(coursegroup)):
        courses_btn = InlineKeyboardButton(coursegroup[i], callback_data='coursegroup|' + coursegroup[i])
        courses_kb.insert(courses_btn)

    if mode == 'answer':
        await bot.send_message(user_id, 'Ваши курсы: ', parse_mode=ParseMode.MARKDOWN, reply_markup=courses_kb)
    else:
        await bot.edit_message_text('Ваши курсы: ', user_id, message_id)
        await bot.edit_message_reply_markup(user_id, message_id, reply_markup=courses_kb)


# Показать список "курс + группа" в первый раз при нажатии кнопки "Мои курсы"
@dp.message_handler(state=States.TEACHER_STATE, text='Мои курсы')
async def process_courses_btn(msg: types.Message):
    await coursegroup_menu(msg.from_user.id, msg.message_id, mode='answer')


# Показать список "курс + группа" снова, при нажатии кнопки "Назад" из меню выбранного элемента
@dp.callback_query_handler(state=States.TEACHER_STATE, text='Назад в список курсов')
async def process_back_course_btn(callback_query: types.CallbackQuery):
    await coursegroup_menu(callback_query.from_user.id, callback_query.message.message_id, mode='edit')


# Показать выбранный элемент из списка "курс + группа" и кнопки действий
@dp.callback_query_handler(Text(startswith='coursegroup'), state=States.TEACHER_STATE)
async def process_one_course_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    coursegroup = callback_query.data.split('|')[1]  # название выбранного элемента ("курс + группа")
    create_hw_btn = InlineKeyboardButton('Создать ДЗ', callback_data='create_hw|' + coursegroup)
    send_hw_btn = InlineKeyboardButton('Отправить в рассылку', callback_data='create_massmessage|' + coursegroup)
    back_btn = InlineKeyboardButton('Назад', callback_data='Назад в список курсов')
    actions_kb = InlineKeyboardMarkup()
    actions_kb.row(create_hw_btn, send_hw_btn)
    actions_kb.row(back_btn)

    await bot.edit_message_text('Вы выбрали ' + coursegroup, user_id, message_id, reply_markup=actions_kb)


@dp.callback_query_handler(Text(startswith='create_hw'), state=States.TEACHER_STATE)
async def process_publish_btn(callback_query: types.CallbackQuery, state: FSMContext):
    coursegroup = callback_query.data.split('|')[1]  # название выбранного элемента ("курс + группа")
    await state.finish()
    await state.set_state(States.TEACHER_CREATE_HW_1_STATE[0])
    await state.update_data(coursegroup=coursegroup)
    print(coursegroup)
    await bot.send_message(callback_query.from_user.id, 'Введите заголовок урока')

@dp.callback_query_handler(Text(startswith='create_massmessage'), state=States.TEACHER_STATE)
async def process_publish_btn(callback_query: types.CallbackQuery, state: FSMContext):
    coursegroup = callback_query.data.split('|')[1]  # название выбранного элемента ("курс + группа")
    await state.finish()
    await state.set_state(States.TEACHER_CREATE_MASS_MESSAGE_STATE[0])
    await state.update_data(coursegroup=coursegroup)
    await bot.send_message(callback_query.from_user.id, 'Введите сообщение для рассылки')


@dp.message_handler(state=States.TEACHER_CREATE_MASS_MESSAGE_STATE)
async def process_post_message(msg: types.Message, state: FSMContext):
    await state.update_data(text=msg.text)
    await msg.answer(text('Вы уверены что хотите отправить это сообщение?'), reply_markup=sure_kb)


@dp.message_handler(state=States.TEACHER_CREATE_HW_1_STATE)
async def process_post_message(msg: types.Message, state: FSMContext):
    await state.update_data(head=msg.text)
    await msg.answer(text('Вы уверены что хотите отправить этот заголовок?'), reply_markup=sure_kb)


@dp.message_handler(state=States.TEACHER_CREATE_HW_2_STATE)
async def process_post_message(msg: types.Message, state: FSMContext):
    await state.update_data(hw_text=msg.text)
    print(msg.text)
    await msg.answer(text('Вы уверены что хотите отправить это ДЗ?'), reply_markup=sure_kb)


# Запоминаем заголовок для ДЗ
@dp.callback_query_handler(state=States.TEACHER_CREATE_HW_1_STATE, text='yes')
async def process_post_message(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    coursegroup = state_data['coursegroup']
    head = state_data['head']
    await state.finish()
    # Пересохраняем данные в новый state
    await state.set_state(States.TEACHER_CREATE_HW_2_STATE[0])
    await state.update_data(coursegroup=coursegroup)
    await state.update_data(head=head)

    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text(text('Отправьте файл с ДЗ, можно добавить описание в сообщении'),
                                user_id, message_id)


# Запоминаем и отправляем ДЗ
@dp.callback_query_handler(state=States.TEACHER_CREATE_HW_2_STATE, text='yes')
async def process_yes_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    await bot.edit_message_text(text('ДЗ с заголовком "', user_data['head'], '" будет отправлено для ',
                                     user_data['coursegroup'], '.', sep=''),
                                callback_query.from_user.id, callback_query.message.message_id)
    #await send_hw_to_group(callback_query.from_user.id, user_data['coursegroup'], user_data['head'], user_data['hw_text'])
    await state.finish()
    await state.set_state(States.TEACHER_STATE[0])


# Запоминаем и отправляем массовое сообщение
@dp.callback_query_handler(state=States.TEACHER_CREATE_MASS_MESSAGE_STATE, text='yes')
async def process_yes_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    await bot.edit_message_text(text('Сообщение: "', user_data['text'], '" будет отправлено для ',
                                     user_data['coursegroup'], '.', sep=''),
                                callback_query.from_user.id, callback_query.message.message_id)
    #await send_hw_to_group(callback_query.from_user.id, user_data['coursegroup'], user_data['text'])
    await state.finish()
    await state.set_state(States.TEACHER_STATE[0])


@dp.callback_query_handler(state=States.TEACHER_CREATE_MASS_MESSAGE_STATE | States.TEACHER_CREATE_HW_1_STATE
                                 | States.TEACHER_CREATE_HW_2_STATE, text='edit')
async def process_edit_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text('Введите сообщение еще раз.', user_id, message_id)


@dp.callback_query_handler(state=States.TEACHER_CREATE_MASS_MESSAGE_STATE | States.TEACHER_CREATE_HW_1_STATE
                                 | States.TEACHER_CREATE_HW_2_STATE, text='cancel')
async def process_cancel_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text('Отменено.', user_id, message_id)
    await state.finish()
    await state.set_state(States.TEACHER_STATE[0])
