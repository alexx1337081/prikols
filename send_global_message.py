import datetime
import psycopg2
import telebot
from telebot import types
token='7868964757:AAEN8BRIyF6CJHOKT1ywAr424zFlW68NY6M'
bot=telebot.TeleBot(token)
conn = psycopg2.connect(dbname='udar', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def start_message(message):
    cursor.execute('SELECT id FROM users')
    users = cursor.fetchall()
    for id in users:
        bot.send_message(id[0],"В связи с тем, что некий\n Куртов Кирилл Васильевич(@kirushabbq) добровольно пополнил призовой фонд на 1250(!) рублей, вносятся некоторые изменения\n1 место - 1500р\n2 место - 1000р\n3 место - 500\n4 место - литр энджера на выбор\n5 место - литр энджера гранат")


bot.polling()