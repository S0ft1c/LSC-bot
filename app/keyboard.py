from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardButton, InlineKeyboardMarkup)

cmd_start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ввести параметры', callback_data='edit_params')]
])
