import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config


# создание объектов бота и диспетчера
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop, storage=storage)

