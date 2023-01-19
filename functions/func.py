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


async def send_all_admins(text, markup=InlineKeyboardMarkup()):
    for chat_id in config.admin_id:
        try:
            await bot.send_message(chat_id, text, reply_markup=markup)
            await asyncio.sleep(0.1)
        except:
            pass


def format_time(all_time: int):
    if all_time == 0:
        return "Сейчас"
    days = all_time // (60 * 60 * 24)
    all_time -= days * (60 * 60 * 24)
    hours = all_time // (60 * 60)
    all_time -= hours * (60 * 60)
    minutes = all_time // 60
    all_time -= hours * 60
    seconds = all_time % 60
    text = []
    if days > 0:
        text.append(f"{days}д")
    if hours > 0:
        text.append(f"{hours}ч")
    if minutes > 0:
        text.append(f"{minutes}мин")
    if seconds > 0:
        text.append(f"{seconds}сек")
    return " ".join(text)
