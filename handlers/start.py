from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp, bot
from data.config import CHANNEL_IDS

class Form(StatesGroup):
    waiting_for_channel_id = State()

@dp.message_handler(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Salom! Iltimos, kanal yoki guruh ID-sini yuboring.")
    await Form.waiting_for_channel_id.set()

@dp.message_handler(state=Form.waiting_for_channel_id)
async def save_channel_id(message: types.Message, state: FSMContext):
    channel_id = message.text.strip()
    if channel_id.isdigit():  # ID raqam ekanligini tekshirish
        CHANNEL_IDS.append(channel_id)
        await message.reply(f"Kanal ID {channel_id} muvaffaqiyatli qo'shildi.")
        await state.finish()
    else:
        await message.reply("Kanal yoki guruh ID raqam bo'lishi kerak!")
