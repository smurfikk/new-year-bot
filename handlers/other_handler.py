import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

import texts
from keyboards import main_menu
from loader import dp


@dp.callback_query_handler(text="...", state='*')
async def handler_call_dot(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)


@dp.callback_query_handler(state='*')
async def handler_call(call: types.CallbackQuery, state: FSMContext):
    state = await state.get_state()
    logging.error(f"Ошибка обработки сообщения\n{state=} {call.data=}")


@dp.message_handler(chat_type="private", state='*')
async def handler_msg(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(texts.start, reply_markup=main_menu.main_menu(message.from_user.id))
