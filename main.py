import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import logging
import os
from dotenv import load_dotenv
import json
import time

# .env faylini yuklash
load_dotenv()

# Bot token va kanal identifikatorlarini .env faylidan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_IDS = os.getenv("CHANNEL_IDS").split(',')
POST_INTERVAL = int(os.getenv("POST_INTERVAL", 60))  # Default intervalni son sifatida olish

logging.basicConfig(level=logging.INFO)

# Botni yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Faylni yuborish funksiyasi
async def send_post_to_channels(media=None, post_text=None, post_type=None):
    for channel_id in CHANNEL_IDS:
        try:
            if post_type == 'photo':
                # Rasm yuborish, post text bilan
                await bot.send_photo(channel_id, media, caption=post_text)
            elif post_type == 'video':
                # Video yuborish, post text bilan
                await bot.send_video(channel_id, media, caption=post_text)
            elif post_type == 'audio':
                # Audio yuborish, post text bilan
                await bot.send_audio(channel_id, media, caption=post_text)
            elif post_type == 'document':
                # Fayl yuborish, post text bilan
                await bot.send_document(channel_id, media, caption=post_text)
            elif post_type == 'text':
                # Faqat matn yuborish
                await bot.send_message(channel_id, post_text)
            print(f"Message sent to channel {channel_id}")
        except Exception as e:
            print(f"Error sending message to channel {channel_id}: {e}")

# Yuborilgan postlar ro'yxatini saqlash
def save_sent_posts(sent_posts):
    with open('sent_posts.json', 'w') as f:
        json.dump(sent_posts, f)

# Yuborilgan postlar ro'yxatini olish
def load_sent_posts():
    if os.path.exists('sent_posts.json'):
        with open('sent_posts.json', 'r') as f:
            return json.load(f)
    return []

# Rasmni qabul qilish va yuborish
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo_message(message: types.Message):
    # Rasmni olish
    photo = message.photo[-1].file_id  # Yuqori sifatdagi rasmni tanlang
    post_text = message.caption  # Rasm tagidagi matnni olish
    sent_posts = load_sent_posts()

    post_info = {
        'media': photo,
        'post_text': post_text,
        'post_type': 'photo',
        'timestamp': time.time(),  # Yuborilgan vaqti
        'interval': POST_INTERVAL  # Yuborish intervali (default)
    }
    sent_posts.append(post_info)
    save_sent_posts(sent_posts)

    await send_post_to_channels(photo, post_text, post_type='photo')

# Video qabul qilish va yuborish
@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video_message(message: types.Message):
    # Video faylni olish
    video = message.video.file_id
    post_text = message.caption  # Video tagidagi matnni olish
    sent_posts = load_sent_posts()

    post_info = {
        'media': video,
        'post_text': post_text,
        'post_type': 'video',
        'timestamp': time.time(),  # Yuborilgan vaqti
        'interval': POST_INTERVAL  # Yuborish intervali (default)
    }
    sent_posts.append(post_info)
    save_sent_posts(sent_posts)

    await send_post_to_channels(video, post_text, post_type='video')

# Faqat matn yuborish
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text_message(message: types.Message):
    post_text = message.text  # Faqat matnni olish
    sent_posts = load_sent_posts()

    post_info = {
        'media': None,
        'post_text': post_text,
        'post_type': 'text',
        'timestamp': time.time(),  # Yuborilgan vaqti
        'interval': POST_INTERVAL  # Yuborish intervali (default)
    }
    sent_posts.append(post_info)
    save_sent_posts(sent_posts)

    await send_post_to_channels(post_text=post_text, post_type='text')

# Faylni yuborish
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document_message(message: types.Message):
    document = message.document.file_id
    post_text = message.caption  # Fayl tagidagi matnni olish
    sent_posts = load_sent_posts()

    post_info = {
        'media': document,
        'post_text': post_text,
        'post_type': 'document',
        'timestamp': time.time(),  # Yuborilgan vaqti
        'interval': POST_INTERVAL  # Yuborish intervali (default)
    }
    sent_posts.append(post_info)
    save_sent_posts(sent_posts)

    await send_post_to_channels(document, post_text, post_type='document')

# Avtomatik post yuborish uchun
async def resend_post():
    sent_posts = load_sent_posts()
    current_time = time.time()

    for post in sent_posts:
        time_diff = current_time - post['timestamp']
        if time_diff >= post['interval']:
            # Postni qayta yuborish
            await send_post_to_channels(post['media'], post['post_text'], post_type=post['post_type'])
            post['timestamp'] = current_time  # So'nggi yuborilgan vaqti yangilash

    # Yangi ro'yxatni saqlash
    save_sent_posts(sent_posts)

# Avtomatik qayta yuborish uchun
async def resend_posts_periodically():
    while True:
        await resend_post()
        await asyncio.sleep(60)  # Har 60 soniyada qayta tekshirish

# Start qilish va pollingni boshlash
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Bot ishlayapti. Rasm, video, matn yoki fayl yuboring.")
    # Avtomatik qayta yuborish uchun ishlashni boshlash
    asyncio.create_task(resend_posts_periodically())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
