from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config

# Bot ob'ektini yaratish
bot = Bot(token=config.BOT_TOKEN)

# Bot holatini saqlash uchun xotira ombori
storage = MemoryStorage()

# Dispatcher yaratish
dp = Dispatcher(bot, storage=storage)
