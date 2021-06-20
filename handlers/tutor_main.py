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

generate_keys_btn = KeyboardButton('Сгенерировать ключи')
create_btn = KeyboardButton('Создать')
publish_post_btn = KeyboardButton('Опубликовать пост')
exit_btn = KeyboardButton('Выйти')

tutor_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(generate_keys_btn,
                                                              create_btn,
                                                              publish_post_btn,
                                                              exit_btn)