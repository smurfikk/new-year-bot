import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import main_menu
from loader import dp, bot
from functions import user_func, open_ai_func
import texts


@dp.message_handler(chat_type="private", commands=['start'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await state.finish()
    user_func.first_join(message.from_user.id, message.from_user.username)
    await message.answer(texts.start, reply_markup=main_menu.main_menu(message.from_user.id))


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
