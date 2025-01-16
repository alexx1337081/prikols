import psycopg2
conn = psycopg2.connect(dbname='udar', user='alex',
                        password='0209', host='192.168.1.75')
cursor = conn.cursor()
if input('вы уверены? (y/n)') == 'y':
    if input('точно? (y/n)') == 'y':
        cursor.execute('TRUNCATE users CASCADE')
        cursor.execute('TRUNCATE events CASCADE')
        cursor.execute('TRUNCATE problems CASCADE')
        conn.commit()
