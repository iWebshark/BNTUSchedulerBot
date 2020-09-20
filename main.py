import re
import telebot
import config
import utils
import datetime
from pgres import Database

bot = telebot.TeleBot(config.BOT_TOKEN)
db = Database()


@bot.message_handler(commands=['start'], func=lambda message: message.chat.type == "private")
def greet_new_user(message: telebot.types.Message):
    username = utils.get_user_name(message.from_user)
    available_groups = utils.get_groups_representation(db)
    welcome_message = f"Привет <b><i>{username}</i></b>!\n" \
                      f"С моей помощью ты можешь посмотреть свое расспиание. \n"
    user = db.get_user(message.from_user.id)
    if user is not None:
        welcome_message += f"Твоя группа <b>{user[1]}</b>\n" \
                           f"⬇️Держи расписание⬇️"
        bot.send_message(message.chat.id, welcome_message, parse_mode='html')
        get_today_schedule(message)
    else:
        welcome_message += f"Отправь мне номер одной из доступных групп:\n" \
                           f"{available_groups}"
        buttons = utils.get_buttons_by_options(db.get_available_groups())
        bot.send_message(message.chat.id, welcome_message, parse_mode="html", reply_markup=buttons)


@bot.message_handler(commands=['help'], func=lambda message: message.chat.type == "private")
def show_help_info(message: telebot.types.Message):
    text = f"Список доступный команд (можно просто нажать)\n" \
           f"⚙️ /schedule - показать расписание\n" \
           f"⚙️ /change - сменить группу\n" \
           f"⚙️ /groups - список доступных групп"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['groups'], func=lambda message: message.chat.type == "private")
def show_available_groups(message: telebot.types.Message):
    available_groups = utils.get_groups_representation(db)
    text = f"Доступные группы:\n" \
           f"{available_groups}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['change'])
def change_user_group(message: telebot.types.Message):
    user = db.get_user(message.from_user.id)
    if user is None:
        pass
    else:
        buttons = utils.get_buttons_by_options(db.get_available_groups())
        text = f"Твоя текущая группа: {user[1]}\n" \
               f"Выбери из списка новую группу"
        bot.send_message(message.chat.id, text, reply_markup=buttons)
        show_available_groups(message)


@bot.message_handler(regexp=r"\d{6,10}", func=lambda message: message.chat.type == "private")
def reg_user_group(message: telebot.types.Message):
    user_id = message.from_user.id
    if db.get_group(message.text) is None:
        buttons = utils.get_buttons_by_options(db.get_available_groups())
        bot.send_message(message.chat.id, "Такая группа недоступна!\nВыбери из списка ниже\n", reply_markup=buttons)
        show_available_groups(message)
    else:
        db.reg_user(user_id, message.text)
        bot.send_message(message.chat.id, f"Теперь твоя группа: <b>{message.text}\n</b>"
                                          f"⬇️Вот твое расписание⬇️", parse_mode='html')
        get_today_schedule(message)


@bot.message_handler(commands=['schedule'], func=lambda message: message.chat.type == "private", )
def get_today_schedule(message: telebot.types.Message):
    if db.get_user_group(message.from_user.id) is None:
        buttons = utils.get_buttons_by_options(db.get_available_groups())
        bot.send_message(message.chat.id, "Группа не выбрана!\nВыбери из списка ниже\n", reply_markup=buttons)
        show_available_groups(message)
    else:
        text = utils.get_today_schedule(db, message.from_user.id)
        date_str = re.search(r"\d{2}.\d{2}.\d{4}", text).group(0)
        markup = utils.get_schedule_buttons(date_str)
        bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def move_to_selected_day(call: telebot.types.CallbackQuery):
    if db.get_user_group(call.from_user.id) is None:
        buttons = utils.get_buttons_by_options(db.get_available_groups())
        bot.send_message(call.message.chat.id, "Группа не выбрана!\nВыбери из списка ниже\n", reply_markup=buttons)
        show_available_groups(call.message)
    else:
        date_str = call.data.split("-")[1]
        if date_str == "today":
            today = datetime.datetime.today()
            date_str = today.strftime('%d.%m.%Y')
        text = utils.get_one_date_from_str(db, call.from_user.id, date_str)
        buttons = utils.get_schedule_buttons(date_str)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              parse_mode='html',
                              reply_markup=buttons)


@bot.message_handler(content_types=['text'])
def process_text_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Не понимаю😣")


if __name__ == '__main__':
    bot.polling(none_stop=True)
