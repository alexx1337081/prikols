import telebot
import datetime
from nado import data, nice
import random
token='7868964757:AAEN8BRIyF6CJHOKT1ywAr424zFlW68NY6M'
vowels = ['а', 'о', 'у', 'э', 'ы', 'я', 'ё', 'ю', 'е', 'и']
bot=telebot.TeleBot(token)



def random_udar(word):
    current_udar = [i for i in range(len(word)) if word[i] == word[i].upper()][0]
    incorr_udars = [i for i in range(len(word)) if word[i].lower() in vowels]
    incorr_udars.remove(current_udar)
    incorr_udar = random.choice(incorr_udars)
    word = word.lower()
    word = word.split('(')[0]
    word_udar = ''
    for i, let in enumerate(word):
        if i == incorr_udar:
            word_udar += let.upper()
            continue
        word_udar += let

    return word_udar + word[1]


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.id == 1237189946:
        bot.send_message(message.chat.id, 'здравствуйте мой повелитель')
    bot.send_message(message.chat.id,"введи /check")
    print(datetime.datetime.now(),message.from_user.id,message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
          message.text)

@bot.message_handler(commands=['check'])
def start_message(message):
    global ans
    if message.from_user.username != 'difuzlik':
        d = data
        words = [d.pop(random.randint(0, len(d))) for i in range(5)]
        task = []
        ncorr = random.randint(2, 3)
        ans = ''
        for i, word in enumerate(words):
            if ncorr != 0:
                task.append(word)
                ans += str(i+1)
                ncorr -= 1
                continue
            task.append(random_udar(word))
        bot.send_message(message.chat.id, f'Где правильно ударение стоит епт?\n'
                                              f'1) {task[0]}\n'
                                              f'2) {task[1]}\n'
                                              f'3) {task[2]}\n'
                                              f'4) {task[3]}\n'
                                              f'5) {task[4]}')


    else:
        bot.send_message(message.chat.id, 'русик пошёл нахуй')



@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data.split('.')[0] == 1:
        res = []
    if callback.data.split('.')[1] in data:
        bot.send_message(callback.message.chat.id, 'хорош')
        res.append(1)
    else:
        bot.send_message(callback.message.chat.id, 'лох')
        res.append(0)
    print(res)





@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.from_user.username == 'difuzlik':
        bot.send_message(message.chat.id, 'русик иди в пизду')
    if message.text.lower() == 'иди нахуй':
        bot.send_message(message.chat.id, 'сам иди нахуй пидор ебанный')
    if message.text.lower() == 'соси':
        bot.send_message(message.chat.id, 'сам соси уебок')
    try:
        int(message.text)
        if message.text == ans:
            bot.send_message(message.chat.id, 'пральна')
        else:
            bot.send_message(message.chat.id, 'нипральна')
    except:
        pass
    print(datetime.datetime.now(), message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
          message.text)


bot.infinity_polling()