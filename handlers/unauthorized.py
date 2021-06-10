from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from utils import States
from loader import dp
from .buttons import parent_in_system_kb

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)  # take current state of user
    await state.set_state(States.UNAUTHORIZED_STATE[0])  # user is unauthorized in the very beginning
    await message.answer("Привет, я бот введи пожалуйста ключ :)")  # write welcome message to user


# Authorization works only in UNAUTHORIZED state
@dp.message_handler(state=States.UNAUTHORIZED_STATE)
async def authorization(msg: types.Message):
    text_ = msg.text                                  # take user's message
    state = dp.current_state(user=msg.from_user.id)  # take current state
    # check user's authorization code (TO DO)
    if text_ == 'studentCode':
        await state.set_state(States.STUDENT_STATE[0])  # change user's state to STUDENT
        # create parent code
        parentCode = 'parentCode'
        await msg.answer(text("Вы успешно авторизовались как ученик. Код для авторизации родителя: ",
                              code(parentCode), ".", sep=""),
                         parse_mode=ParseMode.MARKDOWN,
                         reply_markup=parent_in_system_kb)
    elif text_ == 'parentCode':
        await state.set_state(States.PARENT_STATE[0])   # change user's state to PARENT
        # TO DO: Find children of the parent
        await msg.answer("Вы успешно авторизовались как родитель. Вас добавили дети: ")
    else:
        await msg.answer("Такого ключа не существует, пожалуйста, попробуйте еще раз.")  # code is not correct


# @dp.message_handler(state='*')
# async def echo_message(msg: types.Message):
#     state = dp.current_state(user=msg.from_user.id)
#     print(await state.get_state())
