from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, executor, types
from utils import States
from loader import dp


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.UNAUTHORIZED_STATE[0])
    await message.answer("Привет, я бот введи пожалуйста ключ :)")


@dp.message_handler(state=States.UNAUTHORIZED_STATE)
async def authorization(msg: types.Message):
    text = msg.text
    state = dp.current_state(user=msg.from_user.id)
    if text == 'studentCode':
        await state.set_state(States.STUDENT_STATE[0])
        await msg.answer("Вы успешно авторизовались как ученик.")
    else:
        await msg.answer("Такого ключа не существует, пожалуйста, попробуйте еще раз.")


@dp.message_handler(state='*')
async def echo_message(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    print(await state.get_state())
