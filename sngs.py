#Файл с основными настройками/запросами к SQL

#Токен бота
bot_token = '7942815705:AAHTbNcFA6MfoKjF6F3SXtj5HZnDBSDE8HY'


#Данные от SQL-сервера
SERVER = 'mysql-ru-br2.joinserver.xyz'
DATABASE = 's252266_Hakaton'
USERNAME = 'u252266_UemnEZfUmO'
PASSWORD = 'Nn7EANEQ+M79lCxI=wgzR5Ya'
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

#Основные SQL-запросы для удобства
userID = -1;
login = ''
password = ''
sqlAuth = f'SELECT * FROM Users Where login = {login} AND password = {password}' #Авторизация




