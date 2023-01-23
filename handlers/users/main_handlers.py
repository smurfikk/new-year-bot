import asyncio
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatType

from keyboards import main_menu
from loader import dp, bot
from functions import user_func, open_ai_func
import texts


@dp.message_handler(chat_type="private", commands=['start'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    user_func.first_join(message.from_user.id, message.from_user.username)
    await message.answer(texts.start, reply_markup=main_menu.main_menu(message.from_user.id))


@dp.message_handler(commands=['help'], state='*')
async def handler_help(message: types.Message, state: FSMContext):
    await state.finish()
    chat_type = message.chat.type
    if chat_type != "private":
        chat_type = "group"
    await message.answer(texts.help_text[chat_type], reply_markup=main_menu.main_menu(message.from_user.id))


@dp.message_handler(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE],
                    regexp=r"когда.+(нг|новый год)", state="*")
@dp.message_handler(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE],
                    regexp=r"сколько (до|осталось до).+(нг|нового года)", state="*")
async def handler_new_year(message: types.Message, state: FSMContext):
    await state.finish()
    date = open_ai_func.get_date()
    new_year = date.replace(year=date.year + 1, day=1, month=1, hour=0, minute=0, second=0)
    times = open_ai_func.format_time(int((new_year - date).total_seconds()))
    text = f"<b>До нового года {times}</b>"
    if date.month == 12 and date.day == 31:
        text += f"\n\n<i>{texts.congratulations_all[random.randint(0, 21)]}</i>"
    await message.answer(text)


@dp.message_handler(chat_type="private", state='*')
async def handler_msg(message: types.Message, state: FSMContext):
    await state.finish()
    text = message.text
    if len(text) < 1000:
        msg = await message.reply(f"<b>Сейчас отвечу!</b>")
        await enter_queue(message.from_user.id, text, message.message_id, msg.message_id)
        if len(open_ai_func.queue) > 1:
            await msg.edit_text(f"<b>Сейчас отвечу!</b>\n"
                                f"В очереди {len(open_ai_func.queue)} чел.")
    else:
        await message.answer("Слишком длинное сообщение...")


async def enter_queue(user_id, text, message_id, message_id_delete):
    open_ai_func.queue.append([user_id, text, message_id, message_id_delete])
    if not open_ai_func.working:
        await open_ai_func.activate_queue()
