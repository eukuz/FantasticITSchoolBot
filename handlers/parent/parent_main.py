from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp, bot, db
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from aiogram import types
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from handlers.student.student_courses import course_menu

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
        return db.get_group(id=group_id).name
    except AttributeError:
        return f"<group name with id {group_id} not found>"


# Mеню выбора ребёнка
async def child_menu(parent_id, message_id, display_text, mode):

    children_list = db.get_student(parent_id=db.get_parent(UID=parent_id))
    children_buttons = InlineKeyboardMarkup()
    if type(children_list) is not list:
        children_list = [children_list]

    for i in range(len(children_list)):
        child_btn = InlineKeyboardButton(text=children_list[i].full_name,
                                         callback_data='student ' + children_list[i].UID)
        children_buttons.insert(child_btn)
    children_buttons.insert(InlineKeyboardButton("Отмена", callback_data='cancel'))

    if mode == 'answer':
        await bot.send_message(parent_id, display_text, parse_mode=ParseMode.MARKDOWN, reply_markup=children_buttons)
    else:
        await bot.edit_message_text(display_text, parent_id, message_id)
        await bot.edit_message_reply_markup(parent_id, message_id, reply_markup=children_buttons)


# Mеню выбора группы для студента/ребёнка
async def group_menu(parent_id, child_id, message_id, display_text, mode):
    groups = db.get_group(student_UID=child_id)
    if type(groups) is not list:
        groups = [groups]
    groups_kb = InlineKeyboardMarkup()
    for i in range(len(groups)):
        groups_btn = InlineKeyboardButton(groups[i].name, callback_data='group ' + str(groups[i].id))
        groups_kb.insert(groups_btn)
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
