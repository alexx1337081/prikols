import telebot
import datetime
from nado import data
import random
import psycopg2
token='7868964757:AAEN8BRIyF6CJHOKT1ywAr424zFlW68NY6M'
vowels = ['а', 'о', 'у', 'э', 'ы', 'я', 'ё', 'ю', 'е', 'и']
bot=telebot.TeleBot(token)
conn = psycopg2.connect(dbname='udar', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()

# def random_udar(word):
#     res = []
#     p = 0
#     q = 1
#     word = word.lower()
#     word_udar = ''
#     for _ in range(len([i for i in word if i in vowels])):
#         for letter in word:
#             if letter in vowels:
#                 p += 1
#                 if p == q:
#                     word_udar += letter.upper()
#                     continue
#             word_udar += letter
#         res.append(word_udar)
#         word_udar = ''
#         q +=1
#         p = 0
#     return res


def random_udar(word):
    if '(' in word:
        if word.split(' (')[0] == word:
            wordv = word.split(') ')[1]
            words = word.split(') ')[0] + ') '
            p = 0
        else:
            wordv = word.split(' (')[0]
            words = '(' + word.split(' (')[1]
            p = 1
    else:
        wordv = word
        words = ''
        p = 0
    current_udar = [i for i in range(len(wordv)) if wordv[i] == wordv[i].upper()][0]
    incorr_udars = [i for i in range(len(wordv)) if wordv[i].lower() in vowels]
    incorr_udars.remove(current_udar)
    incorr_udar = random.choice(incorr_udars)
    wordv = wordv.lower()
    word_udar = ''
    for i, let in enumerate(wordv):
        if i == incorr_udar:
            word_udar += let.upper()
            continue
        word_udar += let

    if p == 0: return words + word_udar
    if p == 1: return word_udar + ' ' + words


@bot.message_handler(commands=['reg'])
def register(message):
    global reg
    cursor.execute('select id from users')
    users = [i[0] for i in cursor.fetchall()]
    if message.from_user.id not in users:
        bot.send_message(message.chat.id, 'тебя нет в базе, введи своё имя(до 255 символов, поменять нельзя ваще, подумай хорошенько)')
        reg = 1
    else:
        bot.send_message(message.chat.id, 'какой рег, ты есть уже')
        print(datetime.datetime.now(), message.from_user.id, message.from_user.username, '-',
              message.from_user.first_name, message.from_user.last_name, ": тщетно пытается зарегаться",)


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.id == 1237189946:
        bot.send_message(message.chat.id, 'здравствуйте мой повелитель')
    bot.send_message(message.chat.id,"дарова\nсписок команд:\n/start ты уже нажал\n/check получить задание\n/reg регистрация для учёта статистики\n/stat вывод статистики")
    print(datetime.datetime.now(),message.from_user.id,message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
          message.text)

@bot.message_handler(commands=['check'])
def start_message(message):
    cursor.execute('select id from users')
    users = [i[0] for i in cursor.fetchall()]
    if message.from_user.id not in users:
        bot.send_message(message.chat.id, 'ты не зареган пиши /reg')
        return None
    global ans
    global reg
    reg = 0
    d = data
    words = [d.pop(random.randint(0, len(d))) for i in range(5)]
    task = []
    ncorr = random.randint(2, 4)
    ans = ''
    for i, word in enumerate(words):
        if ncorr != 0:
            task.append((word, 1))
            ncorr -= 1
            continue
        task.append((random_udar(word), 0))
    random.shuffle(task)
    ans = ''.join([str(i+1) for i in range(len(task)) if task[i][1]])
    bot.send_message(message.chat.id, f'Где правильно ударение стоит?\n'
                                          f'1) {task[0][0]}\n'
                                          f'2) {task[1][0]}\n'
                                          f'3) {task[2][0]}\n'
                                          f'4) {task[3][0]}\n'
                                          f'5) {task[4][0]}')

@bot.message_handler(commands=['stat'])
def check_stat(message):
    cursor.execute('select id from users')
    users = [i[0] for i in cursor.fetchall()]
    if message.from_user.id not in users:
        bot.send_message(message.chat.id, 'куда тебе стат давай пиши /reg')
        return None
    cursor.execute('select total_tasks, correct_tasks from users '
                  f'where id = {message.from_user.id}' )
    query = cursor.fetchall()
    print(query)
    bot.send_message(message.chat.id, f'всего решено заданий: {query[0][0]}\n'
                                          f'правильно из них решено: {query[0][1]}\n'
                                          f'винрейт: {round(query[0][1]/query[0][0]*100, 1)}%')



@bot.message_handler(content_types=['text'])
def send_text(message):
    global reg
    if reg:
        cursor.execute('INSERT INTO users '
                       f"VALUES ({message.from_user.id}, '{message.text}', 0, 0)")
        conn.commit()
        print('новый пользователь', message.from_user.id, message.from_user.first_name, message.from_user.last_name, ": ", message.text)
        bot.send_message(message.chat.id, 'успешно')
        reg = 0
        return None

    if message.text == ans:
        bot.send_message(message.chat.id, 'пральна')
        cursor.execute('UPDATE users '
                       'SET total_tasks = total_tasks + 1, '
                       '    correct_tasks = total_tasks + 1 '
                      f'WHERE id = {message.from_user.id};')
        conn.commit()
    else:
        bot.send_message(message.chat.id, f'нипральна, пральна будет {ans}')
        cursor.execute('UPDATE users '
                       'SET total_tasks = total_tasks + 1 '
                      f'WHERE id = {message.from_user.id}; ')
        conn.commit()
    print(datetime.datetime.now(), message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
          message.text)

print('поехал')
bot.infinity_polling()