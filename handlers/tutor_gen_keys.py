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


@dp.message_handler(state=States.TUTOR_STATE, text='Сгенерировать ключи')
async def process_generate_keys_btn(msg: types.Message):
    students_btn = InlineKeyboardButton('Студентам', callback_data='gen students')
    tutors_btn = InlineKeyboardButton('Кураторам', callback_data='gen tutors')
    teachers_btn = InlineKeyboardButton('Учителям', callback_data='gen teachers')
    gen_kb = InlineKeyboardMarkup().insert(students_btn).insert(tutors_btn).insert(teachers_btn)
    await msg.answer(text='Для кого вы хотите сгенерировать ключи?', reply_markup=gen_kb)


@dp.callback_query_handler(Text(startswith='gen '), state=States.TUTOR_STATE)
async def process_number_gen_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    await bot.send_message(user_id, text='Сколько штук? (Введите число)')
    state = dp.current_state(user=user_id)
    if callback_data.find('students') != -1:
        await state.set_state(States.GENKEYS_STUDENT_STATE[0])
    elif callback_data.find('tutors') != -1:
        await state.set_state(States.GENKEYS_TUTOR_STATE[0])
    else:
        await state.set_state(States.GENKEYS_TEACHER_STATE[0])


@dp.message_handler(state=States.GENKEYS_TEACHER_STATE | States.GENKEYS_STUDENT_STATE | States.GENKEYS_TUTOR_STATE)
async def process_number_keys(msg: types.Message):
    if msg.text.isnumeric():
        # TODO: generate keys
        n = int(msg.text)
        state = dp.current_state(user=msg.from_user.id)
        s = await state.get_state()
        if s == States.GENKEYS_STUDENT_STATE[0]:
            keys = ['studentCode1', 'studentCode2', 'studentCode3']
        elif s == States.GENKEYS_TUTOR_STATE[0]:
            keys = ['tutorCode1', 'tutorCode2', 'tutorCode3']
        else:
            keys = ['teacherCode1', 'teacherCode2', 'teacherCode3']
        await msg.answer(text(*list(map(code, keys))[:n], sep='\n'), parse_mode=ParseMode.MARKDOWN)
        await state.set_state(States.TUTOR_STATE[0])
    else:
        await msg.answer('Кажется то что вы ввели не является числом. Пожалуйста попробуйте еще раз.')