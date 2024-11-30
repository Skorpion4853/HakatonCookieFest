import asyncio
from telebot.async_telebot import AsyncTeleBot
import os
from telebot import types
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot import asyncio_filters
from telebot.states.sync.context import StateContext
from DabaseCommand import auth
from Config import get_token

from DabaseCommand import get_worker_top, return_worker_top

from telebot.callback_data import CallbackData, CallbackDataFilter


#Объяление бота
bot = AsyncTeleBot(get_token() ,state_storage=StateMemoryStorage())

#Подключение к SQL-серверу
#sql = mysql.connector.connect(user = sngs.USERNAME,
                             # password = sngs.PASSWORD,
                              #host= sngs.SERVER,
                              #database = sngs.DATABASE)
#cursor = sql.cursor()

class loginState(StatesGroup):
    login = State()
    password = State()
    authorizated = State()

def check_login(login, password):
    return True

'''async def send_welcome(message):
    text = 'Привет!\nЯ-ботинок\nТы авторизован как работник\nВыбери действие'
    marup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Рейтинги', callback_data='rtngs')
    btn2 = types.InlineKeyboardButton(text='Профиль', callback_data='prfl')
    marup.add(btn1, btn2)
    await bot.send_message(message.chat.id, text, reply_markup = marup)'''


#Реакция бота на команду /start
@bot.message_handler(commands=['start'])
async def start(message, state: StateContext):
    text = 'Привет!\nЯ - чат-бот по мотивации вашей работы!\nПожалуйста авторизайтесь: введите свой логин и пароль разными сообщениями.'
    await bot.send_message(message.chat.id, text)
    await bot.set_state(user_id=message.from_user.id, state=loginState.login,
                          chat_id=message.chat.id)

# Здесь пользователь вводит логин свой
@bot.message_handler(state=loginState.login)
async def login_state(message, state: StateContext):
    #Устанавливаем стейт
    await state.add_data(login=message.text)

    await bot.send_message(message.chat.id, "Введите пароль")

    await bot.set_state(user_id=message.from_user.id, state=loginState.password,
                          chat_id=message.chat.id)

# Здесь пользователь вводит свой пароль
@bot.message_handler(state=loginState.password)
async def password_state(message, state: StateContext):
    await state.add_data(password=message.text)
    async with state.data() as data:
        login = data.get("login")
        password = data.get("password")
    status = auth(login=login, password=password)
    if status != None:
        await bot.send_message(message.chat.id, f"Вы успешно зашли под логином: {login}")
        await bot.set_state(user_id=message.from_user.id, state=loginState.authorizated,
                          chat_id=message.chat.id)
        #Устанавливаем права пользователю
        await state.add_data(permission=status)

        #Перемещение на главное меню.
        await MainMenu(message, state)
    else:
        await bot.send_message(message.chat.id, f"Неправильный логин или пароль!!")
    await bot.delete_message(message.chat.id, message.id)

#Main Menu
@bot.message_handler(state=loginState.authorizated)
async def MainMenu(message, state: StateContext):
    async with state.data() as data:
        adm = data.get('permission')
    if adm == 1:
        username = 'Иванов Иван Иваныч'     #надо брать из БД, но пока заглушка
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup(row_width=1)
        rngs_btn = types.InlineKeyboardButton(text='Рейтинги \U0001F4C8', callback_data='ratings')
        dwnld_btn = types.InlineKeyboardButton(text='Выгрузить БД \U0001F4E5', callback_data='downloadDB')
        mng_btn = types.InlineKeyboardButton(text='Управление сотрудниками \U0001F9FE', callback_data='Manage')
        mkup.add(rngs_btn, dwnld_btn, mng_btn)
        try: await bot.edit_message_text(text, message.chat.id, message.id, reply_markup=mkup)
        except: await bot.send_message(message.chat.id, text, reply_markup=mkup)
    elif adm == 0:
        username = 'Иванов Иван Иваныч'     #надо брать из БД, но пока заглушка
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup(row_width=1)
        rngs_btn = types.InlineKeyboardButton(text = 'Рейтинги \U0001F4C8', callback_data='ratings')
        prfl_btn = types.InlineKeyboardButton(text = 'Профиль \U0000274C', callback_data='profile')
        mkup.add(rngs_btn,prfl_btn)
        try:
            await bot.edit_message_text(text, message.chat.id, message.id, reply_markup=mkup)
        except:
            await bot.send_message(message.chat.id, text, reply_markup=mkup)


@bot.callback_query_handler(lambda c: c.data == 'ratings') #Рейтинг
async def employee_rating(callback_query: types.CallbackQuery):
    mkup = types.InlineKeyboardMarkup(row_width=1)
    glb_rtngs_btn = types.InlineKeyboardButton(text='Глобальный \U0001F5FA', callback_data='global rating')
    brnch_rtngs_btn = types.InlineKeyboardButton(text='Филиалов \U0001F3D8', callback_data='branches rating')
    lcl_rtngs_btn = types.InlineKeyboardButton(text='Вашего филилала \U0001F3E0', callback_data='local rating')
    bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToMenu')
    mkup.add(glb_rtngs_btn, brnch_rtngs_btn, lcl_rtngs_btn, bck_btn)
    await bot.edit_message_text('Выберите рейтинг \U0001F4C8', callback_query.message.chat.id, callback_query.message.id,
                                reply_markup=mkup)


@bot.callback_query_handler(lambda c: c.data == 'global rating') #Глобальный рейтинг по сэллари
async def global_rating(callback_query: types.CallbackQuery, state: StateContext):
    async with state.data() as data:
        login = data.get("login")
    mkup = types.InlineKeyboardMarkup(row_width=1)
    glb_rtngs_btn = types.InlineKeyboardButton(text='Salary', callback_data='global rating')
    brnch_rtngs_btn = types.InlineKeyboardButton(text='Price', callback_data='global rating_p')
    bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToMenu')
    mkup.add(glb_rtngs_btn, brnch_rtngs_btn, bck_btn)
    await bot.edit_message_text(f'{get_worker_top(login, "salary")}', callback_query.message.chat.id, callback_query.message.id,
                                reply_markup=mkup)

@bot.callback_query_handler(lambda c: c.data == 'global rating_p') #Глобальный рейтинг по прайсу
async def global_rating_p(callback_query: types.CallbackQuery, state: StateContext):
    async with state.data() as data:
        login = data.get("login")
    mkup = types.InlineKeyboardMarkup(row_width=1)
    glb_rtngs_btn = types.InlineKeyboardButton(text='Salary', callback_data='global rating')
    brnch_rtngs_btn = types.InlineKeyboardButton(text='Price', callback_data='global rating_p')
    bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToMenu')
    mkup.add(glb_rtngs_btn, brnch_rtngs_btn, bck_btn)
    await bot.edit_message_text(f'{get_worker_top(login, "price")}', callback_query.message.chat.id, callback_query.message.id,
                                reply_markup=mkup)

#Профиль
@bot.callback_query_handler(lambda c: c.data == 'profile')
async def employee_profile(callback: types.CallbackQuery):
    text = 'Данная функция пока в разработке \U0001F634'
    mkup = types.InlineKeyboardMarkup()
    bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToMenu')
    mkup.add(bck_btn)
    await bot.delete_message(callback.message.chat.id, callback.message.id)
    await bot.send_message(callback.message.chat.id, text, reply_markup=mkup)

#Возврат в меню
@bot.callback_query_handler(lambda c: c.data == "BackToMenu")
async def back_menu(callback: types.CallbackQuery, state: StateContext):
    await MainMenu(callback.message, state)

#Скачать БД
@bot.callback_query_handler(lambda c: c.data == 'downloadDB')
async def download_DB(callback: types.CallbackQuery):
    text = 'Выберите формат файла'
    mkup = types.InlineKeyboardMarkup(row_width=1)
    xlsx_btn = types.InlineKeyboardButton(text='Exel .xlsx', callback_data='dwnldXLSX')
    json_btn = types.InlineKeyboardButton(text='JavaScript Object Notation .json', callback_data='dwnldJSON')
    csv_btn = types.InlineKeyboardButton(text='Comma-Separated Values .csv', callback_data='dwnldCSV')
    bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToMenu')
    mkup.add(xlsx_btn, json_btn, csv_btn, bck_btn)
    await bot.delete_message(callback.message.chat.id, callback.message.id)
    await bot.send_message(callback.message.chat.id, text, reply_markup=mkup)

#Выгрузка CSV из базы
@bot.callback_query_handler(lambda c: c.data == "dwnldCSV")
async def downloadcsv(callback: types.CallbackQuery, state: StateContext):
    async with state.data() as data:
        login = data.get("login")
    df = return_worker_top(login, 'salary')
    df2 = return_worker_top(login, 'price')
    file_path = f"files/{login}_salary.csv"
    file_path2 = f"files/{login}_price.csv"
    df.to_csv(file_path)
    df2.to_csv(file_path2)
    with open(file_path, 'rb') as file:
        await bot.send_document(callback.message.chat.id, file)
    with open(file_path2, 'rb') as file:
        await bot.send_document(callback.message.chat.id, file)
    os.remove(file_path)
    os.remove(file_path2)
    await MainMenu(callback.message, state)

#Управление сотрудниками
@bot.callback_query_handler(lambda c:c.data == 'Manage')
async def manage_employees(callback: types.CallbackQuery):
    text = 'Выберите действие'
    mkup = types.InlineKeyboardMarkup(row_width=1)
    add_btn = types.InlineKeyboardButton(text='Добавить сотрудника \U00002714', callback_data='addEmployee')
    del_btn = types.InlineKeyboardButton(text='Удалить сотрудника \U0000274C', callback_data='delEmployee')
    bck_btn = types.InlineKeyboardButton(text='Назад', callback_data='BackToMenu')
    mkup.add(add_btn, del_btn, bck_btn)
    await bot.edit_message_text(text, callback.message.chat.id, callback.message.id, reply_markup=mkup)


#Запуск бота
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
from telebot.states.asyncio.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))
print("bot is active")
asyncio.run(bot.polling())
