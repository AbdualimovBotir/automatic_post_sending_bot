from loader import bot
from config import CHANNEL_IDS, POST_INTERVAL
import asyncio

async def send_auto_posts():
    while True:
        for channel_id in CHANNEL_IDS:
            try:
                await bot.send_message(channel_id, "Bu avtomatik xabar.")
                print(f"Xabar {channel_id} kanal/guruhga yuborildi.")
            except Exception as e:
                print(f"{channel_id} kanal/guruhga xabar yuborishda xatolik: {e}")
        await asyncio.sleep(POST_INTERVAL)  # POST_INTERVAL soniyada qayta yuborish
