from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import bot
from data_base import sqlite_db
from data_base.sqlite_db import sql_add_command
from keyboards import admin_kb, client_kb
from config import admin_id


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    quantity = State()
    category = State()


async def moderator(message: types.Message):
    if message.from_user.id == admin_id:
        await bot.send_message(admin_id, 'Готов к работе', reply_markup=admin_kb.kb_admin)
        await message.delete()


async def cm_start(message: types.Message):
    if message.from_user.id == admin_id:
        await FSMAdmin.photo.set()
        await message.reply('Отправь URL фотки товара', reply_markup=admin_kb.cancel_kb)


async def cm_return(message: types.Message):
    if message.from_user.id == admin_id:
        await bot.send_message(admin_id, 'Вы снова в обычном меню', reply_markup=client_kb.kb_client)


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Отменено', reply_markup=admin_kb.kb_admin)


async def load_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['photo'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи название')


async def load_name(message: types.Message, state=FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи краткое описание')


async def load_description(message: types.Message, state=FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи цену')


async def load_price(message: types.Message, state=FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await FSMAdmin.next()
        await message.reply('Введи количество товара')


async def load_quantity(message: types.Message, state=FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['quantity'] = int(message.text)
        await FSMAdmin.next()
        await message.reply('Введи категорию товара')


async def load_category(message: types.Message, state=FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['category'] = message.text
        await sql_add_command(state)
        await sqlite_db.sql_read(message)
        await state.finish()
        await bot.send_message(admin_id, 'Вы загрузили товар', reply_markup=admin_kb.kb_admin)


async def del_callback_run(callback: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback.data.replace('del ', ''))
    await callback.answer(text=f'Вы удалили {callback.data.replace("del ", "")}', show_alert=True)


async def edit_item(message: types.Message):
    if message.from_user.id == admin_id:
        read = await sqlite_db.sql_read_table('catalog')
        if read:
            for ret in read:
                await bot.send_photo(admin_id, ret[1], f'{ret[2]}\nОписание: {ret[3]}\nЦена: {ret[4]} руб.\nОсталось:'
                                                       f' {ret[5]}\nКатегория: {ret[6]}',
                                     reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='+',
                                                                                                  callback_data=f'cart_'
                                                                                                                f'add'
                                                                                                                f'{ret[0]}'
                                                                                                  ),
                                                                             (InlineKeyboardButton(text='-',
                                                                                                   callback_data=f'cart_'
                                                                                                                 f'delete'
                                                                                                                 f'{ret[0]}'
                                                                                                   ))))
                await bot.send_message(admin_id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                                       add(InlineKeyboardButton(f'Удалить {ret[2]}', callback_data=f'del {ret[2]}')))
        else:
            await bot.send_message(admin_id, 'Пусто...')


async def cart_adding_admin(callback: types.CallbackQuery):
    await sqlite_db.quantity_sql_add(callback.data.replace('cart_add', ''))
    read = await sqlite_db.sql_read_product_id(callback.data.replace('cart_add', ''))
    for ret in read:
        await callback.answer(f'Количество товара увеличилось: {int(ret[5])}')


async def cart_deleting_admin(callback: types.CallbackQuery):
    await sqlite_db.quantity_sql_delete(callback.data.replace('cart_delete', ''))
    read = await sqlite_db.sql_read_product_id(callback.data.replace('cart_delete', ''))
    if read:
        for ret in read:
            await callback.answer(f'Количество товара уменьшилось: {int(ret[5])}')
    else:
        await callback.answer(f'Количество товара: 0', show_alert=True)


async def cart_clearing(_):
    read = await sqlite_db.sql_read_table('cart')
    if read:
        for ret in read:
            await sqlite_db.quantity_sql_add(ret[2])
        await sqlite_db.cart_clear()
        await bot.send_message(admin_id, 'Корзина очищена')
    else:
        await bot.send_message(admin_id, 'Корзина пуста')


def admin_handlers_register(dp: Dispatcher):
    dp.register_message_handler(moderator, text='moderator')
    dp.register_message_handler(cm_start, text='Загрузить', state=None)
    dp.register_message_handler(cm_return, text='Вернуться')
    dp.register_message_handler(cancel_handler, state='*', text='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_quantity, state=FSMAdmin.quantity)
    dp.register_message_handler(load_category, state=FSMAdmin.category)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(cart_adding_admin, lambda x: x.data and x.data.startswith('cart_add'))
    dp.register_callback_query_handler(cart_deleting_admin, lambda x: x.data and x.data.startswith('cart_delete'))
    dp.register_message_handler(edit_item, text='Редактировать')
    dp.register_message_handler(cart_clearing, text='Очистить корзину')

