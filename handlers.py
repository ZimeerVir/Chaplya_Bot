from aiogram import types


def btns_menu():
    """Объявление кнопок для основного меню"""
    mark_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_weather = types.KeyboardButton("Погода \U00002600")
    btn_help = types.KeyboardButton("Помощь \U0001F4AC")
    btn_chep = types.KeyboardButton("Чепухи \U0001F921")
    btn_ban = types.KeyboardButton("Запретка \U0001F64A")
    btn_img = types.KeyboardButton("Мааася!) \U00002764")
    btn_timer = types.KeyboardButton("Таймер \U0000231B")
    mark_menu.add(btn_weather)
    mark_menu.add(btn_chep)
    mark_menu.add(btn_img)
    mark_menu.add(btn_timer)
    mark_menu.add(btn_help, btn_ban)
    return mark_menu


def btns_weather():
    """Объявление кнопок для выбора города в погоде"""
    mark_weather = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_moscow = types.KeyboardButton("Москва")
    btn_zelenograd = types.KeyboardButton("Зеленоград")
    btn_saratov = types.KeyboardButton("Саратов")
    btn_balakovo = types.KeyboardButton("Балаково")
    btn_volsk = types.KeyboardButton("Вольск")
    btn_cancel = types.KeyboardButton("Назад \U0001F519")
    mark_weather.add(btn_moscow)
    mark_weather.add(btn_zelenograd)
    mark_weather.add(btn_saratov)
    mark_weather.add(btn_balakovo)
    mark_weather.add(btn_volsk)
    mark_weather.add(btn_cancel)
    return mark_weather


def btns_chep():
    """Компоновка ссылок-кнопок для раздела 'Чепухи'"""
    mark_chep = types.InlineKeyboardMarkup()
    btn_chep_1 = types.InlineKeyboardButton("Первый чепух!", url="https://vk.com/elkinay")
    btn_chep_2 = types.InlineKeyboardButton("Второй чепух!", url="https://vk.com/zimeervir")
    btn_chep_3 = types.InlineKeyboardButton("Третий чепух!", url="https://vk.com/id299453853")
    mark_chep.add(btn_chep_1)
    mark_chep.add(btn_chep_2, btn_chep_3)
    return mark_chep
