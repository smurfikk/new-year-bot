import random

from aiogram.types import Message, ChatType
from aiogram.dispatcher import FSMContext

from middlewares.throttling import rate_limit
from loader import dp, bot
from functions import open_ai_func
import texts

counter = 0


@dp.message_handler(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP], regexp=r"^\..+$", state='*')
async def handler_msg_start_with_dot(message: Message, state: FSMContext):
    text = message.text
    if text.startswith("."):
        await enter_queue(message.chat.id, text[1:].strip(), message.message_id)


@rate_limit(0)
@dp.message_handler(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP], state='*')
async def handler_msg(message: Message, state: FSMContext):
    global counter
    counter += 1
    if counter >= 15 or random.randint(0, 7) == 1:
        text = message.text
        if len(text) < 1000:
            await enter_queue(message.chat.id, text, message.message_id)
            counter = 0


async def enter_queue(user_id, text, message_id):
    open_ai_func.queue.append([user_id, text, message_id, 0])
    if not open_ai_func.working:
        await open_ai_func.activate_queue()
