from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from config import dp, bot
from aiogram.utils.keyboard import ReplyKeyboardBuilder



async def kb_client_welcom(user_id):
    await bot.send_message(chat_id=user_id, text="1: Смотреть Анкеты\n2: Редактирование анкеты\n3: Магазин",
                           reply_markup=kb_vibor_memu_main)





kb_vibor_OK = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text ='Okey')]
    ],
    one_time_keyboard=True,
    input_field_placeholder='Окей',
    selective=True

)

kb_vibor_ostavit = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text ='Оставить, что было')]
    ],
    one_time_keyboard=True,
    input_field_placeholder='Окей',
    selective=True

)


kb_vibor_pola = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text ='Парень'), types.KeyboardButton(text ='Девушка')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выбирай давай',
    selective=True

)

kb_vibor_shop = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text ='100 нажатий'), types.KeyboardButton(text ='VIP')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Нажмиите кнопку',
    selective=True

)


kb_vibor_memu_main = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text = '1'), types.KeyboardButton(text = '2'), types.KeyboardButton(text = '3')],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Чего ты хочешь?',
    selective=True

)

answer_change_menu = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text = 'Фото'), types.KeyboardButton(text = 'Описание'), types.KeyboardButton(text = 'Имя'), types.KeyboardButton(text = 'Пол')],
    [types.KeyboardButton(text = 'Возраст'), types.KeyboardButton(text = 'Город'), types.KeyboardButton(text = 'Выйти'), types.KeyboardButton(text = 'Удалить анкету')]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Чего ты хочешь?',
    selective=True

)



kb_vibor_siti_geo = ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text = 'Санкт-Петербург'), types.KeyboardButton(text = 'Москва')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выбери город из предложнных',
    selective=True

)

def profile(text: str | list):
    builder = ReplyKeyboardBuilder()
    if isinstance(text, str):
        text = [text]
    [builder.button(text=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# def profile(text):
#     builder = ReplyKeyboardBuilder()
#     if isinstance(text, str):
#         text = [text]
#     [builder.button(text=txt) for txt in text]
#     return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# buttons = ["Парень", "Девушка"]
# kb_vibor_pola = types.ReplyKeyboardMarkup(resize_keyboard=True)
# buttons = ["Парень", "Девушка"]
# kb_vibor_pola.add(*buttons)