from datetime import datetime
import sqlite3
import pytz
import asyncio
from aiogram.types import InlineKeyboardMarkup

import config
from loader import bot


def connect():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    return conn, cursor


def get_date():
    date = datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)
    return date


def str_to_date(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f%z')


# code from https://t.me/bez_domnyi


async def send_all_admins(text, markup=InlineKeyboardMarkup()):
    for chat_id in config.admin_id:
        try:
            await bot.send_message(chat_id, text, reply_markup=markup)
            await asyncio.sleep(0.1)
        except:
            pass
