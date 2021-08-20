from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, executor, types
from loader import bot

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)