import telebot
import datetime

weekdays = {0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 4: 'Пт', 5: 'Сб', 6: 'Вс'}


def get_user_name(user: telebot.types.User) -> str:
    if user.first_name is not None:
        return user.first_name
    if user.username is not None:
        return user.username
    if user.last_name is not None:
        return user.last_name


def get_buttons_by_options(options):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for option in options:
        button = telebot.types.KeyboardButton(option)
        markup.add(button)
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
    buttons.append(telebot.types.InlineKeyboardButton(">>", callback_data=f"get-{next_day.date().strftime('%d.%m.%Y')}"))
    markup.row(
        *buttons
    )
    return markup


def get_groups_representation(db):
    groups = db.get_available_groups()
    available_groups = ""
    for group in groups:
        available_groups += f"- {group}\n"
    return available_groups


def get_today_schedule(db, user_id):
    today = datetime.datetime.today()
    return get_one_day_schedule(db, user_id, today)


def get_one_date_from_str(db, user_id, date_str):
    split = date_str.split(".")
    date = datetime.datetime(int(split[2]), int(split[1]), int(split[0]))
    return get_one_day_schedule(db, user_id, date)


def get_one_day_schedule(db, user_id, date: datetime):
    week_num = get_week_number(date)
    classes = db.get_day_schedule(user_id, date.weekday(), week_num)
    text = ""
    if date.date() == datetime.date.today():
        text += "<b>(Сегодня)</b>\n"
    text += f"🗓{weekdays[date.weekday()]} {date.strftime('%d.%m.%Y')} <i>{week_num} неделя</i>\n\n"
    if len(classes) == 0:
        text += "<b>Занятий нет</b>"
    else:
        for cl in classes:
            text += f"{cl}\n\n"
    return text


def get_week_number(date: datetime):
    week = date.date().isocalendar()[1]
    if (week % 2) == 0:
        return 1
    else:
        return 2


def same_dates(date_str):
    split = date_str.split(".")
    date = datetime.datetime(int(split[2]), int(split[1]), int(split[0]))
    return date.date() == datetime.datetime.today().date()


def send_messages(db, bot):
    date = datetime.datetime.today()
    if date.weekday() != 6:
        users = db.get_users()
        for user in users:
            text = get_today_schedule(db, user[0])



