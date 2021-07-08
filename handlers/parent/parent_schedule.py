import gspread
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from db.models import Groups
from loader import dp, bot, db
from aiogram.utils.markdown import text, bold
from aiogram.types import ParseMode, callback_query, message
from aiogram import types
from utils import States
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from .parent_main import child_menu, group_menu, get_student_name_by_id

from config import credentials, google_url

gc = gspread.service_account_from_dict(credentials)
sh = gc.open_by_url(google_url)
worksheet = sh.sheet1
list_of_lists = worksheet.get_all_values()


def all_schedule(group_list):
    sch = []
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    for j in range(len(group_list)):
        group = group_list[j]
        ind = list_of_lists[0].index(group)

        for i in range(len(list_of_lists)):
            if list_of_lists[i][ind] != '':
                sch.append(list_of_lists[i][0] + ' ' + list_of_lists[i][ind])
            if list_of_lists[i][0] in days:
                sch.append(list_of_lists[i][0])

    return sch


@dp.message_handler(state=States.PARENT_STATE, text='Расписание')
async def process_schedule_btn(message: types.Message):
    await child_menu(message.from_user.id,message.message_id,"Выберите ребёнка","answer")


# Когда выбрали ребёнка
@dp.callback_query_handler(Text(startswith='student '), state=States.PARENT_STATE)
async def process_question_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    student_id = callback_query.data.split(' ')[1]
    group_names = db.get_group(student_UID=student_id)
    list_of_groups = []
    if type(group_names) is not Groups:
        for i in range(len(group_names)):
            list_of_groups.append(group_names[i].name + '-' + db.get_group(student_UID=student_id)[i].group_key)
    else:
        list_of_groups.append(group_names.name + '-' + db.get_group(student_UID=student_id).group_key)
    print(group_names)
    schedule = all_schedule(list_of_groups)
    sch = ''
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    for i in range(1, len(schedule) - 1):
        if ((schedule[i] not in days) or (schedule[i + 1] not in days)):
            sch += str(schedule[i]) + "\n"
    if sch == '':
        sch = 'Пусто'
    await bot.edit_message_text(sch, user_id, message_id)
