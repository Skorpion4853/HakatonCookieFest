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


#Реакция бота на команду /start
@bot.message_handler(commands=['start'])
async def start(message):
    text = 'Привет!\nЯ - чат-бот по мотивации вашей работы!\nПожалуйста, введите ваш логин и пароль через двоеточие\nНапрмер: ivanov:12345'
    await bot.send_message(message.chat.id, text)


#Main Menu
@bot.message_handler(content_types=['text'])
async def MainMenu(message):
    adm = 1     #надо брать из БД, но пока заглушка
    if adm == 1:    #надо брать из БД, но пока заглушка
        username = 'Иванов Иван Иваныч'     #надо брать из БД, но пока заглушка
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup(row_width=1)
        rngs_btn = types.InlineKeyboardButton(text='Рейтинги', callback_data='ratingsEmployeer')
        dwnld_btn = types.InlineKeyboardButton(text='Выгрузить БД', callback_data='downloadDB')
        mng_btn = types.InlineKeyboardButton(text='Управление сотрудниками', callback_data='Manage')
        mkup.add(rngs_btn, dwnld_btn, mng_btn)
        await bot.send_message(message.chat.id, text, reply_markup=mkup)
    elif adm == 0:      #надо брать из БД, но пока заглушка
        username = 'Иванов Иван Иваныч'     #надо брать из БД, но пока заглушка
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup(row_width=1)
        rngs_btn = types.InlineKeyboardButton(text = 'Рейтинги', callback_data='ratings')
        prfl_btn = types.InlineKeyboardButton(text = 'Профиль', callback_data='profile')
        mkup.add(rngs_btn,prfl_btn)
        await bot.send_message(message.chat.id, text, reply_markup= mkup)


#Обработка callback ботом
@bot.callback_query_handler(func = lambda callback: callback.data)
async def check_callback_data(callback):
    #callback'и работника
    if callback.data == 'ratings': #Выводим раздел рейтинги
        mkup = types.InlineKeyboardMarkup()
        glb_rtngs_btn = types.InlineKeyboardButton(text='Глобальный', callback_data='global rating')
        brnch_rtngs_btn = types.InlineKeyboardButton(text='Филиалов', callback_data='branches rating')
        lcl_rtngs_btn = types.InlineKeyboardButton(text='Вашего филилала', callback_data='local rating')
        bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToEmployeeMenu')
        mkup.add(glb_rtngs_btn, brnch_rtngs_btn, lcl_rtngs_btn, bck_btn)
        await bot.edit_message_text('Выберите рейтинг',callback.message.chat.id, callback.message.id , reply_markup = mkup)
    elif callback.data == 'profile': #Выводим раздел профиль
        username = 'Иванов Иван Иваныч'  # Заглушка, брать из БД
        text = f'Профиль\nФИО: {username}'
        mkup = types.InlineKeyboardMarkup()
        bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToEmployeeMenu')
        mkup.add(bck_btn)
        await bot.delete_message(callback.message.chat.id, callback.message.id)
        await bot.send_message(callback.message.chat.id, text, reply_markup=mkup)
    elif callback.data == 'BackToEmployeeMenu': #Возврат к меню работника
        username = 'Иванов Иван Иваныч' #Заглушка, брать из БД
        text = f'Привет, {username}\nВыбери действие'
        marup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Рейтинги', callback_data='ratings')
        btn2 = types.InlineKeyboardButton(text='Профиль', callback_data='profile')
        marup.add(btn1, btn2)
        await bot.edit_message_text(text, callback.message.chat.id, callback.message.id, reply_markup=marup)
    #callback'и работодателя
    elif callback.data == 'ratingsEmployeer': #Выводим раздел рейтинги
        mkup = types.InlineKeyboardMarkup()
        glb_rtngs_btn = types.InlineKeyboardButton(text='Глобальный', callback_data='global rating')
        brnch_rtngs_btn = types.InlineKeyboardButton(text='Филиалов', callback_data='branches rating')
        lcl_rtngs_btn = types.InlineKeyboardButton(text='Вашего филилала', callback_data='local rating')
        bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToEmployeerMenu')
        mkup.add(glb_rtngs_btn, brnch_rtngs_btn, lcl_rtngs_btn, bck_btn)
        await bot.edit_message_text('Выберите рейтинг',callback.message.chat.id, callback.message.id , reply_markup = mkup)
    elif callback.data == 'BackToEmployeerMenu':
        username = 'Иванов Иван Иваныч'  # надо брать из БД, но пока заглушка
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup(row_width=1)
        rngs_btn = types.InlineKeyboardButton(text='Рейтинги', callback_data='ratingsEmployeer')
        dwnld_btn = types.InlineKeyboardButton(text='Выгрузить БД', callback_data='downloadDB')
        mng_btn = types.InlineKeyboardButton(text='Управление сотрудниками', callback_data='Manage')
        mkup.add(rngs_btn, dwnld_btn, mng_btn)
        await bot.edit_message_text(text, callback.message.chat.id, callback.message.id, reply_markup=mkup)
    elif callback.data == 'downloadDB':
        text = 'Выберите формат файла'
        mkup = types.InlineKeyboardMarkup(row_width=1)
        xlsx_btn = types.InlineKeyboardButton(text='Exel .xlsx', callback_data='dwnldXLSX')
        json_btn = types.InlineKeyboardButton(text='JavaScript Object Notation .json', callback_data='dwnldJSON')
        csv_btn = types.InlineKeyboardButton(text='Comma-Separated Values .csv', callback_data='dwnldCSV')
        bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToEmployeerMenu')
        mkup.add(xlsx_btn, json_btn, csv_btn, bck_btn)
        await bot.delete_message(callback.message.chat.id, callback.message.id)
        await bot.send_message(callback.message.chat.id, text, reply_markup=mkup)
    elif callback.data == 'Manage':
        text = 'Выберите действие'
        mkup = types.InlineKeyboardMarkup(row_width=1)
        add_btn = types.InlineKeyboardButton(text = 'Добавить сотрудника', callback_data='addEmployee')
        del_btn = types.InlineKeyboardButton(text = 'Удалить сотрудника', callback_data='delEmployee')
        bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToEmployeerMenu')
        mkup.add(add_btn, del_btn, bck_btn)
        await bot.delete_message(callback.message.chat.id, callback.message.id)
        await bot.send_message(callback.message.chat.id, text, reply_markup=mkup)
#Запуск бота
asyncio.run(bot.polling())




