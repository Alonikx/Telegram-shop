import asyncio

from aiogram import Bot, Dispatcher, types
from config import bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# присваивание токена боту и указание обработчика обновлений

loop = asyncio.get_event_loop()
bot = Bot(bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, loop=loop, storage=storage)



