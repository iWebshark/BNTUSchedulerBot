import datetime
import telebot
import bntu_cache

weekdays = {0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 4: 'Пт', 5: 'Сб', 6: 'Вс'}


def reg_or_update_user(message: telebot.types.Message):
    user = bntu_cache.get_user(message.from_user.id)
    username = get_user_name(message.from_user)
    if user is None:
        bntu_cache.reg_user(message.chat.id, message.from_user.id, username)
    elif user.chat_id != str(message.chat.id) or user.username != username:
        bntu_cache.update_user(message.chat.id, message.from_user.id, username)


def get_user_name(user: telebot.types.User) -> str:
    if user.first_name is not None:
        return user.first_name
    if user.username is not None:
        return user.username
    if user.last_name is not None:
        return user.last_name


def get_schedule_variants_buttons():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    this_week = telebot.types.KeyboardButton('Текущая неделя')
    next_week = telebot.types.KeyboardButton('Следующая неделя')
    today = telebot.types.KeyboardButton('Сегодня')
    markup.row(this_week, next_week)
    markup.row(today)
    return markup


# date comes in dd.mm.yyyy format
def get_schedule_buttons(date_str: str):
    split = date_str.split(".")
    date = datetime.datetime(int(split[2]), int(split[1]), int(split[0]))
    markup = telebot.types.InlineKeyboardMarkup()
    prev_day = date - datetime.timedelta(days=1)
    next_day = date + datetime.timedelta(days=1)
    buttons = [telebot.types.InlineKeyboardButton("<<", callback_data=f"get-{prev_day.date().strftime('%d.%m.%Y')}")]
    if not same_dates(date_str):
        buttons.append(telebot.types.InlineKeyboardButton("Сегодня", callback_data=f"get-today"))
    buttons.append(
        telebot.types.InlineKeyboardButton(">>", callback_data=f"get-{next_day.date().strftime('%d.%m.%Y')}"))
    markup.row(
        *buttons
    )
    return markup


def same_dates(date_str):
    split = date_str.split(".")
    date = datetime.datetime(int(split[2]), int(split[1]), int(split[0]))
    return date.date() == datetime.datetime.today().date()


def get_today_schedule():
    today = datetime.datetime.today()
    return get_one_day_schedule(today)


def get_one_date_from_str(date_str):
    split = date_str.split(".")
    date = datetime.datetime(int(split[2]), int(split[1]), int(split[0]))
    return get_one_day_schedule(date)


def get_one_day_schedule(date: datetime):
    week_num = get_week_number(date)
    schedule = bntu_cache.get_day_schedule(week_num, date.weekday())
    return get_schedule_text(date, schedule, week_num)


def get_week_schedule(week_type) -> str:
    day = datetime.datetime.today()
    if week_type == 'next_week':
        day = day + datetime.timedelta(days=7)
    dates = [day + datetime.timedelta(days=i) for i in range(0 - day.weekday(), 7 - day.weekday())]
    week_number = get_week_number(day)
    week_schedule = bntu_cache.get_week_schedule(week_number)

    text = ""
    iterator = 0
    for day_schedule in week_schedule:
        text += "➖➖➖➖➖➖➖➖➖\n\n"
        text += get_schedule_text(dates[iterator], day_schedule, week_number)
        iterator += 1
    return text


def get_schedule_text(date, schedule, week_num):
    text = ""
    if date.date() == datetime.date.today():
        text += "<b>(Сегодня)</b>\n"
    text += f"🗓<b>{weekdays[date.weekday()]} {date.strftime('%d.%m.%Y')} <i>{week_num} неделя</i></b>\n\n"
    if len(schedule.day_schedule) == 0:
        text += "<b>Занятий нет</b>\n\n"
    else:
        text += str(schedule)
    return text


def get_week_number(date: datetime):
    week = date.date().isocalendar()[1]
    if (week % 2) == 0:
        return 2
    else:
        return 1
