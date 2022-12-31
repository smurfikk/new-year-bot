from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(
    InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
    InlineKeyboardButton(text="🗣 Рассылка", callback_data="admin_mail"),
)

