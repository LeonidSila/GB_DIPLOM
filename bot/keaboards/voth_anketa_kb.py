from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
# kb_ok = KeyboardButton(text='OK')
from aiogram.utils.keyboard import ReplyKeyboardBuilder


kb_vibor_anketa_poisk = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text = '🧡'), types.KeyboardButton(text = '👎🏻'), types.KeyboardButton(text = '💤')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выбирай из преложенных',
    selective=True

)

kb_vibor_anketa_time = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text = 'Более чем'), types.KeyboardButton(text = 'НЕТ')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выбирай из преложенных',
    selective=True

)