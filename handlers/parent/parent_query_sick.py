from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, db, bot
from handlers.student.student_schedule import get_student_schedule
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from aiogram import types
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from .parent_main import sure_kb, child_menu, send_request_to_group, get_student_name_by_id, get_parent_name_by_id
from config import GROUP


@dp.callback_query_handler(state=States.PARENT_STATE, text='sick')
async def process_sick_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(States.PARENT_SICK_STATE[0])
    await state.update_data(child='')
    await child_menu(callback_query.from_user.id, callback_query.message.message_id,
                     display_text='Выберите ребёнка который заболел',
                     mode='edit')


@dp.callback_query_handler(Text(startswith='student'),
                           state=States.PARENT_SICK_STATE)
async def process_question_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    student_id = callback_query.data.split('|')[1]  # получаем id студента
    await state.update_data(child=student_id)
    student_name = await get_student_name_by_id(student_id)
    await bot.send_message(callback_query.from_user.id, 'Прикрепите подтверждающий документ для ' + str(student_name))


@dp.message_handler(state=States.PARENT_SICK_STATE, content_types=['photo', 'document', 'text'])
async def process_post_message(msg: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data['child']:  # Если не указали ребёнка, бот не отреагирует на сообщение
        await msg.reply(text('Вы уверены что хотите отправить эту справку?'), reply_markup=sure_kb)


@dp.callback_query_handler(state=States.PARENT_SICK_STATE, text='yes')
async def process_yes_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(text('Ваша справка отправлена организаторам, ожидайте ответа в этом боте'),
                                callback_query.from_user.id, callback_query.message.message_id)

    chat_id = callback_query.from_user.id
    message_id = callback_query.message.reply_to_message.message_id

    user_data = await state.get_data()
    child_id = user_data['child']
    parent_id = callback_query.from_user.id

    await send_sick_request(parent_id, child_id, message_id)

    await state.finish()
    await state.set_state(States.PARENT_STATE[0])


async def send_sick_request(parent_id, child_id, message_id):
    parent_name = await get_parent_name_by_id(parent_id)
    child_name = await get_student_name_by_id(child_id)

    # Добавляем ссылку на аккаунт если настройки приватности пользователя позволяют.
    parent_name_link = f'[{parent_name}](tg://user?id={str(parent_id)})'
    child_name_link = f'[{child_name}](tg://user?id={str(child_id)})'

    caption = f'Справка от родителя {parent_name_link}. Заболел ребёнок {child_name_link}.'
    await send_request_to_group(parent_id, message_id, GROUP, caption)

