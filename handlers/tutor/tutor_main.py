from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types
from loader import dp, bot
from utils import States
from aiogram.dispatcher.filters import Text

generate_keys_btn = KeyboardButton('Сгенерировать ключи')
create_btn = KeyboardButton('Создать')
publish_post_btn = KeyboardButton('Опубликовать пост')
update_schedule_btn = KeyboardButton('Обновить расписание')
exit_btn = KeyboardButton('Выйти')

tutor_main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(generate_keys_btn,
                                                              create_btn,
                                                              publish_post_btn,
                                                              update_schedule_btn,
                                                              exit_btn)


@dp.message_handler(state=States.TUTOR_STATE, text='Обновить расписание')
async def process_update_schedule_btn(msg: types.Message):
    # TODO: Update schedule
    await msg.answer('Расписание успешно обновлено.')