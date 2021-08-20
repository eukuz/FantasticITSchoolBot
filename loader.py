from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, executor, types
import config
from db.app_db import Database

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database()
dp.middleware.setup(LoggingMiddleware())


async def publish_msg(students, msg: types.Message):
    for student in students:
        await msg.send_copy(student.UID)