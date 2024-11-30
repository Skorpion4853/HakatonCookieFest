import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot import asyncio_filters
from telebot.states.sync.context import StateContext
from DabaseCommand import auth
from Config import get_token


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
    text = 'Привет!\nЯ - чат-бот по мотивации вашей работы!\nПожалуйста, введите ваш логин и пароль через двоеточие\nНапрмер: ivanov:12345'
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
    else:
        await bot.send_message(message.chat.id, f"Неправильный логин или пароль!!")
    await bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)

#Main Menu
@bot.message_handler(content_types=['text'], state=loginState.authorizated)
async def MainMenu(message):
    adm = 0
    if adm == 1:  #надо брать из БД, но пока заглушка
        username = 'Иванов Иван Иваныч'
        text = f'Привет, {username}\nВыбери действие'
        mkup = types.InlineKeyboardMarkup()
        rngs_btn = types.InlineKeyboardButton(text='Рейтинги', callback_data='ratings')
        dwnld_btn = types.InlineKeyboardButton(text='Выгрузить БД', callback_data='downloadDB')
        mng_btn = types.InlineKeyboardButton(text='Управление сотрудниками', callback_data='Manage')
        mkup.Add(rngs_btn, dwnld_btn, mng_btn)
        await bot.send_message(message.chat.id, text, reply_markup=mkup)
    elif adm == 0:  #надо брать из БД, но пока заглушка
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
    if callback.data == 'ratings':
        mkup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Назад', callback_data='back')
        mkup.add(btn1)
        await bot.edit_message_text('Рейтинги пока не доступны',callback.message.chat.id, callback.message.id, reply_markup = mkup)
    elif callback.data == 'back':
        username = 'Иванов Иван Иваныч'
        text = f'Привет, {username}\nВыбери действие'
        marup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Рейтинги', callback_data='ratings')
        btn2 = types.InlineKeyboardButton(text='Профиль', callback_data='profile')
        marup.add(btn1, btn2)
        await bot.edit_message_text(text, callback.message.chat.id, callback.message.id, reply_markup=marup)


#Запуск бота
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
from telebot.states.asyncio.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))
print("bot is active")
asyncio.run(bot.polling())
