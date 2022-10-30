#!/usr/bin/python3
# require for working to install different packets not include in python: yTelegramBotAPI, psutil
import telebot   # pip install pyTelegramBotAPI
import config
import time
import psutil    # pip install psutil
import sqlite3

bot = telebot.TeleBot(config.TOKEN_SPIDER)


@bot.message_handler(commands=["downed"])
def downed(message):
    if id_user(message) is True:
        while True:
            down(message)
    else:
        bot.reply_to(message, f'\n{"ACCESS DENIED"}')


@bot.message_handler(commands=["info"])
def info(message):
    if id_user(message) is True:
        stat(message)
    else:
        bot.reply_to(message, f'\n{"ACCESS DENIED"}')


@bot.message_handler(commands=["start"])
def start(message):
    if id_user(message) is True:
        while True:
            stat(message)
            time.sleep(10)
    else:
        bot.reply_to(message, f'\n{"ACCESS DENIED"}')


@bot.message_handler(content_types=['text'])
def id_user(message):
    user_id = message.from_user.id
    f_name = message.from_user.first_name    # when user send you a message, it shows you name and id in terminal.
    print(f_name, user_id)     # when user send you a message, it shows you name and id in terminal.
    conn = sqlite3.connect("database_users.db")
    for y in conn.execute(f"SELECT userid FROM users WHERE userid='{int(user_id)}'"):
        for x in y:
            if int(user_id) == int(x):
                return True
        else:
            return False
    conn.close()


def down(message):
    while True:
        list_diff = []
        proc1 = []
        for proc in psutil.process_iter(['pid', 'name']):
            proc1.append(proc.name())
            data = (                   # type name of your process
                "Telegram",
                "htop"
            )
            if data not in proc1:
                list_diff = set(data) - set(proc1)
        if len(list_diff) <= 0:
            continue
        bot.send_message(message.chat.id, f'\n ⚠PROCESS_IS_DOWN⚠\n{list_diff}')
        time.sleep(10)


def stat(message):
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        data = (                      # type name of your process
            "Telegram",
            "htop"
        )
        for data in data:
            if data in proc.name():
                time.sleep(1)
                bot.send_message(message.chat.id, f'\n{proc.name()} ✅ \nPID {proc.pid}')


def bot_polling():
    while True:
        try:
            print('*' * 10, "BOT_IS_STARTED", '*' * 10)
            bot.polling(none_stop=True, interval=3)
        except Exception as e:  # except ConnectionError or ConnectionResetError
            # or TimeoutError or ConnectionAbortedError as e:
            print(f"Bot polling failed, restarting in {'15sec'}sec.\nError:\n{e}")
            bot.stop_polling()
            time.sleep(30)
        else:
            bot.stop_polling()
            print('*' * 10, "Bot polling loop finished", '*' * 10)
            break


bot_polling()
