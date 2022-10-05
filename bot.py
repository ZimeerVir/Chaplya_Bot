import asyncio
import datetime
import random
import glob
import re
import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import cities, code_to_smile, month, open_weather_token, week
from config import help_answer
from handlers import btns_chep, btns_menu, btns_weather
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message) -> None:
    """Начинаем общение бота с команды "/start" """
    write_msg(message) # Запись сообщения пользователя в файл

    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Привет, Чапля! \U0001F44B")
    mark.add(button)

    await bot.send_message(
        message.chat.id, "\U0001F916 Ииии... Камера, мотор, погнали!", reply_markup=mark
    )
    write_msg_bot(message, "\U0001F916 Ииии... Камера, мотор, погнали!")


@dp.message_handler(commands=["weather"])
async def weather(msg: types.Message) -> None:
    """Помощь о погоде (можно удалить)"""
    write_msg(msg) # Запись сообщения пользователя в файл

    await bot.send_message(msg.chat.id, "Введи, падла, свой гребанный город сюда:")

    write_msg_bot(msg, "Введи, падла, свой гребанный город сюда:")


@dp.message_handler()
async def echo_message(msg: types.Message) -> None:
    """Обработка сообщения и выбор ответа"""
    write_msg(msg) # Запись сообщения пользователя в файл

    mess = msg.text.lower()

    if "111" in msg.text:
        await bot.delete_message(msg.chat.id, msg.message_id)
    elif "соси" in mess:
        await bot.delete_message(msg.chat.id, msg.message_id)
        await bot.send_message(msg.chat.id, "\U0001F916 Сам!")
        await asyncio.sleep(5)
        await bot.delete_message(msg.chat.id, msg.message_id + 1)
        msg_bot = "Сам..."
        write_msg_bot(msg, msg_bot)
    elif "привет" in mess:
        mark_menu = btns_menu()
        await bot.send_message(
            msg.chat.id,
            f"Приветствую тебя, {msg.from_user.first_name}. \U0001F44B\n "
            f"Премного благодарен, что ты заглянул ко мне!)\n"
            f"Посмотри на кнопки.",
            reply_markup=mark_menu,
        )
        write_msg_bot(msg,
            f"Приветствую тебя, {msg.from_user.first_name}. \U0001F44B "
            f"Премного благодарен, что ты заглянул ко мне!) "
            f"Посмотри на кнопки."
        )
    elif msg.text == "Погода \U00002600":
        mark_weather = btns_weather()
        await bot.send_message(
            msg.chat.id, "Выбери город, чтобы узрить!", reply_markup=mark_weather
        )
        write_msg_bot(msg, "Выбери город, чтобы узрить!")
    elif msg.text == "Чепухи \U0001F921":
        mark_menu = btns_menu()
        mark_chep = btns_chep()
        await bot.send_message(
            msg.chat.id, "Есть ссылочки для тебя!", reply_markup=mark_chep
        )
        await bot.send_message(msg.chat.id, "Хорошего дня)", reply_markup=mark_menu)
        msg_bot = "Есть ссылочки для тебя! Хорошего дня)"
        write_msg_bot(msg, "Есть ссылочки для тебя! Хорошего дня)")
    elif msg.text == "Мааася!) \U00002764":
        await images_masya(msg)
    elif msg.text == "Таймер \U0000231B":
        await bot.send_message(msg.from_user.id,
        'Чтобы поставить таймер, просто скажите мне "Поставь таймер на _ "')
        write_msg_bot(msg, 'Чтобы поставить таймер, просто скажите мне "Поставь таймер на _ "')
    elif msg.text == "Помощь \U0001F4AC":
        mark_menu = btns_menu()
        await bot.send_message(msg.from_user.id, help_answer, reply_markup=mark_menu)
        write_msg_bot(msg, help_answer)
    elif msg.text == "Запретка \U0001F64A":
        mark_menu = btns_menu()
        await bot.send_message(msg.from_user.id,
        "Я культурный бот, поэтому попрошу не выражаться)", reply_markup=mark_menu)
        write_msg_bot(msg, "Я культурный бот, поэтому попрошу не выражаться)")
    elif "Поставь таймер на" in msg.text:
        await timer_10(msg)
    elif msg.text in cities:
        await data_weather(cities[msg.text], msg)
    elif msg.text == "Назад \U0001F519":
        mark_menu = btns_menu()
        await bot.send_message(msg.from_user.id, "Жду указаний", reply_markup=mark_menu)
        write_msg_bot(msg, "Жду указаний")
    else:
        mark_menu = btns_menu()
        await bot.send_message(msg.chat.id,
        "\U0001F916 Error: Ой! Давай не неси фигни!", reply_markup=mark_menu
        )
        write_msg_bot(msg, "\U0001F916 Error: Ой! Давай не неси фигни!")


async def data_weather(city: str, msg: types.Message) -> None:
    """Подключение к сервису погоды и обработка ответа"""
    request = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&appid={open_weather_token}&units=metric")
    data = request.json()
    await date_now(data, msg)
    await weather_now(data, msg)
    write_msg_bot(msg, request)


async def date_now(data: dict, msg: types.Message) -> None:
    """Работа со временем для раздела погоды"""
    tim = datetime.datetime.fromtimestamp(data["dt"])
    time_clock = tim.strftime("\n%H:%M:%S")
    date = (
        tim.strftime("%d") + " " + month[tim.strftime("%B")] + " " + tim.strftime("%Y"))
    day_week = week[tim.strftime("%A")]
    await bot.send_message(msg.from_user.id, data["name"])
    await bot.send_message(msg.from_user.id, f"{time_clock}\n{day_week}\n{date}")
    write_msg_bot(msg, f'{data["name"]} {time_clock} {day_week} {date}')


async def weather_now(data: dict, msg: types.Message) -> None:
    """Составление основного ответа о погоде"""
    mark_menu = btns_menu()

    weather_data = data["weather"][0]["main"]
    if weather_data in code_to_smile:
        weather_smile = code_to_smile[weather_data]
    else:
        weather_smile = "Посмотри в окно! А то чет не пойму, что там за погода!"
    write_msg_bot(msg, weather_smile)
    sun = datetime.datetime.fromtimestamp(
        data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

    await bot.send_message(
        msg.from_user.id,
        f"Погода: {weather_smile}\n"
        f'Температура: {data["main"]["temp"]}°C\n'
        f'Температура сегодня: {data["main"]["temp_min"]} - {data["main"]["temp_max"]}°C\n'
        f'Ветер: {data["wind"]["speed"]} м/с\n'
        f'Влажность: {round(data["main"]["pressure"]/1.33, 2)} мм.рт.ст\n\n'
        f"Время дня:\n"
        f'Восход: {datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")}\n'
        f'Закат: {datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")}\n'
        f"Продолжительность светового дня: {sun}",
        reply_markup=mark_menu)

    write_msg_bot(msg,
        f"Погода: {weather_smile}"
        f'Температура: {data["main"]["temp"]}°C'
        f'Температура сегодня: {data["main"]["temp_min"]} - {data["main"]["temp_max"]}°C'
        f'Ветер: {data["wind"]["speed"]} м/с'
        f'Влажность: {round(data["main"]["pressure"]/1.33, 2)} мм.рт.ст'
        f"Время дня:"
        f'Восход: {datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")}'
        f'Закат: {datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")}'
        f"Продолжительность светового дня: {sun}")


async def images_masya(msg: types.Message) -> None:
    """Выбор рандомной картинки и ее отправка"""
    mark_menu = btns_menu()
    images = glob.glob("./images/*")
    img = random.choice(images)
    await bot.send_photo(msg.chat.id, photo=open(img, "rb"), reply_markup=mark_menu)
    write_msg_bot(msg, "*** Фото Марсена! ***")


def write_msg(msg: types.Message) -> None:
    """Запись в файл сообщений User"""
    file = open(f"./Messeges/Msg {msg.from_user.first_name}", "a", encoding="UTF-8")
    file.write(f"{msg.date.date()}: "
    f"{msg.from_user.first_name} ({datetime.datetime.now().strftime('%H:%M:%S')}) - {msg.text}\n")
    file.close()


def write_msg_bot(msg: types.Message, msg_bot: str) -> None:
    """Запись в файл ответов бота"""
    file = open(f"./Messeges/Msg {msg.from_user.first_name}", "a", encoding="UTF-8")
    file.write(f"{msg.date.date()}: "
    f"Chaplya_Bot ({datetime.datetime.now().strftime('%H:%M:%S')}) - {msg_bot}\n")
    file.close()


async def timer_10(msg: types.Message) -> None:
    """(Разработка таймера)"""
    try:
        time_user_list = re.findall(r"\d+", msg.text)
        time_user_int = int(time_user_list[0])

        await bot.send_message(msg.from_user.id, f"Пошел отсчет {time_user_int} сек.")
        write_msg_bot(msg, f"Пошел отсчет {time_user_int} сек.")

        await asyncio.sleep(time_user_int)
        await bot.send_message(msg.from_user.id, 'Время вышло!')
        write_msg_bot(msg, "Время вышло!")
    except IndexError:
        await bot.send_message(msg.from_user.id, 'Я не понял, насколько ставить таймер')


if __name__ == "__main__":
    # Я не понимаю (нужна хелп)
    executor.start_polling(dp)
 