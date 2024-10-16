from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import keyboards.client_kb
from config import admin_id
from data_base import sqlite_db
from keyboards.client_kb import kb_client, category_kb, keyboard_cart, keyboard_cart_cancel
from create_bot import bot


class FSMClient(StatesGroup):
    link = State()


async def cancel_handler1(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отменено', reply_markup=keyboard_cart)


# функция отправки сообщения на вызов команды /start
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здравствуйте, вы используете бота небольшого магазина с запчастями, '
                                                 'нажимайте кнопки для перемещения по боту. Доставка осуществляется '
                                                 'только в города России и СНГ Почтой России.',
                           reply_markup=kb_client)

# функция отправки сообщения на вызов команды /help
async def help_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Тестовый текст')


async def contacts(message: types.Message):
    await bot.send_message(message.from_user.id, 'Телеграмм владельца: --- \n\nТелеграмм создателя: ---')


async def catalog(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите категорию товаров', reply_markup=category_kb)


async def products(read, message):
    if read:
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[1], f'{ret[2]}\nОписание: {ret[3]}\nЦена: {ret[4]} рублей'
                                                               f'\nОсталось: {ret[5]}',
                                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='+',
                                                                                              callback_data=f"cart_"
                                                                                                            f"adding "
                                                                                                            f"{ret[0]}"
                                                                                              ),
                                                                         (InlineKeyboardButton(text='-',
                                                                                               callback_data=f'cart_'
                                                                                                             f'deleting'
                                                                                                             f'{ret[0]}'
                                                                                               ))))
        await bot.send_message(message.from_user.id, 'Нажимайте + и - для добавления и удаления товаров из корзины',
                               reply_markup=keyboards.client_kb.keyboard_contact)
    else:
        await bot.send_message(message.from_user.id, 'В этой категории нет товаров')


async def repair_phone(message: types.Message):
    read = await sqlite_db.sql_read_category(var="Платы от телефонов")
    await products(read, message)


async def chargers(message: types.Message):
    read = await sqlite_db.sql_read_category(var="Блоки питания")
    await products(read, message)


async def tv_repair(message: types.Message):
    read = await sqlite_db.sql_read_category(var="Запчасти от телевизоров")
    await products(read, message)


async def cart_adding(callback: types.CallbackQuery):
    read = await sqlite_db.sql_read_product_id(callback.data.replace('cart_adding ', ''))
    for ret in read:
        if int(ret[5]) > 0:
            await sqlite_db.cart_adding_sql(callback.message.chat.id, ret[0], ret[2], ret[4])
            await callback.answer(f'Товар добавлен в корзину, товара осталось:{int(ret[5]) - 1}')
        else:
            await callback.answer('Товар закончился', show_alert=True)


async def cart_deleting(callback: types.CallbackQuery):
    read = await sqlite_db.cart_product_checking(callback.data.replace('cart_deleting', ''))
    read1 = await sqlite_db.sql_read_product_id(callback.data.replace('cart_deleting', ''))
    if read:
        for ret in read1:
            await sqlite_db.cart_deleting_sql(callback.data.replace('cart_deleting', ''))
            await callback.answer(f'Товар удален из корзины, товара осталось: {int(ret[5]) + 1}')
    else:
        await callback.answer('У вас нет этого товара в корзине', show_alert=True)


async def catalog_return(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=kb_client)


async def cart(message: types.Message):
    read = await sqlite_db.cart_checking(message.from_user.id)
    count = 0
    if read:
        await bot.send_message(message.from_user.id, 'У вас в корзине:', reply_markup=keyboards.client_kb.keyboard_cart)
        for ret in read:
            await bot.send_message(message.from_user.id, f'{ret[3]}\n'
                                                         f'Цена: {ret[4]} руб.',
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Удалить из '
                                                                                                     'корзины',
                                                                                                callback_data=
                                                                                                f'cart_deleting'
                                                                                                f'{ret[2]}')))
            count += int(ret[4])
        await bot.send_message(message.from_user.id, f'Общая стоимость заказа: {count} рублей',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Оформить',
                                                                                            callback_data='order_buy')))
    else:
        await bot.send_message(message.from_user.id, 'Ваша корзина пуста')


async def category_return(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы вернулись к категориям', reply_markup=category_kb)


async def order_accepting(callback: types.CallbackQuery):
    await FSMClient.link.set()
    await callback.message.answer('Пожалуйста введите ссылку на ваш профиль',
                                  reply_markup=keyboard_cart_cancel)
    await callback.answer()


async def link_confirming(message: types.Message, state=FSMContext):
    read = await sqlite_db.cart_checking(message.from_user.id)
    count = 0
    data = message.text
    await bot.send_message(admin_id, f'Ссылка на заказчика: {data}')
    for ret in read:
        await bot.send_message(admin_id, f'Код товара:{ret[2]}\n'
                                         f'Название товара:{ret[3]}\nЦена:{ret[4]} руб.')
        count += int(ret[4])
    await bot.send_message(admin_id, f'Общая цена заказа: {count} руб.')
    await state.finish()
    await sqlite_db.cart_clear_after_offer(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Спасибо за оформление заказа, продавец скоро с вами свяжется',
                           reply_markup=kb_client)


def message_handlers_register(dp: Dispatcher):

