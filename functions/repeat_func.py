import logging
import random
import time
import traceback

from aiogram import Bot, types

import texts
from functions.user_func import *

import config

bot = Bot(token=config.bot_token, parse_mode=types.ParseMode.HTML)


async def timer_hour():
    date = get_date()
    if date.year == 2022:
        hours = 24 - date.hour
        minutes = 60 - date.minute
        if minutes == 60 or hours == 1:
            if hours > 1:
                await send_email(f"{hours}ч")
            else:
                await send_email(f"{minutes}мин")


async def send_email(times):
    users = all_users()
    time_start = time.time()
    true_send = 0
    for user_id, in users:
        text = f"<b>До нового года {times}</b>\n\n" \
               f"<i>{texts.congratulations[random.randint(0, 8)]}</i>"
        try:
            await bot.send_message(user_id, text)
            true_send += 1
            await asyncio.sleep(0.05)
        except:
            traceback.print_exc()
    text = f"""
✅ Рассылка окончена
👍 Отправлено: {true_send}
👎 Не отправлено: {len(users) - true_send}
🕐 Время выполнения: {int(time.time() - time_start)} секунд
"""
    await send_all_admins(text)
