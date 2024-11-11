import random
from fnmatch import fnmatch




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


def random_udar(word):
    if word.split(' (')[0] == word:
        wordv = word.split(') ')[1]
        words = word.split(') ')[0] + ') '
    else:
        wordv = word.split(' (')[0]
        words = '(' + word.split(' (')[1]
    print(words)
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

    return words + word_udar


print(random_udar('прИбыли (на место)'))
print(random_udar('(ему) завИдно'))
print(random_udar('красАвчик'))

