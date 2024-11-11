import psycopg2
conn = psycopg2.connect(dbname='udar', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()

cursor.execute('CREATE TABLE users('
               'id bigint PRIMARY KEY,'
               'name VARCHAR(255),'
               'total_tasks int,'
               'correct_tasks int)')

cursor.execute('INSERT INTO users '
               "VALUES (1237189946, 'санёк', 0, 0)")
conn.commit()