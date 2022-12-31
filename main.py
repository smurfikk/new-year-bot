# - *- coding: utf- 8 - *-
import asyncio

from aiogram import executor

import middlewares
from handlers import dp
from loader import bot, scheduler
from functions import repeat_func


async def scheduler_start():
    await repeat_func.timer_hour()
    scheduler.add_job(repeat_func.timer_hour, "cron", second=0)
    scheduler.start()


async def on_startup(dp):
    middlewares.setup(dp)
    info = await bot.get_me()
    await scheduler_start()
    print(f"~~~~~ Bot @{info.username} was started ~~~~~")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
