import random
from fnmatch import fnmatch
import emoji



from nado import data

vowels = ['а', 'о', 'у', 'э', 'ы', 'я', 'ё', 'ю', 'е', 'и']

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

def correct_udar(word):
    for i in data:
        if word.lower() == i.lower():
            return i



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

def incorr_words(usr_answer, answer):
    res = set(usr_answer+answer[0]) #общее множество
    res = res - set(set(answer[0]) & set(usr_answer)) #общее - пересечение
    return [correct_udar(answer[int(i)]) for i in res]

s = [1, 2, 3, 4, 5, 6]
print(s[1:])
print(*range(1,6))




