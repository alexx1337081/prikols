from random import choice

import telebot
import datetime
import emoji
from nado import data, bred, good_stickers, bad_stickers
import random
import psycopg2
from telebot import types
token='7868964757:AAEN8BRIyF6CJHOKT1ywAr424zFlW68NY6M'
vowels = ['а', 'о', 'у', 'э', 'ы', 'я', 'ё', 'ю', 'е', 'и']
bot=telebot.TeleBot(token)
conn = psycopg2.connect(dbname='udar', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()

def current_udar(word):
    for i, let in enumerate(word):
        if let == let.upper():
            return i


@bot.message_handler(commands=['replist'])
def replist(message):
    cursor.execute('SELECT word, variants FROM easy_words')
    easy_words = cursor.fetchall()
    if not easy_words:
        bot.send_message(message.chat.id, 'пусто')
        return None
    easy_words = ''.join([f'{word[:int(udar)].lower() + word[int(udar):].capitalize()}\n' for word, udar in easy_words])
    bot.send_message(message.chat.id, easy_words)
    print(datetime.datetime.now(),message.from_user.id,message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
          message.text)


@bot.message_handler(commands=['udar'])
def check_udar(message):
    bot.send_message(message.chat.id, correct_udar(message.text.split('udar ')[1]))
    print(datetime.datetime.now(),message.from_user.id,message.from_user.username, '-', message.from_user.first_name, message.from_user.last_name, ": ",
          message.text)


@bot.message_handler(commands=['rep'])
def report(message):
    print(datetime.datetime.now(), message.from_user.id, message.from_user.username, '-', message.from_user.first_name,
          message.from_user.last_name, ": ",
          message.text)
    rep_index = message.text.split('rep ')[1]
    try:
        int(rep_index)
    except:
        bot.send_message(message.from_user.id, 'ошибка ввода')
        return None
    cursor.execute(f'SELECT word{rep_index} FROM events WHERE user_id = {message.from_user.id}')
    query = cursor.fetchall()
    if not query:
        bot.send_message(message.from_user.id, 'у вас нет задания пока')
        return None
    word = query[0][0]
    if word == correct_udar(word):
        bot.send_message(message.from_user.id, 'это правильное слово дурак')
        return None
    cursor.execute('INSERT INTO easy_words(word, variants) '
                  f"VALUES('{correct_udar(word)}', '{current_udar(word)}')"
                   'ON CONFLICT (word)'
                   f'''DO UPDATE SET variants = CONCAT(easy_words.variants, '{current_udar(word)}')''')
    bot.send_message(message.from_user.id, 'добавил')
    conn.commit()



def is_emoji(s):
    return s in emoji.UNICODE_EMOJI


def correct_udar(word):
    for i in data:
        if word.lower() == i.lower():
            return i
    print('АААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА', word)
    return 'Произошла ошибка скиньте скрин сане'


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    click = call.data.split('_')[0]
    user_id = call.data.split('_')[1]
    if call.message:
        if click == "check":
            if user_id != '1131169121' and user_id != '1237189946':
                cursor.execute('select word from problems '
                               f'where user_id = {user_id} and mistakes = (select max(mistakes) from problems where user_id = {user_id})')
                pwords = cursor.fetchall()
            else:
                pwords = []
            cursor.execute('SELECT word, variants FROM easy_words')
            easy_words = dict(cursor.fetchall())
            if not pwords:
                words = random.sample(data, 5)
            else:
                words = random.sample(data, 4)
                while len(words) < 5:
                    pword = random.choice(pwords)[0]
                    if pword.lower() not in [i.lower() for i in words]:
                        words.append(pword)
                random.shuffle(words)
            words_easy = []
            for word in words:
                try:
                    words_easy.append((word, easy_words[word]))
                except KeyError:
                    words_easy.append((word, None))
            task = []
            ncorr = random.randint(2, 4)
            ans = []
            for i, word in enumerate(words_easy):
                if ncorr != 0:
                    task.append((word[0], 1))
                    ncorr -= 1
                    continue
                task.append((random_udar(word[0], word[1]), 0))
            random.shuffle(task)
            ans.append(''.join([str(i + 1) for i in range(len(task)) if task[i][1]]))
            ans.extend([i[0] for i in task])
            bot.send_message(user_id, f'Где правильно ударение стоит?\n'
                                              f'1) {task[0][0].replace('ё', 'е')}\n'
                                              f'2) {task[1][0].replace('ё', 'е')}\n'
                                              f'3) {task[2][0].replace('ё', 'е')}\n'
                                              f'4) {task[3][0].replace('ё', 'е')}\n'
                                              f'5) {task[4][0].replace('ё', 'е')}')
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
            print(datetime.datetime.now(), user_id, ": ", "stat")
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
            if query[0][2] != 0:
                bot.send_message(user_id, f'Всего решено заданий: {query[0][2]}\n'
                                                  f'Ваш винрейт: {round(query[0][3] / query[0][2] * 100, 1)}%\n'
                                                  f'Ваш рейтинг: {query[0][4]}\n'+
                                                  pozor, reply_markup=otvet)
            else:
                bot.send_message(user_id, f'Всего решено заданий: {query[0][2]}\n'
                                          f'Ваш винрейт: 0%\n'
                                          f'Ваш рейтинг: {query[0][4]}\n' +
                                 pozor, reply_markup=otvet)
            if (query[0][4] < -20 or query[0][4]>100) and random.randint(1, 5) == 1:
                bot.send_sticker(user_id, 'CAACAgIAAxkBAAENhvRni5gowxQt69PCJa_Ee0EThagJgwAC0FQAAgIhGEteqE-U3SzeJTYE')
                print('сколько нафиг')



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


def random_udar(word, easy_udars):
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
    if easy_udars != None:
        for i in easy_udars:
            print(word, i)
            incorr_udars.remove(int(i))
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
                if random.randint(1, 3) == 1:
                    bot.send_sticker(message.chat.id, random.choice(good_stickers))
                bot.send_message(message.chat.id, 'Верно', reply_markup=otvet)
                print(datetime.datetime.now(), message.from_user.username, '-', message.from_user.first_name,
                      message.from_user.last_name, ": ",
                      message.text, "✅")
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
                if random.randint(1, 3) == 1:
                    bot.send_sticker(message.chat.id, random.choice(bad_stickers))
                bot.send_message(message.chat.id, f'Неверно, правильный ответ {ans[0]}\nошибки в словах:' + mistake_print, reply_markup=otvet)
                print(datetime.datetime.now(), message.from_user.username, '-', message.from_user.first_name,
                      message.from_user.last_name, ": ",
                      message.text, "❌")
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

bot.infinity_polling(timeout=10, long_polling_timeout = 5)
