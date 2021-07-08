from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp, bot
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from aiogram import types
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from config import GROUP
from .parent_main import sure_kb, child_menu, group_menu, send_request_to_group, \
    get_student_name_by_id, get_parent_name_by_id, get_group_name_by_id


@dp.callback_query_handler(state=States.PARENT_STATE, text='feedback')
async def process_sick_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(States.PARENT_FEEDBACK_STATE[0])
    await state.update_data(child='', group='')
    await child_menu(callback_query.from_user.id, callback_query.message.message_id,
                     display_text='Выберите ребёнка для которого нужен фидбек',
                     mode='edit')


# Когда выбрали ребёнка
@dp.callback_query_handler(Text(startswith='student'),
                           state=States.PARENT_FEEDBACK_STATE)
async def process_question_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    student_id = callback_query.data.split(' ')[1]  # получаем id студента
    await state.update_data(child=student_id)
    student_name = await get_student_name_by_id(student_id)
    await group_menu(parent_id=callback_query.from_user.id,
                     message_id=callback_query.message.message_id,
                     child_id=student_id,
                     display_text=f'Выберите группу для {student_name}',
                     mode='edit')


# Когда выбрали группу
@dp.callback_query_handler(Text(startswith='group'),
                           state=States.PARENT_FEEDBACK_STATE)
async def process_question_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_data = await state.get_data()
    if user_data['child']:  # Если не указали ребёнка, бот не отреагирует на сообщение
        group_id = callback_query.data.split(' ')[1]  # получаем id группы
        await state.update_data(group=group_id)
        group_name = await get_group_name_by_id(group_id)
        student_name = await get_student_name_by_id(user_data['child'])
        await bot.edit_message_text(
            text=f"Вы хотите получить фидбек по студенту {student_name} по курсу/группе '{group_name}' ?",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=InlineKeyboardMarkup()
            .add(
                InlineKeyboardButton('Да', callback_data='yes'),
                InlineKeyboardButton('Отмена', callback_data='cancel')
            )
            )


@dp.callback_query_handler(state=States.PARENT_FEEDBACK_STATE, text='yes')
async def process_yes_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(text('Ваша заявка на фидбек отправлена организаторам, ожидайте ответа в этом боте'),
                                callback_query.from_user.id, callback_query.message.message_id)
    message_id = callback_query.message.message_id
    user_data = await state.get_data()
    child_id = user_data['child']
    group_id = user_data['group']
    parent_id = callback_query.from_user.id

    await send_feedback_request(parent_id, child_id, group_id, message_id)

    await state.finish()
    await state.set_state(States.PARENT_STATE[0])


async def send_feedback_request(parent_id, child_id, group_id, message_id):
    parent_name = await get_parent_name_by_id(parent_id)
    child_name = await get_student_name_by_id(child_id)
    group_name = await get_group_name_by_id(group_id)

    # Добавляем ссылку на аккаунт если настройки приватности пользователя позволяют.
    # TODO вынести в отделюную функцию создание markdown-ссылки на аккаунт
    parent_name_link = f'[{parent_name}](tg://user?id={str(parent_id)})'
    child_name_link = f'[{child_name}](tg://user?id={str(child_id)})'

    caption = f'Родитель {parent_name_link} запрашивает фидбек для ребёнка {child_name_link} по курсу {group_name}.'
    await send_request_to_group(parent_id, message_id, GROUP, caption, is_only_caption=True)
