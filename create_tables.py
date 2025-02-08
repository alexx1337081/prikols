import psycopg2
conn = psycopg2.connect(dbname='udar', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()

# cursor.execute('CREATE TABLE users('
#                'id text PRIMARY KEY,'
#                'name VARCHAR(40),'
#                'total_tasks int,'
#                'correct_tasks int,'
#                'rating int)')

#cursor.execute('CREATE TABLE problems('
#               'id serial PRIMARY KEY,'
#               'user_id bigint REFERENCES users(id),'
#               'word varchar(40),'
#               'mistakes int,'
#               'UNIQUE (user_id, word))')

# cursor.execute('CREATE TABLE events('
#                'id serial PRIMARY KEY, '
#                'user_id bigint REFERENCES users(id) unique,'
#                'ans text,'
#                'word1 varchar(40),'
#                'word2 varchar(40),'
#                'word3 varchar(40),'
#                'word4 varchar(40),'
#                'word5 varchar(40))')


#cursor.execute('CREATE TABLE easy_words('
#               'id serial PRIMARY KEY,'
#               'word text,'
#               'variants text,'
#               'UNIQUE (word))')

# cursor.execute('CREATE TABLE admin_sessions('
#                'id serial PRIMARY KEY,'
#                'user_id text,'
#                'question int,'
#                'UNIQUE (word))')

# cursor.execute('CREATE TABLE test2('
#                'id serial PRIMARY KEY,'
#                'sname text,'
#                'class text,'
#                'result1 int,'
#                'result2 int)')

conn.commit()