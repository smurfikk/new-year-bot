import random

from aiogram.types import Message, ChatType
from aiogram.dispatcher import FSMContext

from middlewares.throttling import rate_limit
from loader import dp, bot
from functions import open_ai_func
import texts

counter = 0


@dp.message_handler(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP], regexp=r"сколько.+(нг|нового года)", state='*')
async def handler_msg(message: Message, state: FSMContext):
    await state.finish()
    date = open_ai_func.get_date()
    if date.year == 2022:
        hours = 24 - date.hour
        minutes = 60 - date.minute
        if hours > 0:
            times = f"{hours}ч"
        else:
            times = f"{minutes}мин"
        text = f"<b>До нового года {times}</b>\n\n" \
               f"<i>{texts.congratulations[random.randint(0, 8)]}</i>"
    else:
        text = "Дахуя"
    await message.answer(text)


@rate_limit(0)
@dp.message_handler(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP], state='*')
async def handler_msg(message: Message, state: FSMContext):
    global counter
    counter += 1
    if counter >= 15 or random.randint(0, 10) == 1:
        text = message.text
        if len(text) < 1000:
            await enter_queue(message.chat.id, text, message.message_id)
            counter = 0


async def enter_queue(user_id, text, message_id):
    open_ai_func.queue.append([user_id, text, message_id, 0])
    if not open_ai_func.working:
        await open_ai_func.activate_queue()
