import asyncio
import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from keyboards import main_menu, admin_menu
from functions import user_func, admin_func
from filters import *
from states import *


@dp.message_handler(IsAdmin(), commands=['admin'], state='*')
async def handler_admin_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("<b>Меню админа</b>", reply_markup=admin_menu.main_menu)


@dp.callback_query_handler(state='*', regexp=r"^admin_menu$")
async def handler_call_admin_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<b>Меню админа</b>", reply_markup=admin_menu.main_menu)


@dp.callback_query_handler(state='*', regexp=r"^admin_stats$")
async def handler_call_admin_stats(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    text = admin_func.admin_stats()
    if call.message.html_text not in text:
        await call.message.edit_text(text, reply_markup=admin_menu.main_menu)


@dp.callback_query_handler(state='*', regexp=r"^admin_mail$")
async def handler_call_admin_mail(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await Email.message_id.set()
    await call.message.edit_text("Отправьте сообщение для рассылки (текст, фото, видео или гиф)",
                                 reply_markup=main_menu.back("admin_menu"))


@dp.message_handler(IsAdmin(), state=Email.message_id, content_types=['text', 'photo', 'video', 'gif', 'animation'])
async def handler_admin_mail_message_id(message: types.Message, state: FSMContext):
    message_id = message.message_id
    await state.update_data(message_id=message_id)
    await Email.next()
    await bot.copy_message(message.from_user.id, message.from_user.id, message_id)
    await message.answer("Отправьте + для подтверждения")


@dp.message_handler(state=Email.confirm)
async def handler_admin_mail_confirm(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            message_id = data['message_id']
        await state.finish()
        asyncio.create_task(send_email(message, message_id))
    else:
        await state.finish()
        await message.answer("Рассылка отменена")


async def send_email(message, message_id):
    users = user_func.all_users()
    await message.answer(f"Рассылка началась\nВсего пользователей: {len(users)}")
    time_start = time.time()
    true_send = 0
    for user_id, in users:
        try:
            await bot.copy_message(user_id, message.from_user.id, message_id)
            true_send += 1
            await asyncio.sleep(0.05)
        except:
            pass
    text = f"""
✅ Рассылка окончена
👍 Отправлено: {true_send}
👎 Не отправлено: {len(users) - true_send}
🕐 Время выполнения: {int(time.time() - time_start)} секунд
"""
    await message.answer(text)

