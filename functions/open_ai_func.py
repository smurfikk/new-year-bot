import logging
import traceback

import openai
import asyncio

import config
from functions.func import *
from loader import bot
from aiogram.utils.exceptions import BotBlocked
from functions.caching import caching

queue = []
working = False

openai.api_key = config.ai_api_key
model_engine = "text-davinci-003"


async def enter_queue(user_id, text, message_id, message_id_delete):
    queue.append([user_id, text, message_id, message_id_delete])
    if not working:
        asyncio.create_task(activate_queue())
    return len(queue)


async def activate_queue():
    global working, queue
    working = True
    while queue:
        user_id, prompt, message_id, message_id_delete = queue[0]
        queue.remove([user_id, prompt, message_id, message_id_delete])
        try:
            image = False
            if prompt.startswith((".img", "img")):
                image = True
                prompt = prompt[4:].strip()
            elif prompt.startswith("."):
                prompt = prompt[1:].strip()
            if len(prompt) == 0:
                continue
            response = get_response(prompt, image)
            conn, cursor = connect()
            cursor.execute("INSERT INTO messages (date_send, from_user, input_text, output_text) VALUES (?, ?, ?, ?)",
                           [get_date(), user_id, prompt, response])
            conn.commit()
            conn.close()
            try:
                if image:
                    await bot.send_photo(user_id, response, caption=prompt, reply_to_message_id=message_id,
                                         parse_mode=None)
                else:
                    await bot.send_message(user_id, response, reply_to_message_id=message_id, parse_mode=None)
            except BotBlocked:
                pass
            try:
                await bot.delete_message(user_id, message_id_delete)
            except:
                pass
        except Exception:
            logging.error(f"Ошибка получения ответа\n{traceback.format_exc()}")
    working = False


@caching(15 * 60)
def get_response(prompt: str, image: bool):
    if image:
        completion_image = openai.Image.create(prompt=prompt)
        return completion_image.data[0].url
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return completion.choices[0].text
