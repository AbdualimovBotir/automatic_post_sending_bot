import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv('D:/django_project/Kanallar-bilan-ishlash/.env')

# O'zgaruvchilarni yuklash
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_IDS = os.getenv("CHANNEL_IDS").split(',')
POST_INTERVAL = int(os.getenv("POST_INTERVAL"))

# Kanal ID-larni int ga aylantirish
CHANNEL_IDS = [int(channel_id.strip()) for channel_id in CHANNEL_IDS]
