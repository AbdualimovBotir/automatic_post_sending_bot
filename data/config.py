import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = os.getenv("ADMINS", "").split(",")
CHANNEL_IDS = os.getenv("CHANNEL_IDS", "").split(",")
