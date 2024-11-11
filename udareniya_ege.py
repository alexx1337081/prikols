import telebot
import datetime
from nado import data
token='7644736024:AAEC_Rwhhi3p5ckKV1_ZZ-t9cLhwmnzkmJ8'
bot=telebot.TeleBot(token)


def get_ans(task):
    try:
        words = [task.split('\n')[0].split('  ')[1].strip(),
                 task.split('\n')[2].split('  ')[1].strip(),
                 task.split('\n')[4].split('  ')[1].strip(),
                 task.split('\n')[6].split('  ')[1].strip(),
                 task.split('\n')[8].split('  ')[1].strip()]
    except:
        try:
            words = [task.split('\n')[0].split(')')[1].strip(),
                     task.split('\n')[2].split(')')[1].strip(),
                     task.split('\n')[4].split(')')[1].strip(),
                     task.split('\n')[6].split(')')[1].strip(),
                     task.split('\n')[8].split(')')[1].strip()]
        except:
            words = [task.split('\n')[0].split(')')[1].strip(),
                     task.split('\n')[1].split(')')[1].strip(),
                     task.split('\n')[2].split(')')[1].strip(),
                     task.split('\n')[3].split(')')[1].strip(),
                     task.split('\n')[4].split(')')[1].strip()]
    ans = ''
    miss = ''
    for i, word in enumerate(words):
        if word in data:
            ans += str(i+1)
        elif word.lower() not in [i.lower() for i in data]:
            miss += str(f'слова {word} нет в справочнике\n')
    return ans, miss




@bot.message_handler(commands=['start'])
def start_message(message):
  if message.from_user.id == 1237189946:
      bot.send_message(message.chat.id, 'здравствуйте мой повелитель')
  bot.send_message(message.chat.id,"Привет ✌️ короче копируй задание с сайта без условия тупа слова с их циферками и я тебе ответ скидываю.\nP.S. вряд ли в базе бота есть все слова которые попадаются на сайте, бот выбирает варианты которые точно верны и указывает на затруднительные слова")
  bot.send_message(message.chat.id, "Сообщение снизу - пример ввода, попробуй скопировать его в чат для проверки")
  bot.send_message(message.chat.id, "1)  окрУжит\n2)  Отрочество\n3)  облЕгчит\n4)  отдалА\n5)  какАшка")
  print(datetime.datetime.now(),message.from_user.id,message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
        message.text)

@bot.message_handler(content_types=['text'])
def send_text(message):
    p = 'норм'
    if message.text.lower() == 'иди нахуй':
        bot.send_message(message.chat.id, 'сам иди нахуй пидор ебанный')
    if message.text.lower() == 'соси':
        bot.send_message(message.chat.id, 'сам соси уебок')
    # try:
    bot.send_message(message.chat.id, f'{get_ans(message.text)[0]}\n{get_ans(message.text)[1]}')
    # except:
    #     bot.send_message(message.chat.id, 'чето не то я хз')
    #     p = 'баг'
    print(p, datetime.datetime.now(), message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
          message.text)


bot.infinity_polling()













