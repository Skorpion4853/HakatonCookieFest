
SERVER = 'mysql-ru-br2.joinserver.xyz'
DATABASE = 's252266_Hakaton'
USERNAME = 'u252266_UemnEZfUmO'
PASSWORD = 'Nn7EANEQ+M79lCxI=wgzR5Ya'

import mysql.connector
from faker import Faker
from random import randint, choice


cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD,
                              host=SERVER,
                              database=DATABASE)

cursor = cnx.cursor()
#cursor.execute("DROP TABLE Operations")
#cursor.execute("DROP TABLE Users")
query = ('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY AUTO_INCREMENT,
full_name NVARCHAR(200) NOT NULL,
login NVARCHAR(100) NOT NULL UNIQUE,
password NVARCHAR(100) NOT NULL,
filial NVARCHAR(10) NOT NULL,
access BOOL NOT NULL
)
''')
cursor.execute(query)


fake = Faker()

filial_options = ["Филиал 1", "Филиал 2", "Филиал 3", "Филиал 4"]

data_user = (
    ("Ivan Ivanovich", "admin", "admin", choice(filial_options), 1),
    ("Anatoliy Anatolivich", 'user', 'user', choice(filial_options), 0),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1)),
    (fake.name(), fake.user_name(), fake.password(), choice(filial_options), randint(0, 1))
    )


add_user = ('INSERT INTO Users' 
            '(full_name, login, password, filial, access)' 
            'VALUES (%s, %s, %s, %s, %s)')
for user in data_user:
    cursor.execute(add_user, user)


cursor.execute('SELECT * FROM Users')
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