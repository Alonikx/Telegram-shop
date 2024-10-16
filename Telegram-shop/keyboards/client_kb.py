# клавиатура
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton('ℹ️ О магазине')
b2 = KeyboardButton('🛍️ Каталог')
b3 = KeyboardButton('📔 Контакты')
b4 = KeyboardButton('🛒 Корзина')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True).add(b2).add(b1).add(b3).add(b4)

# клавиатура категорий
cat_b1 = KeyboardButton('💻 Матрицы для ноутбуков')
cat_b2 = KeyboardButton('⚡ Блоки питания')
cat_b3 = KeyboardButton('📱 Платы от телефонов')
cat_b4 = KeyboardButton('📺 Запчасти от телевизоров')
cat_b5 = KeyboardButton('↩️ Вернуться в меню')

category_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(cat_b4).add(cat_b3).add(cat_b2). \
    add(cat_b5)

# клавиатура покупок
keyboard_contact = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_contact.add(KeyboardButton('🛒 Корзина'))
keyboard_contact.add(KeyboardButton('↩️ Вернуться к категориям'))

# клавиатура корзины
keyboard_cart = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cart.add(KeyboardButton('↩️ Вернуться к категориям'))
keyboard_cart.add(KeyboardButton('↩️ Вернуться в меню'))

keyboard_cart_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cart_cancel.add(KeyboardButton('❌ Отмена'))


keyboard_menu_cart = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_menu_cart.add(KeyboardButton('↩️ Вернуться в меню'))
