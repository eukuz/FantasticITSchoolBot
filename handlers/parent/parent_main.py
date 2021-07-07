from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp, bot, db
from handlers.student.student_schedule import get_student_schedule
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from aiogram import types
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

# Главная клавиатура родителя
parent_schedule_btn = KeyboardButton('Расписание')
parent_query_btn = KeyboardButton('Запрос')
parent_exit_btn = KeyboardButton('Выйти')
parent_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(parent_schedule_btn,
                                                               parent_query_btn,
                                                               parent_exit_btn)

query_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Задать вопрос', callback_data='question'),
                                      InlineKeyboardButton('Сообщить о болезни', callback_data='sick'),
                                      InlineKeyboardButton('Получить фидбек', callback_data='feedback'))


@dp.message_handler(state=States.PARENT_STATE, text='Запрос')
async def process_query_btn(msg: types.Message):
    await msg.answer('Выберите действие: ', reply_markup=query_kb)


# Кнопки для подтверждения пользовательского ввода
yes_btn = InlineKeyboardButton('Да', callback_data='yes')
edit_btn = InlineKeyboardButton('Изменить', callback_data='edit')
cancel_btn = InlineKeyboardButton('Отмена', callback_data='cancel')
sure_kb = InlineKeyboardMarkup().add(yes_btn, edit_btn, cancel_btn)


async def send_request_to_group(sender_id, sender_message_id, group_id, caption, is_only_caption=False):
    full_caption = f"`{sender_id}`\n{caption}"
    if is_only_caption:
        await bot.send_message(chat_id=group_id,
                               text=full_caption,
                               parse_mode=ParseMode.MARKDOWN)
        return

    # Копируем сообщение пользователя в группу
    user_msg = await bot.copy_message(chat_id=group_id,
                                      from_chat_id=sender_id,
                                      message_id=sender_message_id)

    # Отвечаем на только что отправленное в группу сообщение
    await bot.send_message(chat_id=group_id,
                           reply_to_message_id=user_msg.message_id,
                           text=full_caption,
                           parse_mode=ParseMode.MARKDOWN)


async def get_childs(parent_id):
    # TODO get children data
    # формат {student_id : student_name}
    return {1: 'Ребенок 1',
            2: 'Ребёнок 2'}


async def get_student_groups(student_id):
    # TODO get student groups data
    # формат {group_id : group_name}
    return {1: 'Курс/Группа 1',
            2: 'Курс/Группа 2'}


async def get_parent_name_by_id(parent_id):
    try:
        return db.get_parent(UID=parent_id).full_name
    except AttributeError:
        return f"<parent name with id {parent_id} not found>"


async def get_student_name_by_id(student_id):
    try:
        return db.get_student(UID=student_id).full_name
    except AttributeError:
        return f"<student name with id {student_id} not found>"


async def get_group_name_by_id(group_id):
    try:
        return db.get_group(UID=group_id).course
    except AttributeError:
        return f"<group name with id {group_id} not found>"


# Mеню выбора ребёнка
async def child_menu(parent_id, message_id, display_text, mode):
    students_dict = await get_childs(parent_id)
    students_kb = InlineKeyboardMarkup()
    for student_id, student_name in students_dict.items():
        student_btn = InlineKeyboardButton(student_name, callback_data='student|' + str(student_id))
        students_kb.insert(student_btn)
    students_kb.insert(InlineKeyboardButton("Отмена", callback_data='cancel'))
    if mode == 'answer':
        await bot.send_message(parent_id, display_text, parse_mode=ParseMode.MARKDOWN, reply_markup=students_kb)
    else:
        await bot.edit_message_text(display_text, parent_id, message_id)
        await bot.edit_message_reply_markup(parent_id, message_id, reply_markup=students_kb)


# Mеню выбора группы
async def group_menu(parent_id, child_id, message_id, display_text, mode):
    groups_dict = await get_student_groups(child_id)
    groups_kb = InlineKeyboardMarkup()
    for group_id, group_name in groups_dict.items():
        student_btn = InlineKeyboardButton(group_name, callback_data='group|' + str(group_id))
        groups_kb.insert(student_btn)
    groups_kb.insert(InlineKeyboardButton("Отмена", callback_data='cancel'))
    if mode == 'answer':
        await bot.send_message(parent_id, display_text, parse_mode=ParseMode.MARKDOWN, reply_markup=groups_kb)
    else:
        await bot.edit_message_text(display_text, parent_id, message_id)
        await bot.edit_message_reply_markup(parent_id, message_id, reply_markup=groups_kb)


# Возвращение пользователя в PARENT_STATE при отмене ввода
@dp.callback_query_handler(state=States.PARENT_QUESTION_STATE
                                 | States.PARENT_SICK_STATE
                                 | States.PARENT_FEEDBACK_STATE
                                 | States.PARENT_STATE,
                           text='cancel')
async def process_cancel_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text('Отменено.', user_id, message_id)
    await state.finish()
    await state.set_state(States.PARENT_STATE[0])


# Повтор ввода; состояние (state) не меняется
@dp.callback_query_handler(state=States.PARENT_QUESTION_STATE
                                 | States.PARENT_SICK_STATE
                                 | States.PARENT_FEEDBACK_STATE,
                           text='edit')
async def process_edit_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    await bot.edit_message_text('Введите сообщение еще раз.', user_id, message_id)
