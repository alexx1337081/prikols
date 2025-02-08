#import random
#import tqdm
#result = []
#for _ in tqdm.tqdm(range(100000000)):
#    a = [random.randint(1, 366) for i in range(24)]
#    result.append(23-len(set(a)))
#dups = [i for i in result if i > 0]
#print(f'{round((len(dups)/len(result))*100, 4)}%')

import psycopg2
conn = psycopg2.connect(dbname='udar_results', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()
cursor.execute('SELECT * FROM results')
query = cursor.fetchall()
test1 = [[i[4], i[2], i[5], i[6]] for i in query if i[1] == 1]
test2 = [[i[4], i[2], i[5], i[6]] for i in query if i[1] == 2]
test1.sort()
test2.sort()
for i in test1:
    cursor.execute(f"INSERT INTO test1(sname, class, result1, result2) VALUES('{i[0]}', '{i[1]}', {i[2]}, {i[3]})")
    conn.commit()
for i in test2:
    cursor.execute(f"INSERT INTO test2(sname, class, result1, result2) VALUES('{i[0]}', '{i[1]}', {i[2]}, {i[3]})")
    conn.commit()


