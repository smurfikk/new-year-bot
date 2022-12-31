from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup


def main_menu(user_id=0):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    return markup


def back(call_data):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="⬅️ Назад", callback_data=call_data),
    )
    return markup
