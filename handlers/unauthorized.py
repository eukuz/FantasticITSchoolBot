from aiogram.types.chat import ChatType
from handlers.student.student_register_parent import parent_in_system_kb
from handlers.student.student_main import student_main_kb
from .parent import parent_main_kb
from handlers.tutor.tutor_main import tutor_main_kb
from handlers.tutor.tutor_publish import *
from .teacher import teacher_main_kb
from loader import dp, bot
from .student import *
from .tutor import *


@dp.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message):
    if ChatType.is_group_or_super_group(message.chat):
        return
    state = dp.current_state(user=message.from_user.id)  # take current state of user
    await state.set_state(States.UNAUTHORIZED_STATE[0])  # user is unauthorized in the very beginning
    await message.answer('Привет, я бот введите пожалуйста ключ :)',
                         reply_markup=ReplyKeyboardRemove())       # write welcome message to user


# Authorization works only in UNAUTHORIZED state
@dp.message_handler(state=States.UNAUTHORIZED_STATE)
async def authorization(msg: types.Message):
    text_ = msg.text                                  # take user's message
    state = dp.current_state(user=msg.from_user.id)  # take current state
    # TODO: check user's authorization code
    check = True
    if not check:
        await msg.answer('Такого ключа не существует, пожалуйста, попробуйте еще раз.')  # code is not correct
    elif text_[:3] == 'STU':
        await state.set_state(States.STUDENT_STATE[0])  # change user's state to STUDENT
        # add main buttons for student
        await msg.answer('Вы успешно авторизовались как ученик.',
                         reply_markup=student_main_kb)

        await msg.answer(text('Пожалуйста, зарегестрируйте родителя.'),
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=parent_in_system_kb)
    elif text_[:3] == 'PAR':
        await state.set_state(States.PARENT_STATE[0])   # change user's state to PARENT
        # TODO: find children of the parent
        await msg.answer('Вы успешно авторизовались как родитель. Вас добавили дети: ',
                         reply_markup=parent_main_kb)
    elif text_[:3] == 'CUR':
        await state.set_state(States.TUTOR_STATE[0])  # change user's state to TUTOR
        await msg.answer('Вы успешно авторизовались как куратор.',
                         reply_markup=tutor_main_kb)
    elif text_[:3] == 'TEA':
        await state.set_state(States.TEACHER_STATE[0])  # change user's state to TEACHER
        await msg.answer('Вы успешно авторизовались как учитель.',
                         reply_markup=teacher_main_kb)
    else:
        # TODO: some error message
        await msg.answer('Ошибка. Пожалуйста обратитесь к администрации.')


# Exit button
@dp.message_handler(state=States.STUDENT_STATE | States.PARENT_STATE |
                          States.TUTOR_STATE | States.TEACHER_STATE, text='Выйти')
async def process_exit_btn(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)  # take current state
    await state.set_state(States.UNAUTHORIZED_STATE[0])  # unauthorize user
    await msg.answer('Вы успешно вышли из системы.',
                     parse_mode=ParseMode.MARKDOWN,
                     reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state='*')
async def echo_message(msg: types.Message):
    if ChatType.is_group_or_super_group(msg.chat):
        # if msg.is_forward():
        #     print('Hello')
        try:
            source_message = msg.reply_to_message
            user_id = source_message.text.split('.')[0]
            await msg.answer('Ваше сообщение успешно отправлено.')
            await bot.send_message(user_id, text=msg.text)
        except:
            pass
    else:
        await msg.answer('Я вас не понял. Попробуйте другую команду.')


async def publish_msg(students, msg: types.Message):
    for id in students:
        await bot.send_message(id, text=msg.text)