import logging
from aiogram import Dispatcher
from data.config import ADMINS

# Loggingni sozlash
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")
            logging.info(f"Xabar yuborildi: {admin}")
        except Exception as err:
            logging.exception(f"Xatolik yuz berdi adminga xabar yuborishda: {admin}")
