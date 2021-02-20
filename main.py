import re
import time
import telebot
import utils
import datetime
from pgres import Database
import os
from flask import Flask, request
import bntu_cache

secret = 'tth1uomktubXBGEX8FsZ04vh0s3PRMll'
url = 'https://bntu-scheduler-bot.herokuapp.com/' + secret
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
db = Database()

bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=url)

app = Flask(__name__)


@app.route('/' + secret + '/cache/users', methods=['GET'])
def delete_users_cache():
    bntu_cache.users_cache.clear()
    return "Users cache cleared!"


@app.route('/' + secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@bot.message_handler(commands=['help'])
def show_help_info(message: telebot.types.Message):
    text = f"Список доступный команд (можно просто нажать)\n" \
           f"⚙️ /today - показать расписание на сегодня" \
           f"⚙️ /this_week - показать расписание на эту неделю\n" \
           f"⚙️ /next_week - показать расписание на следующую неделю"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
def greet_new_user(message: telebot.types.Message):
    utils.reg_or_update_user(message)

    username = utils.get_user_name(message.from_user)
    welcome_message = f"Привет <b><i>{username}</i></b>!\n" \
                      f"С моей помощью ты можешь посмотреть расспиание группы 11101516 \n"
    buttons = utils.get_schedule_variants_buttons()
    bot.send_message(message.chat.id, welcome_message, parse_mode='html', reply_markup=buttons)


# Today schedule variant
@bot.message_handler(commands=['today'])
@bot.message_handler(func=lambda message: message.text == 'Сегодня')
def get_today_schedule(message: telebot.types.Message):
    utils.reg_or_update_user(message)

    text = utils.get_today_schedule()
    date_str = re.search(r"\d{2}.\d{2}.\d{4}", text).group(0)
    markup = utils.get_schedule_buttons(date_str)
    bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def move_to_selected_day(call: telebot.types.CallbackQuery):
    date_str = call.data.split("-")[1]
    if date_str == "today":
        today = datetime.datetime.today()
        date_str = today.strftime('%d.%m.%Y')
    text = utils.get_one_date_from_str(date_str)
    buttons = utils.get_schedule_buttons(date_str)
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          parse_mode='html',
                          reply_markup=buttons)


# Get week schedule
@bot.message_handler(commands=['this_week'])
@bot.message_handler(func=lambda message: message.text == 'Текущая неделя')
def get_week_schedule(message: telebot.types.Message):
    utils.reg_or_update_user(message)

    schedule_text = utils.get_week_schedule('this_week')
    bot.send_message(message.chat.id, schedule_text, parse_mode='html')


@bot.message_handler(commands=['next_week'])
@bot.message_handler(func=lambda message: message.text == 'Следующая неделя')
def get_week_schedule(message: telebot.types.Message):
    utils.reg_or_update_user(message)

    schedule_text = utils.get_week_schedule('next_week')
    bot.send_message(message.chat.id, schedule_text, parse_mode='html')


@bot.message_handler(content_types=['text'])
def process_text_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Не понимаю😣")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
