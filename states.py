from aiogram.dispatcher.filters.state import State, StatesGroup


class Email(StatesGroup):
    message_id = State()
    confirm = State()