import telebot
import datetime

from nado import data, bred
import random
import psycopg2
token='7868964757:AAEN8BRIyF6CJHOKT1ywAr424zFlW68NY6M'
vowels = ['а', 'о', 'у', 'э', 'ы', 'я', 'ё', 'ю', 'е', 'и']
bot=telebot.TeleBot(token)
conn = psycopg2.connect(dbname='udar', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()



def correct_udar(word):
    for i in data:
        if word.lower() == i.lower():
            return i
    return 'хз'

def corr_words(usr_answer, answer):
    res = set(set(answer[0]) & set(usr_answer))#общее - пересечение
    return [correct_udar(answer[int(i)]) for i in res]

def incorr_words(usr_answer, answer):
    res = set(usr_answer+answer[0]) #общее множество
    res = res - set(set(answer[0]) & set(usr_answer))#общее - пересечение
    return [correct_udar(answer[int(i)]) for i in res]


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
    global is_ans
    is_ans = 0
    cursor.execute('select id from users')
    users = [i[0] for i in cursor.fetchall()]
    if message.from_user.id not in users:
        bot.send_message(message.chat.id, 'тебя нет в базе, введи своё имя(до 40 символов, поменять нельзя ваще, подумай хорошенько)')
        reg = 1
    else:
        bot.send_message(message.chat.id, 'какой рег, ты есть уже')
        print(datetime.datetime.now(), message.from_user.id, message.from_user.username, '-',
              message.from_user.first_name, message.from_user.last_name, ": тщетно пытается зарегаться",)


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.id == 1237189946:
        bot.send_message(message.chat.id, 'дарова санёк')
    if message.from_user.id == 1253076174:
        bot.send_message(message.chat.id, 'Я люблю тебя!')
    bot.send_message(message.chat.id,"Это бот для подготовки к 4-ому заданию ЕГЭ по русскому языку\n/check - получить задиние\n/stat - посмотреть статистику")
    print(datetime.datetime.now(),message.from_user.id,message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
          message.text)

@bot.message_handler(commands=['check'])
def get_task(message):
    print(message.from_user.first_name, 'взял таску')
    cursor.execute('select id from users')
    users = [i[0] for i in cursor.fetchall()]
    if message.from_user.id not in users:
        bot.send_message(message.chat.id, 'ты не зареган пиши /reg')
        return None
    cursor.execute('select word from problems '
                  f'where user_id = {message.from_user.id} and mistakes = (select max(mistakes) from problems)')
    pwords = cursor.fetchall()
    global ans
    global reg
    reg = 0
    if not pwords:
        words = random.sample(data, 5)
    else:
        words = random.sample(data, 4)
        while len(words) < 5:
            pword = random.choice(pwords)[0]
            if pword.lower() not in [i.lower() for i in words]:
                words.append(pword)
        random.shuffle(words)
    task = []
    ncorr = random.randint(2, 4)
    ans = []
    for i, word in enumerate(words):
        if ncorr != 0:
            task.append((word, 1))
            ncorr -= 1
            continue
        task.append((random_udar(word), 0))
    random.shuffle(task)
    ans.append(''.join([str(i+1) for i in range(len(task)) if task[i][1]]))
    ans.extend([i[0] for i in task])
    bot.send_message(message.chat.id, f'Где правильно ударение стоит?\n'
                                          f'1) {task[0][0]}\n'
                                          f'2) {task[1][0]}\n'
                                          f'3) {task[2][0]}\n'
                                          f'4) {task[3][0]}\n'
                                          f'5) {task[4][0]}')
    global is_ans
    is_ans = 1

@bot.message_handler(commands=['stat'])
def check_stat(message):
    cursor.execute('select * from users')
    query = cursor.fetchall()
    users = [i[0] for i in query]
    if message.from_user.id not in users:
        bot.send_message(message.chat.id, 'куда тебе стат давай пиши /reg')
        return None

    stats = [(i[1], i[4]) for i in query]
    stats = sorted(stats, key=lambda x: x[1])
    cursor.execute('select * from users '
                  f'where id = {message.from_user.id}' )
    query = cursor.fetchall()
    if query[0][2] != 0:
        bot.send_message(message.chat.id, f'всего решено заданий: {query[0][2]}\n'
                                              f'правильно из них решено: {query[0][3]} ({round(query[0][3]/query[0][2]*100, 1)}%)\n'
                                              f'рейтинг: {query[0][4]}')
        bot.send_message(message.chat.id,f'самый главный лошарик - {stats[0][0]}\n'
                         f'рейтинг позорника: {stats[0][1]}')
    else:
        bot.send_message(message.chat.id, 'ты ниче не решал')



@bot.message_handler(content_types=['text'])
def send_text(message):
    print(datetime.datetime.now(), message.from_user.username, '-', message.from_user.first_name,
          message.from_user.last_name, ": ",
          message.text)
    global reg
    if reg:
        if len(message.text) > 40:
            bot.send_message(message.chat.id, 'меньше сорока камон')
            reg = 0
            return None
        cursor.execute('INSERT INTO users '
                       f"VALUES ({message.from_user.id}, '{message.text}', 0, 0, 0)")
        conn.commit()
        print('новый пользователь', message.from_user.id, message.from_user.first_name, message.from_user.last_name, ": ", message.text)
        bot.send_message(message.chat.id, 'успешно')
        reg = 0
        return None
    button1 = telebot.types.KeyboardButton("/check")
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    string = message.text
    global is_ans
    if is_ans:
        try:
            int(string)
        except ValueError:
            bot.send_message(message.chat.id, random.choice(bred))
            return None
        if len(string) >= 2 and len(string) <= 4 and all(
                map(lambda x: int(x) >= 1 and int(x) <= 5, string)) and string == ''.join(
                sorted([str(i) for i in string])) and len(set(string)) == len(string):
            if message.text == ans[0]:
                keyboard.add(button1)
                bot.send_message(message.chat.id, 'пральна', reply_markup=keyboard)
                cursor.execute('UPDATE users '
                               'SET total_tasks = total_tasks + 1, '
                               '    correct_tasks = correct_tasks + 1, '
                               '    rating = rating + 1 '
                               f'WHERE id = {message.from_user.id};')
                conn.commit()
                is_ans = 0
            else:
                keyboard.add(button1)
                bot.send_message(message.chat.id, f'нипральна, пральна будет {ans[0]}', reply_markup=keyboard)
                cursor.execute('UPDATE users '
                               'SET total_tasks = total_tasks + 1, '
                               '    rating = rating - 3 '
                               f'WHERE id = {message.from_user.id}; ')
                conn.commit()
                mistake_print = ''
                for i in incorr_words(message.text, ans):
                    mistake_print += f'\n\t{i}'
                    cursor.execute('INSERT INTO problems (user_id, word, mistakes)'
                                  f"VALUES ({message.from_user.id}, '{i}', 1)"
                                   'ON CONFLICT (word)'
                                   'DO UPDATE SET mistakes = problems.mistakes + 1')
                conn.commit()
                is_ans = 0
                bot.send_message(message.chat.id, f'ошибки в словах:' + mistake_print)
            for i in corr_words(message.text, ans):
                cursor.execute('UPDATE problems '
                               'SET mistakes = mistakes - 1 '
                              f"WHERE word = '{i}'")
                conn.commit()
            cursor.execute('DELETE FROM problems WHERE mistakes <= 0')
            conn.commit()
        else:
            bot.send_message(message.chat.id, random.choice(bred))



print('поехал')
bot.infinity_polling()