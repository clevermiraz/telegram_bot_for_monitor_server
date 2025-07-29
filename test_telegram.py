# test_telegram.py

import asyncio
import os

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

print("Using token:", token)
print("Using chat ID:", chat_id)


async def send_test_message():
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text="✅ Test message to your main Telegram account")
    print("✅ Message sent successfully")


if __name__ == "__main__":
    asyncio.run(send_test_message())
