import telebot
import datetime
import emoji
from nado import data, bred
import random
import psycopg2
from telebot import types
token='7868964757:AAEN8BRIyF6CJHOKT1ywAr424zFlW68NY6M'
vowels = ['а', 'о', 'у', 'э', 'ы', 'я', 'ё', 'ю', 'е', 'и']
bot=telebot.TeleBot(token)
conn = psycopg2.connect(dbname='udar', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()



def is_emoji(s):
    return s in emoji.UNICODE_EMOJI


def correct_udar(word):
    for i in data:
        if word.lower() == i.lower():
            return i
    return 'хз'


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    click = call.data.split('_')[0]
    user_id = call.data.split('_')[1]
    if call.message:
        if click == "check":
            cursor.execute('select word from problems '
                           f'where user_id = {user_id} and mistakes = (select max(mistakes) from problems where user_id = {user_id})')
            pwords = cursor.fetchall()
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
            ans.append(''.join([str(i + 1) for i in range(len(task)) if task[i][1]]))
            ans.extend([i[0] for i in task])
            bot.send_message(user_id, f'Где правильно ударение стоит?\n'
                                              f'1) {task[0][0]}\n'
                                              f'2) {task[1][0]}\n'
                                              f'3) {task[2][0]}\n'
                                              f'4) {task[3][0]}\n'
                                              f'5) {task[4][0]}')
            cursor.execute('INSERT INTO events (user_id, ans, word1, word2, word3, word4, word5)'
                           f"VALUES ({user_id}, '{ans[0]}', '{ans[1]}', '{ans[2]}', '{ans[3]}', '{ans[4]}', '{ans[5]}')"
                           'ON CONFLICT (user_id)'
                           f"DO UPDATE SET ans = '{ans[0]}', "
                           f"              word1 = '{ans[1]}',"
                           f"              word2 = '{ans[2]}',"
                           f"              word3 = '{ans[3]}',"
                           f"              word4 = '{ans[4]}',"
                           f"              word5 = '{ans[5]}'")
            conn.commit()
        if click == "stat":
            cursor.execute('select * from users')
            query = cursor.fetchall()
            stats = [(i[1], i[4], i[0]) for i in query]
            stats = sorted(stats, key=lambda x: x[1])
            cursor.execute('select * from users '
                           f'where id = {user_id}')
            query = cursor.fetchall()
            otvet = types.InlineKeyboardMarkup(row_width=3)
            button1 = types.InlineKeyboardButton("Получить задание📲", callback_data=f'check_{user_id}')
            otvet.add(button1)
            if str(stats[0][2]) == user_id:
                pozor = 'Cамый главный лошарик - ВЫ😲'
            else:
                pozor = (f'Cамый главный лошарик - {stats[0][0] or 'пока без имени'}\n'
                         f'С рейтингом: {stats[0][1]}')
            bot.send_message(user_id, f'Всего решено заданий: {query[0][2]}\n'
                                              f'Ваш винрейт: {round(query[0][3] / query[0][2] * 100, 1)}%\n'
                                              f'Ваш рейтинг: {query[0][4]}\n'+
                                              pozor, reply_markup=otvet)





def corr_words(usr_answer, answer):
    res = set(set(answer[0]) & set(usr_answer))#общее - пересечение
    return [correct_udar(answer[int(i)]) for i in res]

def incorr_words(usr_answer, answer):
    res = set(usr_answer+answer[0]) #общее множество
    res = res - set(set(answer[0]) & set(usr_answer))#общее - пересечение
    return [correct_udar(answer[int(i)]) for i in res]


def check_reg(id):
    cursor.execute('SELECT id FROM users')
    if id not in [i[0] for i in cursor.fetchall()]:
        cursor.execute(f"INSERT INTO users(id, total_tasks, correct_tasks, rating) VALUES({id}, 0, 0, 0)")
        conn.commit()
        print('новый пользователь**************', id)
        return False
    else:
        return True


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
    wordv = wordv.lower().replace('ё', 'е')
    word_udar = ''
    for i, let in enumerate(wordv):
        if i == incorr_udar:
            word_udar += let.upper()
            continue
        word_udar += let

    if p == 0: return words + word_udar
    if p == 1: return word_udar + ' ' + words



@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.id == 1237189946:
        bot.send_message(message.chat.id, 'дарова санёк')
    if message.from_user.id == 1253076174:
        bot.send_message(message.chat.id, 'Я люблю тебя!')
    check_reg(message.from_user.id)
    otvet = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton("Получить задание📲", callback_data=f'check_{message.from_user.id}')
    otvet.add(button1)
    bot.send_message(message.chat.id,"Это бот для подготовки к 4-ому заданию ЕГЭ по русскому языку", reply_markup=otvet)
    print(datetime.datetime.now(),message.from_user.id,message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
          message.text)


@bot.message_handler(commands=['stat'])
def check_stat(message):
    print(datetime.datetime.now(), message.from_user.id, message.from_user.username, '-', message.from_user.first_name,
          message.from_user.last_name, ": ",
          message.text)
    check_reg(message.from_user.id)
    cursor.execute('select * from users')
    query = cursor.fetchall()
    stats = [(i[1], i[4], i[0]) for i in query]
    stats = sorted(stats, key=lambda x: x[1])
    cursor.execute('select * from users '
                  f'where id = {message.from_user.id}' )
    query = cursor.fetchall()
    if query[0][2] != 0:
        bot.send_message(message.chat.id, f'всего решено заданий: {query[0][2]}\n'
                                              f'правильно из них решено: {query[0][3]} ({round(query[0][3]/query[0][2]*100, 1)}%)\n'
                                              f'рейтинг: {query[0][4]}')
        if stats[0][2] == message.from_user.id:
            bot.send_message(message.chat.id, f'самый главный лошарик - ВЫ😲')
        else:
            bot.send_message(message.chat.id,f'самый главный лошарик - {stats[0][0] or 'пока без имени'}\n'
                                                  f'рейтинг позорника: {stats[0][1]}')
    else:
        bot.send_message(message.chat.id, 'ты ниче не решал')



@bot.message_handler(content_types=['text'])
def send_text(message):
    print(datetime.datetime.now(), message.from_user.username, '-', message.from_user.first_name,
          message.from_user.last_name, ": ",
          message.text)
    check_reg(message.from_user.id)
    otvet = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton("Ещё задание📲", callback_data=f'check_{message.from_user.id}')
    button2  = types.InlineKeyboardButton("Моя статистика📊", callback_data=f'stat_{message.from_user.id}')
    otvet.add(button1, button2)
    string = message.text
    cursor.execute(f'select * from events where user_id = {message.from_user.id}')
    query = cursor.fetchall()
    if query:
        ans = [i for i in query[0]][2:]
        try:
            int(string)
        except ValueError:
            bot.send_message(message.chat.id, random.choice(bred))
            return None
        if len(string) >= 2 and len(string) <= 4 and all(
                map(lambda x: int(x) >= 1 and int(x) <= 5, string)) and string == ''.join(
                sorted([str(i) for i in string])) and len(set(string)) == len(string):
            if message.text == ans[0]:
                bot.send_message(message.chat.id, 'Верно', reply_markup=otvet)
                cursor.execute('UPDATE users '
                               'SET total_tasks = total_tasks + 1, '
                               '    correct_tasks = correct_tasks + 1, '
                               '    rating = rating + 1 '
                               f'WHERE id = {message.from_user.id};')
                conn.commit()
                cursor.execute(f'DELETE FROM events WHERE user_id = {message.from_user.id}')
                conn.commit()
            else:
                cursor.execute('UPDATE users '
                               'SET total_tasks = total_tasks + 1, '
                               '    rating = rating - 3 '
                               f'WHERE id = {message.from_user.id}; ')
                conn.commit()
                cursor.execute(f'DELETE FROM events WHERE user_id = {message.from_user.id}')
                conn.commit()
                mistake_print = ''
                for i in incorr_words(message.text, ans):
                    mistake_print += f'\n\t{i}'
                    cursor.execute('INSERT INTO problems (user_id, word, mistakes)'
                                  f"VALUES ({message.from_user.id}, '{i}', 1)"
                                   'ON CONFLICT (user_id, word)'
                                   'DO UPDATE SET mistakes = problems.mistakes + 1 '
                                  f"WHERE problems.word = '{i}' AND problems.user_id = {message.from_user.id}")
                    conn.commit()
                bot.send_message(message.chat.id, f'Неверно, правильный ответ {ans[0]}\nошибки в словах:' + mistake_print, reply_markup=otvet)
            for i in corr_words(message.text, ans):
                cursor.execute('UPDATE problems '
                               'SET mistakes = mistakes - 1 '
                              f"WHERE word = '{i}' AND user_id = {message.from_user.id}")
                conn.commit()
            cursor.execute('DELETE FROM problems WHERE mistakes <= 0')
            conn.commit()
        else:
            bot.send_message(message.chat.id, random.choice(bred))



print('поехал')
try:
    bot.infinity_polling(none_stop=True)
except:
    print('фигня')