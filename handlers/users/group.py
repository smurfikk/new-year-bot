import random

from aiogram.types import Message, ChatType
from aiogram.dispatcher import FSMContext

from middlewares.throttling import rate_limit
from loader import dp, bot
from functions import open_ai_func
import texts

counter = {}


@dp.message_handler(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP], regexp=r"^\..+$", state='*')
async def handler_msg_start_with_dot(message: Message, state: FSMContext):
    text = message.text
    if text.startswith("."):
        await enter_queue(message.chat.id, text, message.message_id)


@rate_limit(0)
@dp.message_handler(chat_type=[ChatType.GROUP, ChatType.SUPERGROUP], state='*')
async def handler_msg(message: Message, state: FSMContext):
    global counter
    _counter = get_counter(message.chat.id)
    if _counter >= 15 or random.randint(0, 10) == 1:
        text = message.text
        if len(text) < 1000:
            await enter_queue(message.chat.id, text, message.message_id)
            counter[message.chat.id] = 0


async def enter_queue(user_id, text, message_id):
    open_ai_func.queue.append([user_id, text, message_id, 0])
    if not open_ai_func.working:
        await open_ai_func.activate_queue()


def get_counter(chat_id: int):
    global counter
    if counter.get(chat_id):
        counter[chat_id] += 1
    else:
        counter[chat_id] = 1
    return counter[chat_id]
