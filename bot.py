import requests
import datetime
import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

from config import open_weather_token, cities, week, month, code_to_smile

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Привет, Чапля! \U0001F44B')
    mark.add(button)
    await bot.send_message(message.chat.id, f'\U0001F916 Ииии... Камера, мотор, погнали!', reply_markup=mark)

@dp.message_handler(commands=['weather'])
async def weather(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Введи, падла, свой гребанный город сюда:')
'''
async def btns_menu():
    mark_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_weather = types.KeyboardButton('Погода \U00002600')
    btn_help = types.KeyboardButton('Помощь \U0001F4AC')
    btn_chep = types.KeyboardButton('Чепухи \U0001F921')
    btn_ban = types.KeyboardButton('Погода \U0001F64A')
    mark_menu.add(btn_weather)
    mark_menu.add(btn_chep)
    mark_menu.add(btn_help, btn_ban)
    return mark_menu
'''
@dp.message_handler()
async def echo_message(msg: types.Message):

    flag = False

    if '111' in msg.text:
        await bot.delete_message(msg.chat.id, msg.message_id)
    elif 'соси' in msg.text:
        await bot.delete_message(msg.chat.id, msg.message_id)
        await bot.send_message(msg.chat.id, '\U0001F916 Сам соси!')
        time.sleep(5)
        await bot.delete_message(msg.chat.id, msg.message_id + 1)
    elif 'Соси' in msg.text:
        await bot.delete_message(msg.chat.id, msg.message_id)
        await bot.send_message(msg.chat.id, '\U0001F916 Сам соси!')
        time.sleep(5)
        await bot.delete_message(msg.chat.id, msg.message_id + 1)
    elif (msg.text == 'Привет, Чапля! \U0001F44B'):
        mark_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_weather = types.KeyboardButton('Погода \U00002600')
        btn_help = types.KeyboardButton('Помощь \U0001F4AC')
        btn_chep = types.KeyboardButton('Чепухи \U0001F921')
        btn_ban = types.KeyboardButton('Запретка \U0001F64A')
        mark_menu.add(btn_weather)
        mark_menu.add(btn_chep)
        mark_menu.add(btn_help, btn_ban)
        await bot.send_message(msg.chat.id, f'Приветствую тебя, {msg.from_user.first_name}. \U0001F44B\n '
                                            f'Премного благодарен, что ты заглянул ко мне!)\n'
                                            f'Посмотри на кнопки.', reply_markup=mark_menu)
    elif (msg.text == 'Погода \U00002600'):
        mark_weather = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_moscow = types.KeyboardButton('Москва')
        btn_zelenograd = types.KeyboardButton('Зеленоград')
        btn_saratov = types.KeyboardButton('Саратов')
        btn_balakovo = types.KeyboardButton('Балаково')
        btn_volsk = types.KeyboardButton('Вольск')
        mark_weather.add(btn_moscow)
        mark_weather.add(btn_zelenograd)
        mark_weather.add(btn_saratov)
        mark_weather.add(btn_balakovo)
        mark_weather.add(btn_volsk)
        await bot.send_message(msg.chat.id, f'Выбери город, чтобы узрить!', reply_markup=mark_weather)
    elif 'Чепухи' in msg.text:
        mark_chep = types.InlineKeyboardMarkup()
        btn_chep_1 = types.InlineKeyboardButton('Первый чепух!', url='https://vk.com/elkinay')
        btn_chep_2 = types.InlineKeyboardButton('Второй чепух!', url='https://vk.com/zimeervir')
        btn_chep_3 = types.InlineKeyboardButton('Третий чепух!', url='https://vk.com/id299453853')
        mark_chep.add(btn_chep_1)
        mark_chep.add(btn_chep_2, btn_chep_3)

        mark_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_menu = types.KeyboardButton('На главную')
        mark_menu.add(btn_menu)

        await bot.send_message(msg.chat.id, 'Есть ссылочки для тебя!', reply_markup=mark_chep)
        await bot.send_message(msg.chat.id, reply_markup=mark_menu)
    elif msg.text in cities:
        await data_weather(cities[msg.text], msg)
    elif (msg.text == 'На главную'):
        mark_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_weather = types.KeyboardButton('Погода \U00002600')
        btn_help = types.KeyboardButton('Помощь \U0001F4AC')
        btn_chep = types.KeyboardButton('Чепухи \U0001F921')
        btn_ban = types.KeyboardButton('Запретка \U0001F64A')
        mark_menu.add(btn_weather)
        mark_menu.add(btn_chep)
        mark_menu.add(btn_help, btn_ban)
        await bot.send_message(msg.chat.id, f'Вернулись', reply_markup=mark_menu)
    else:
        await bot.send_message(msg.chat.id, '\U0001F916 Error: Я не понимаю тебя(')

async def data_weather(city, msg):

    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")
    data = r.json()

    await bot.send_message(msg.from_user.id, f'{r} \n')
    await date_now(data, msg)
    await weather_now(data, msg)

async def date_now(data, msg):
    tim = datetime.datetime.fromtimestamp(data['dt'])
    await bot.send_message(msg.from_user.id, data['name'])

    time = tim.strftime('\n%H:%M:%S')

    if tim.strftime('%A') in week:
        day_week = week[tim.strftime("%A")]
    else:
        day_week = 'Пшлнх!'

    if tim.strftime('%B') in month:
        date = tim.strftime("%d") + ' ' + month[tim.strftime("%B")] + ' ' + tim.strftime("%Y")
    else:
        date = 'Пшлнх2!'

    await bot.send_message(msg.from_user.id, f'{time}\n{day_week}\n{date}')

async def weather_now(data, msg):
    # Этот тупой список чисто, чтобы побаловаться
    temp = data['main']["temp"]
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    wind_speed = data['wind']['speed']
    pressure = data['main']['pressure']
    sun = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    # Хуйня ебанная, не буду так больше делать. А вот солнце хз как надо было.

    mark_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_menu = types.KeyboardButton('На главную')
    mark_menu.add(btn_menu)

    weather = data["weather"][0]["main"]
    if weather in code_to_smile:
        weather_smile = code_to_smile[weather]
    else:
        weather_smile = ("Посмотри в окно, не пойму, что там за погода!")

    await bot.send_message(msg.from_user.id,f'Погода: {weather_smile}\n'
          f'Температура: {temp}°C\n'
          f'Температура сегодня: {temp_min} - {temp_max}°C\n'
          f'Ветер: {wind_speed} м/с\n'
          f'Влажность: {round(pressure/1.33, 2)} мм.рт.ст\n\n'
          f'Время дня:\n'
          f'Восход: {datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")}\n'
          f'Закат: {datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")}\n'
          f'Продолжительность светового дня: {sun}', reply_markup=mark_menu)

if __name__ == '__main__':
    executor.start_polling(dp)

