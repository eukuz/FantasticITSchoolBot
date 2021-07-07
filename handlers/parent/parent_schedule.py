from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp, bot
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode
from aiogram import types
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from handlers.student.student_schedule import get_student_schedule
from .parent_main import child_menu, group_menu, get_student_name_by_id


@dp.message_handler(state=States.PARENT_STATE, text='Расписание')
async def process_schedule_btn(msg: types.Message, state: FSMContext):
    await state.update_data(child='', group='')
    await child_menu(msg.from_user.id, msg.message_id,
                     display_text='Выберите ребёнка',
                     mode='answer')


# Когда выбрали ребёнка
@dp.callback_query_handler(Text(startswith='student'),
                           state=States.PARENT_STATE)
async def process_question_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    student_id = callback_query.data.split('|')[1]  # получаем id студента
    await state.update_data(child=student_id)
    student_name = await get_student_name_by_id(student_id)
    await group_menu(parent_id=callback_query.from_user.id,
                     message_id=callback_query.message.message_id,
                     child_id=student_id,
                     display_text=f'Выберите группу для {student_name}',
                     mode='edit')


# Когда выбрали группу
@dp.callback_query_handler(Text(startswith='group'),
                           state=States.PARENT_STATE)
async def process_question_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Тут будет расписание")
