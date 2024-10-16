import logging
from aiogram.utils import executor

from config import admin_id
from create_bot import dp, bot
from data_base import sqlite_db
from handlers.client import message_handlers_register
from handlers.admin import admin_handlers_register

# описание запуска бота
logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    await bot.send_message(admin_id, 'bot running')
    sqlite_db.sql_start()


if __name__ == '__main__':
    message_handlers_register(dp)
    admin_handlers_register(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
