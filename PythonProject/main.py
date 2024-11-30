#Импорт библиотек
import mysql.connector
import asyncio
import sngs
from telebot.async_telebot import AsyncTeleBot
from telebot import types

#Объяление бота
bot = AsyncTeleBot(sngs.bot_token)

#Подключение к SQL-серверу
sql = mysql.connector.connect(user = sngs.USERNAME,
                              password = sngs.PASSWORD,
                              host= sngs.SERVER,
                              database = sngs.DATABASE)
cursor = sql.cursor()


'''async def send_welcome(message):
    text = 'Привет!\nЯ-ботинок\nТы авторизован как работник\nВыбери действие'
    marup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Рейтинги', callback_data='rtngs')
    btn2 = types.InlineKeyboardButton(text='Профиль', callback_data='prfl')
    marup.add(btn1, btn2)
    await bot.send_message(message.chat.id, text, reply_markup = marup)'''


#Реакция бота на команду /start
@bot.message_handler(commands=['start'])
async def start(message):
    text = 'Привет!\nЯ - чат-бот по мотивации вашей работы!\nПожалуйста, введите ваш логин и пароль через двоеточие\nНапрмер: ivanov:12345'
    await bot.send_message(message.chat.id, text)


#Main Menu
@bot.message_handler(content_types=['text'])
async def MainMenu(message):
    adm = 0
    if adm == 1:    #надо брать из БД, но пока заглушка
        username = 'Иванов Иван Иваныч'     #надо брать из БД, но пока заглушка
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup()
        rngs_btn = types.InlineKeyboardButton(text='Рейтинги', callback_data='ratings')
        dwnld_btn = types.InlineKeyboardButton(text='Выгрузить БД', callback_data='downloadDB')
        mng_btn = types.InlineKeyboardButton(text='Управление сотрудниками', callback_data='Manage')
        mkup.add(rngs_btn, dwnld_btn, mng_btn)
        await bot.send_message(message.chat.id, text, reply_markup=mkup)
    elif adm == 0:      #надо брать из БД, но пока заглушка
        username = 'Иванов Иван Иваныч'     #надо брать из БД, но пока заглушка
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup()
        rngs_btn = types.InlineKeyboardButton(text = 'Рейтинги', callback_data='ratings')
        prfl_btn = types.InlineKeyboardButton(text = 'Профиль', callback_data='profile')
        mkup.add(rngs_btn,prfl_btn)
        await bot.send_message(message.chat.id, text, reply_markup= mkup)


#Обработка callback ботом
@bot.callback_query_handler(func = lambda callback: callback.data)
async def check_callback_data(callback):
    if callback.data == 'ratings': #Выводим раздел рейтинги
        mkup = types.InlineKeyboardMarkup()
        glb_rtngs_btn = types.InlineKeyboardButton(text='Глобальный', callback_data='global rating')
        brnch_rtngs_btn = types.InlineKeyboardButton(text='Филиалов', callback_data='branches rating')
        lcl_rtngs_btn = types.InlineKeyboardButton(text='Вашего филилала', callback_data='local rating')
        bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='back')
        mkup.add(glb_rtngs_btn, brnch_rtngs_btn, lcl_rtngs_btn, bck_btn)
        await bot.edit_message_text('Выберите рейтинг',callback.message.chat.id, callback.message.id , reply_markup = mkup)
    elif callback.data == 'profile': #Выводим раздел профиль
        username = 'Иванов Иван Иваныч'  # Заглушка, брать из БД
        text = f'Профиль\nФИО: {username}'
        mkup = types.InlineKeyboardMarkup()
        bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='back')
        mkup.add((bck_btn))
        await bot.send_message(callback.message.chat.id, text, reply_markup=mkup)
    elif callback.data == 'back': #Возврат к меню работника
        username = 'Иванов Иван Иваныч' #Заглушка, брать из БД
        text = f'Привет, {username}\nВыбери действие'
        marup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Рейтинги', callback_data='ratings')
        btn2 = types.InlineKeyboardButton(text='Профиль', callback_data='profile')
        marup.add(btn1, btn2)
        await bot.edit_message_text(text, callback.message.chat.id, callback.message.id, reply_markup=marup)


#Запуск бота
asyncio.run(bot.polling())




