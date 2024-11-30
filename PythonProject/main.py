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

#Авторизация (попытка)
'''
@bot.message_handler(content_types=['text'])
async def Auth(message):
'''

@bot.message_handler(content_types=['text'])
async def MainMenu(message):
    adm = 0
    if adm == 1:
        username = 'Иванов Иван Иваныч'
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup()
        rngs_btn = types.InlineKeyboardButton(text='Рейтинги', callback_data='ratings')
        dwnld_btn = types.InlineKeyboardButton(text='Выгрузить БД', callback_data='downloadDB')
        mng_btn = types.InlineKeyboardButton(text='Управление сотрудниками', callback_data='Manage')
        mkup.Add(rngs_btn, dwnld_btn, mng_btn)
        await bot.send_message(message.chat.id, text, reply_markup=mkup)
    elif adm == 0:
        username = 'Иванов Иван Иваныч'
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup()
        rngs_btn = types.InlineKeyboardButton(text = 'Рейтинги', callback_data='ratings')
        prfl_btn = types.InlineKeyboardButton(text = 'Профиль', callback_data='profile')
        mkup.add(rngs_btn,prfl_btn)
        await bot.send_message(message.chat.id, text, reply_markup= mkup)


#Обработка callback ботом
@bot.callback_query_handler(func = lambda callback: callback.data)
async def check_callback_data(callback):
    if callback.data == 'rtngs':
        marup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='назад', callback_data='bck')
        marup.add(btn1)
        await bot.edit_message_text('Рейтинги пока не доступны',callback.message.chat.id, callback.message.id, reply_markup = marup)
    elif callback.data == 'bck':
        text = cursor.fetchall()
        marup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Рейтинги', callback_data='rtngs')
        btn2 = types.InlineKeyboardButton(text='Профиль', callback_data='prfl')
        marup.add(btn1, btn2)
        await bot.edit_message_text(text, callback.message.chat.id, callback.message.id, reply_markup=marup)


#Запуск бота
asyncio.run(bot.polling())




