
SERVER = 'mysql-ru-br2.joinserver.xyz'
DATABASE = 's252266_Hakaton'
USERNAME = 'u252266_UemnEZfUmO'
PASSWORD = 'Nn7EANEQ+M79lCxI=wgzR5Ya'

import mysql.connector
from random import randint, choice


cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD,
                              host=SERVER,
                              database=DATABASE)

cursor = cnx.cursor()
#cursor.execute("DROP TABLE Operations")
query = (
'''
CREATE TABLE IF NOT EXISTS Operations (
id INTEGER PRIMARY KEY AUTO_INCREMENT,
worker_id INTEGER NOT NULL,
type_op INTEGER NOT NULL,
price_op INTEGER NOT NULL,
FOREIGN KEY (worker_id) REFERENCES Users (id)
)
'''
)
cursor.execute(query)



data_user = (
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1,15), randint(1, 3), randint(1000, 100001)),
    (randint(1,15), randint(1, 3), randint(1000, 100001)),
    (randint(1,15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1,15), randint(1, 3), randint(1000, 100001)),
    (randint(1,15), randint(1, 3), randint(1000, 100001)),
    (randint(1,15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
    (randint(1, 15), randint(1, 3), randint(1000, 100001)),
)


add_user = ('INSERT INTO Operations' 
            '(worker_id, type_op, price_op)' 
            'VALUES (%s, %s, %s)')
for user in data_user:
    cursor.execute(add_user, user)


cursor.execute('SELECT * FROM Operations')
users = cursor.fetchall()
i = 0



# Выводим результаты
for user in users:
    for elem in user:
        print(elem, end=" ")
    print()

cnx.commit()
cursor.close()
cnx.close()