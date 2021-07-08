import gspread as gspread
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, executor, types

from db.models import Groups
from loader import dp, bot, db
from utils import States
from aiogram.dispatcher.filters import Text
from KeyGen import KeyGen
from config import GROUP
from aiogram.dispatcher import FSMContext
from config import credentials, google_url


gc = gspread.service_account_from_dict(credentials)
sh = gc.open_by_url(google_url)
worksheet = sh.sheet1
list_of_lists = worksheet.get_all_values()


def next_day(day):
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    for i in range(len(days)):
        if days[i] == day:
            return days[i + 1]


def day_schedule(group_list, day):
    sch = []
    for j in range(len(group_list)):
        group = group_list[j]
        print(list_of_lists)
        if day == 'Воскресенье':
            ind_next_day = len(list_of_lists)

        ind = list_of_lists[0].index(group)

        for i in range(len(list_of_lists)):
            if list_of_lists[i][0] == day:
                ind_day = i
            if day != 'Воскресенье':
                if list_of_lists[i][0] == next_day(day):
                    ind_next_day = i

        for i in range(ind_day, ind_next_day):
            if list_of_lists[i][ind] != '':
                sch.append((list_of_lists[i][0], list_of_lists[i][ind]))

    return sch


# create week day menu
# Schedule button
@dp.message_handler(state=States.STUDENT_STATE, text='Расписание')
async def process_schedule_btn(message: types.Message):
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    days_buttons = InlineKeyboardMarkup()
    for i in range(len(days)):
        day_btn = InlineKeyboardButton(text=days[i], callback_data='day ' + days[i])
        days_buttons.insert(day_btn)

    await message.answer(text="Выберите день недели", reply_markup=days_buttons)


@dp.callback_query_handler(Text(startswith='day '), state=States.STUDENT_STATE)
async def process_one_course_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    group_names = db.get_group(student_UID=user_id)
    list_of_groups = []
    if type(group_names) is not Groups:
        for i in range(len(group_names)):
            list_of_groups.append(group_names[i].name + '-' + db.get_group(student_UID=user_id)[i].group_key)
    else:
        list_of_groups.append(group_names.name + '-' + db.get_group(student_UID=user_id).group_key)

    print(list_of_groups)
    day = callback_query.data.split(' ')[1]
    schedule = (day_schedule(list_of_groups, day))
    sch = ''
    for i in range(len(schedule)):
        sch += str(schedule[i][0]) + " " + str(schedule[i][1]) + "\n"
    if sch == '':
        sch = 'Пусто'
    await bot.edit_message_text(day + '\n' + sch, user_id, message_id)
