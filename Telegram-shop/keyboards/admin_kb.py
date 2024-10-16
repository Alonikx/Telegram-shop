from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton('Загрузить')
b2 = KeyboardButton('Вернуться')
b3 = KeyboardButton('Отмена')
b4 = KeyboardButton('Редактировать')
b5 = KeyboardButton('Очистить корзину')


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(b1).add(b4).add(b5).add(b2)
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(b3)
