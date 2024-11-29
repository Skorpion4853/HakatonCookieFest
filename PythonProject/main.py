import mysql.connector
import asyncio
import settings
from telebot.async_telebot import AsyncTeleBot
from telebot import types

bot = AsyncTeleBot(settings.bot_token)

cnx = mysql.connector.connect(user = settings.USERNAME,
                              password = settings.PASSWORD,
                              host= settings.SERVER,
                              database = settings.DATABASE)
cursor = cnx.cursor()
sqlQuery = ("SELECT id FROM Users "
            "WHERE login = 'dcooper' AND password = '$gBa*Caq6Q' ")

cursor.execute(sqlQuery)






@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Привет!\nЯ-ботинок\nТы авторизован как работник\nВыбери действие'
    marup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Рейтинги', callback_data='rtngs')
    btn2 = types.InlineKeyboardButton(text='Профиль', callback_data='prfl')
    marup.add(btn1, btn2)
    await bot.send_message(message.chat.id, text, reply_markup = marup)


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



asyncio.run(bot.polling())




