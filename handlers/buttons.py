from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

parent_in_system_btn = InlineKeyboardButton('Мой родитель уже в системе.', callback_data='parent in system')
parent_in_system_kb = InlineKeyboardMarkup().add(parent_in_system_btn)