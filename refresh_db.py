import psycopg2
conn = psycopg2.connect(dbname='udar', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()

# cursor.execute('CREATE TABLE users('
#                'id bigint PRIMARY KEY,'
#                'name VARCHAR(40),'
#                'total_tasks int,'
#                'correct_tasks int,'
#                'rating int)')

cursor.execute('CREATE TABLE problems('
               'id serial PRIMARY KEY,'
               'user_id bigint REFERENCES users(id),'
               'word varchar(40) unique ,'
               'mistakes int)')



# cursor.execute('INSERT INTO users '
#                "VALUES (1237189946, 'санёк', 0, 0)")
conn.commit()