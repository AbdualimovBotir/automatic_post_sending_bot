import asyncio
from aiogram import Bot, types
from config import BOT_TOKEN, CHANNEL_IDS, POST_INTERVAL

# Botni yaratish
bot = Bot(token=BOT_TOKEN)

# Postni kanallarga yuborish
async def send_post_to_channels(message):
    for channel_id in CHANNEL_IDS:
        try:
            if isinstance(message, str):  # Agar matn bo'lsa
                await bot.send_message(channel_id, message)
            elif isinstance(message, types.PhotoSize):  # Agar rasm bo'lsa
                await bot.send_photo(channel_id, message)
            elif isinstance(message, types.Video):  # Agar video bo'lsa
                await bot.send_video(channel_id, message)
            elif isinstance(message, types.Audio):  # Agar audio bo'lsa
                await bot.send_audio(channel_id, message)
            else:
                print(f"Unsupported message type to send to channel {channel_id}")
            print(f"Message sent to channel {channel_id}")
        except Exception as e:
            print(f"Error sending message to channel {channel_id}: {e}")

# Avtomatik post yuborish
async def send_auto_posts(message, post_type='text'):
    while True:
        if post_type == 'text':
            await send_post_to_channels(message)
        elif post_type == 'photo':
            # Bu yerda rasm yuborish uchun rasmni yuklab olishingiz yoki file_id ni o'rnatishingiz mumkin
            photo = types.InputFile('path_to_your_image.jpg')  # Misol uchun, faylni berish
            await send_post_to_channels(photo)
        elif post_type == 'video':
            video = types.InputFile('path_to_your_video.mp4')  # Faylni videoni yuborish
            await send_post_to_channels(video)
        await asyncio.sleep(POST_INTERVAL)  # Belgilangan interval bilan yuborish
