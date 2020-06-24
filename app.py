import json
from datetime import datetime
import telebot
from telebot import types
from telebot.apihelper import _make_request
import pytz
from time import sleep
# "1206195696:AAGMrhQEMMnzyjP5VukNUBS2WgwlE8-jFBw"
# -1001475972248
bot = telebot.TeleBot("1206195696:AAGMrhQEMMnzyjP5VukNUBS2WgwlE8-jFBw")
chat_for = "-1001475972248"
admin_id = 327659575
my_permissions = {
    "can_send_messages": False,
    "can_send_media_messages": False,
    "can_send_polls": False,
    "can_send_other_messages": False
}

allowed_permissions = {
    "can_send_messages": True,
    "can_send_media_messages": True,
    "can_send_polls": True,
    "can_send_other_messages": True
}

new_permissions = types.ChatPermissions(**my_permissions)
allowed_permissions = types.ChatPermissions(**allowed_permissions)

print("start")
print(f"{bot.get_me().username}")

with open("interval.txt", "r") as f:
    interval = f.read()



@bot.message_handler(commands=['start'])
def any_msg(message):

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_button_yes = types.InlineKeyboardButton(text="Поставить время⏳", callback_data=f"yes{message.from_user.id}")
    callback_button_no = types.InlineKeyboardButton(text="Хочу такого же бота🤖", callback_data="no")
    keyboard.add(callback_button_yes, callback_button_no)
    bot.send_message(message.chat.id, """Добро пожаловать {}!🙋‍♂️
Выберите пожалуйста причину вашего входа👇🏻""".format(message.from_user.first_name),reply_markup=keyboard)


@bot.message_handler()
def do_freeze(message):
    check = "undo"
    now = "ye"
    if message.from_user.id == admin_id and message.text.isdigit() and int(message.text) >= 10 and int(message.text) <= 23:

        print(message.text)

        bot.send_message(message.chat.id, """Таймер поставлен✅""")
        while check == "undo":
            sleep(60)
            if datetime.now(pytz.timezone("Europe/Moscow")).strftime("%H") == message.text:
                bot.set_chat_permissions(chat_for, new_permissions)
                now = int(datetime.now(pytz.timezone("Europe/Moscow")).strftime("%H"))
                bot.send_message(message.chat.id, """Установлен час тишины✅
    Для всех участников чата активирована режим чтения⏳""")
                bot.send_message(chat_for, """Установлен час тишины✅
    Для всех участников чата активирована режим чтения⏳""")
                check = "do"
                print(now)
    elif message.from_user.id != admin_id and message.text.isdecimal():
        bot.send_message(message.chat.id, """У вас нет прав поставить таймер🚫""")
    elif message.from_user.id == admin_id and message.text.isdigit() and int(message.text) >= 1 and int(message.text) <= 9:
        bot.send_message(message.chat.id, """Неправильное время🚫""")

    while check == "do":
        if int(datetime.now(pytz.timezone("Europe/Moscow")).strftime("%H")) == int(now) + int(interval):
            bot.set_chat_permissions(chat_for, allowed_permissions)
            bot.send_message(message.chat.id, """Ограничения сняты✅
Участники могут отправлять сообщения!🥳""")
            bot.send_message(chat_for, """Ограничения сняты✅
Участники могут отправлять сообщения!🥳""")
            print("uspex1")
            check = "ando"



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith("yes"):
        global ID
        ID = str(call.data.replace("yes","")) # ID клиента

        s = bot.send_message(call.message.chat.id, text = "Напишите начальное время в нужном формате...📝")

        bot.register_next_step_handler(s,do_freeze) # Переходим в do_freeze


    elif call.data == "no":
        bot.send_message(call.message.chat.id, text = "Позже здесь появится инструкция для поставки бота на вашу группу)")


bot.polling()
