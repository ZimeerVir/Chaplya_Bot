import datetime
import time

import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

from config import open_weather_token, cities, week, month, code_to_smile
from head import btns_menu, btns_weather, btns_chep


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Привет, Чапля! \U0001F44B')
    mark.add(button)
    await bot.send_message(message.chat.id, f'\U0001F916 Ииии... Камера, мотор, погнали!', reply_markup=mark)


@dp.message_handler(commands=['weather'])
async def weather(msg: types.Message):
    await bot.send_message(msg.chat.id, 'Введи, падла, свой гребанный город сюда:')


@dp.message_handler()
async def echo_message(msg: types.Message):
    mess = msg.text.lower()
    if '111' in msg.text:
        await bot.delete_message(msg.chat.id, msg.message_id)
    elif 'соси' in mess:
        await bot.delete_message(msg.chat.id, msg.message_id)
        await bot.send_message(msg.chat.id, '\U0001F916 Сам соси!')
        time.sleep(5)
        await bot.delete_message(msg.chat.id, msg.message_id + 1)
    elif (msg.text == 'Привет, Чапля! \U0001F44B'):
        mark_menu = btns_menu()
        await bot.send_message(msg.chat.id, f'Приветствую тебя, {msg.from_user.first_name}. \U0001F44B\n '
                                            f'Премного благодарен, что ты заглянул ко мне!)\n'
                                            f'Посмотри на кнопки.', reply_markup=mark_menu)
    elif (msg.text == 'Погода \U00002600'):
        mark_weather = btns_weather()
        await bot.send_message(msg.chat.id, f'Выбери город, чтобы узрить!', reply_markup=mark_weather)

    elif 'Чепухи' in msg.text:
        mark_menu = btns_menu()
        mark_chep = btns_chep()

        await bot.send_message(msg.chat.id, 'Есть ссылочки для тебя!', reply_markup=mark_chep)
        await bot.send_message(msg.chat.id, 'Хорошего дня)', reply_markup=mark_menu)
    elif msg.text in cities:
        await data_weather(cities[msg.text], msg)
    else:
        await bot.send_message(msg.chat.id, '\U0001F916 Error: Ой! Давай не неси фигни!')


async def data_weather(city, msg):
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")
    data = r.json()

    await bot.send_message(msg.from_user.id, f'{r} \n')
    await date_now(data, msg)
    await weather_now(data, msg)


async def date_now(data, msg):
    tim = datetime.datetime.fromtimestamp(data['dt'])
    time = tim.strftime('\n%H:%M:%S')
    date = tim.strftime("%d") + ' ' + month[tim.strftime("%B")] + ' ' + tim.strftime("%Y")
    day_week = week[tim.strftime("%A")]

    await bot.send_message(msg.from_user.id, data['name'])
    await bot.send_message(msg.from_user.id, f'{time}\n{day_week}\n{date}')


async def weather_now(data, msg):
    # Хуйня ебанная, не буду так больше делать.(Про то, как было раньше) А вот солнце хз, как надо было
    mark_menu = btns_menu()

    weather = data["weather"][0]["main"]
    if weather in code_to_smile:
        weather_smile = code_to_smile[weather]
    else:
        weather_smile = ("Посмотри в окно! А то чет не пойму, что там за погода!")

    sun = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
        data["sys"]["sunrise"])

    await bot.send_message(msg.from_user.id,f'Погода: {weather_smile}\n'
          f'Температура: {data["main"]["temp"]}°C\n'
          f'Температура сегодня: {data["main"]["temp_min"]} - {data["main"]["temp_max"]}°C\n'
          f'Ветер: {data["wind"]["speed"]} м/с\n'
          f'Влажность: {round(data["main"]["pressure"]/1.33, 2)} мм.рт.ст\n\n'
          f'Время дня:\n'
          f'Восход: {datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")}\n'
          f'Закат: {datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")}\n'
          f'Продолжительность светового дня: {sun}', reply_markup=mark_menu)


if __name__ == '__main__':
    executor.start_polling(dp)

