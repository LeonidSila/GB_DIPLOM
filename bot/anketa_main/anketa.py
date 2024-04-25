import logging
from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router
from database import data_base as db
from config import dp, bot
from keaboards import client_kb, voth_anketa_kb
from aiogram.fsm.context import FSMContext
from keaboards.client_kb import profile
from aiogram.types import FSInputFile, InputMediaPhoto
from anketa_main import anketa_form
# from geo_map import geo_map_client
List_photo = {}

router_anketa = Router()

class Wait(StatesGroup):
    choosing_gender = State()
    name = State()
    age = State()
    city = State()
    text = State()
    photo = State()
    photo_2 = State()
    photo_3 = State()
    answer_change = State()
    answer_change_2 = State()
    my_anketa_answer = State()
    change_text = State()
    change_photo = State()
    change_photo_2 = State()
    change_photo_3 = State()
    change_name = State()
    change_age = State()
    change_pol = State()
    change_city = State()
    delete_confirm = State()
    anketa_reaction = State()

@router_anketa.message(F.text == 'Okey')
async def choose_gender_in(message: types.Message, state: FSMContext):
    await state.set_state(Wait.choosing_gender)
    await message.answer("Кто ты", reply_markup=profile(["Парень", "Девушка"]))


@router_anketa.message(Wait.choosing_gender, F.text.casefold().in_(["парень", "девушка"]))
async def choose_gender_out(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_username = message.from_user.username
    user_url = message.from_user.username
    db.cursor.execute('SELECT COUNT(*) FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    db.conn.commit()
    if user_count == 0:
        db.cursor.execute('INSERT INTO anketa (id, name, url_user) VALUES (?, ?, ?)', (user_id, user_username, user_url, ))
        db.conn.commit()
        await state.update_data(vibor_pola_user=message.text.lower())
        await bot.send_message(user_id, text="Введи свое имя:", reply_markup=profile(message.from_user.first_name))
        await state.set_state(Wait.name)
    else:
        await state.update_data(vibor_pola_user=message.text.lower())
        await bot.send_message(user_id, text="Введи свое имя:", reply_markup=profile(message.from_user.first_name))
        await state.set_state(Wait.name)

@router_anketa.message(Wait.choosing_gender)
async def incorrect_form_poll(message : types.Message, state: FSMContext):
    await message.answer('Такое непредусмотренно')


@router_anketa.message(Wait.name)
async def choose_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_name_user=message.text.lower())
    await state.set_state(Wait.age)
    db.cursor.execute('SELECT age FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    db.conn.commit()
    if user_count is None:
        await bot.send_message(user_id, text="Введи свой возраст:",reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(user_id, text="Введи свой возраст:",reply_markup=profile(str(user_count)))

@router_anketa.message(Wait.age)
async def choose_age(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text.isdigit():
        await state.update_data(vibor_age_user=message.text.lower())
        await state.set_state(Wait.city)
        await bot.send_message(user_id, text="Выберите город из предложенных",reply_markup=client_kb.kb_vibor_siti_geo)
    else:
        await message.answer("Требуется число, возраст состоит из чисел")

@router_anketa.message(Wait.city, F.text.casefold().in_(["санкт-петербург", "москва"]))
async def choose_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_city_user=message.text)
    await state.set_state(Wait.text)
    db.cursor.execute('SELECT opisanie FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    db.conn.commit()
    if user_count is None:
        await bot.send_message(user_id, text="Введи Описание:",reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(user_id, text="Введи Описание:",reply_markup=profile(str("Оставить текущее")))

@router_anketa.message(Wait.city)
async def incorrect_form_poll(message : types.Message, state: FSMContext):
    await message.answer('Такое непредусмотренно')


@router_anketa.message(Wait.text, F.text == "Оставить текущее")
async def choose_text_base(message: types.Message, state: FSMContext):
    await state.set_state(Wait.photo)
    user_id = message.from_user.id
    db.cursor.execute('SELECT opisanie FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    await state.update_data(vibor_text_user=user_count)
    db.conn.commit()
    db.cursor.execute('SELECT photo, photo_2, photo_3 FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    db.conn.commit()
    if user_count[0] == None and user_count[1] == None and user_count[2] == None:
        await bot.send_message(user_id, text="Пришлите фото для анкеты",reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(user_id, text="Пришлите фото для анкеты",reply_markup = profile(str("Оставить текущее")))
    

@router_anketa.message(Wait.text)
async def choose_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if len(message.text) < 20:
        await message.answer("Слишком мало информации, прошу переосмыслить написанное")
    else:
        await state.update_data(vibor_text_user=message.text)
        await state.set_state(Wait.photo)
        db.cursor.execute('SELECT photo, photo_2, photo_3 FROM anketa WHERE id = ?', (user_id, ))
        user_count = db.cursor.fetchone()
        user_count = user_count[0]
        db.conn.commit()
    if user_count == None:
        await bot.send_message(user_id, text="Пришлите фото для анкеты",reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(user_id, text="Пришлите фото для анкеты",reply_markup = profile(str("Оставить текущее")))

@router_anketa.message(Wait.photo, F.text == "Оставить текущее")
async def choose_photo_ost(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    await anketa_form.db_anketa_user_main(user_id=user_id, 
                                                     gender=data['vibor_pola_user'], 
                                                     name=data['vibor_name_user'], 
                                                     age=data['vibor_age_user'], 
                                                     text=data['vibor_text_user'], 
                                                     city=data['vibor_city_user'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))

@router_anketa.message(Wait.photo, F.photo)
async def choose_photo_1(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_photo_user=message.photo[-1].file_id)
    await state.set_state(Wait.photo_2)
    await bot.send_message(chat_id=user_id, text="Ожидаю 2 фото", reply_markup=profile(["Оставить 1 фото"]))

@router_anketa.message(Wait.photo_2, F.photo)
async def choose_photo_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_photo_user_2=message.photo[-1].file_id)
    await state.set_state(Wait.photo_3)
    await bot.send_message(chat_id=user_id, text="Ожидаю 3 фото", reply_markup=profile(["Оставить 2-е фотографии"]))

@router_anketa.message(Wait.photo_3, F.photo)
async def choose_photo_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_photo_user_3=message.photo[-1].file_id)
    data = await state.get_data()
    await anketa_form.db_anketa_user_main(user_id=user_id,
                                                     gender=data['vibor_pola_user'], 
                                                     name=data['vibor_name_user'], 
                                                     age=data['vibor_age_user'], 
                                                     text=data['vibor_text_user'], 
                                                     city=data['vibor_city_user'],
                                                     photo=data['vibor_photo_user'],
                                                     photo_2=data['vibor_photo_user_2'],
                                                     photo_3=data['vibor_photo_user_3'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))

@router_anketa.message(Wait.photo_2, F.text == 'Оставить 1 фото')
async def choose_photo_2_ost(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    await anketa_form.db_anketa_user_main(user_id=user_id,
                                                     gender=data['vibor_pola_user'],
                                                     name=data['vibor_name_user'], 
                                                     age=data['vibor_age_user'], 
                                                     text=data['vibor_text_user'], 
                                                     city=data['vibor_city_user'],
                                                     photo=data['vibor_photo_user'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))


@router_anketa.message(Wait.photo_3, F.text == 'Оставить 2-е фотографии')
async def choose_photo_3_ost(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    await anketa_form.db_anketa_user_main(user_id=user_id,
                                                     gender=data['vibor_pola_user'],  
                                                     name=data['vibor_name_user'], 
                                                     age=data['vibor_age_user'], 
                                                     text=data['vibor_text_user'], 
                                                     city=data['vibor_city_user'],
                                                     photo=data['vibor_photo_user'],
                                                     photo_2=data['vibor_photo_user_2'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))

@router_anketa.message(Wait.answer_change, F.text == 'Да')
async def choose_ost_yes(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    await client_kb.kb_client_welcom(user_id=user_id)

@router_anketa.message(Wait.answer_change, F.text == 'Изменить анкету')
async def choose_ost_no(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(Wait.answer_change_2)
    await anketa_form.chose_change_anketa(user_id=user_id)

###############################################################################################
"""
Обработка выбора изминений
"""
###############################################################################################

###############################################################################################
"""
Обработка ввода фото
"""
###############################################################################################

@router_anketa.message(Wait.answer_change_2, F.text == 'Фото')
async def choose_change_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(Wait.change_photo)
    await bot.send_message(user_id, text="Пришлите фото для анкеты",reply_markup=types.ReplyKeyboardRemove())

@router_anketa.message(Wait.change_photo, F.photo)
async def choose_change_photo_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_photo_change_user=message.photo[-1].file_id)
    await state.set_state(Wait.change_photo_2)
    await bot.send_message(chat_id=user_id, text="Ожидаю 2 фото", reply_markup=profile(["Оставить 1 фото"]))

@router_anketa.message(Wait.change_photo_2, F.photo)
async def choose_change_photo_3(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_photo_2_change_user=message.photo[-1].file_id)
    await state.set_state(Wait.change_photo_3)
    await bot.send_message(chat_id=user_id, text="Ожидаю 3 фото", reply_markup=profile(["Оставить 2 фото"]))

@router_anketa.message(Wait.change_photo_3, F.photo)
async def choose_change_photo_4(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_photo_3_change_user=message.photo[-1].file_id)
    data = await state.get_data()
    await anketa_form.db_anketa_user_main_change(user_id=user_id,
                                                     photo=data['vibor_photo_change_user'],
                                                     photo_2=data['vibor_photo_2_change_user'],
                                                     photo_3=data['vibor_photo_3_change_user'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))

###############################################################################################
"""
Обработка выбора колличества фото
"""
###############################################################################################

@router_anketa.message(Wait.change_photo_2, F.text == 'Оставить 1 фото')
async def choose_photo_2_change_ost(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    await anketa_form.db_anketa_user_main_change(user_id=user_id,
                                                     photo=data['vibor_photo_change_user'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))


@router_anketa.message(Wait.change_photo_3, F.text == 'Оставить 2 фото')
async def choose_photo_3_change_ost(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    await anketa_form.db_anketa_user_main_change(user_id=user_id,
                                                     photo=data['vibor_photo_change_user'],
                                                     photo_2=data['vibor_photo_2_change_user'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))

###############################################################################################
"""
Завершешния выбора количества фото
"""
###############################################################################################
    
@router_anketa.message(Wait.answer_change_2, F.text == 'Описание')
async def choose_change_opisanie(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(Wait.change_text)
    await bot.send_message(user_id, text="Введи Описание:",reply_markup=types.ReplyKeyboardRemove())

@router_anketa.message(Wait.change_text)
async def choose_change_opisanie_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if len(message.text) < 20:
        await message.answer("Слишком мало информации, прошу переосмыслить написанное")
    else:
        await state.update_data(vibor_change_text_user=message.text)
        data = await state.get_data()
        await anketa_form.db_anketa_user_main_change(user_id=user_id,
                                                     text=data['vibor_change_text_user'])
        await state.set_state(Wait.answer_change)
        await anketa_form.anketa_main(user_id=user_id)
        await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))
###############################################################################################

@router_anketa.message(Wait.answer_change_2, F.text == 'Имя')
async def choose_change_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(Wait.change_name)
    await bot.send_message(user_id, text="Введи Ваше Имя:",reply_markup=types.ReplyKeyboardRemove())

@router_anketa.message(Wait.change_name)
async def choose_change_name_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_chose_name_user=message.text)
    data = await state.get_data()
    await anketa_form.db_anketa_user_main_change(user_id=user_id,
                                                    name=data['vibor_chose_name_user'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))
###############################################################################################

@router_anketa.message(Wait.answer_change_2, F.text == 'Пол')
async def choose_change_pol(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(Wait.change_pol)
    await bot.send_message(user_id, text="Выберите ваш пол", reply_markup=profile(["Парень", "Девушка"]))

@router_anketa.message(Wait.change_pol, F.text.casefold().in_(["парень", "девушка"]))
async def choose_change_pol_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_change_pola_user=message.text.lower())
    data = await state.get_data()
    await anketa_form.db_anketa_user_main_change(user_id=user_id,
                                                    gender=data['vibor_change_pola_user'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))


###############################################################################################

@router_anketa.message(Wait.answer_change_2, F.text == 'Возраст')
async def choose_change_age(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(Wait.change_age)
    await bot.send_message(user_id, text="Введи ваш возраст:", reply_markup=types.ReplyKeyboardRemove())

@router_anketa.message(Wait.change_age)
async def choose_change_age_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text.isdigit():
        await state.update_data(vibor_change_age_user=message.text.lower())
        data = await state.get_data()
        await anketa_form.db_anketa_user_main_change(user_id=user_id,
                                                        age=data['vibor_change_age_user'])
        await state.set_state(Wait.answer_change)
        await anketa_form.anketa_main(user_id=user_id)
        await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))
    else:
        await message.answer("Требуется число, возраст состоит из чисел")


###############################################################################################

@router_anketa.message(Wait.answer_change_2, F.text == 'Город')
async def choose_change_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(Wait.change_city)
    await bot.send_message(user_id, text="Выберите город из предложенных",reply_markup=client_kb.kb_vibor_siti_geo)

@router_anketa.message(Wait.change_city, F.text.casefold().in_(["санкт-петербург", "москва"]))
async def choose_change_city_2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(vibor_change_city_user=message.text)
    data = await state.get_data()
    await anketa_form.db_anketa_user_main_change(user_id=user_id,
                                                    city=data['vibor_change_city_user'])
    await state.set_state(Wait.answer_change)
    await anketa_form.anketa_main(user_id=user_id)
    await message.answer("Все верно?", reply_markup=profile(["Да", "Изменить анкету"]))

@router_anketa.message(Wait.change_city)
async def choose_change_city(message: types.Message, state: FSMContext):
    await message.answer("Таких вариантов нет")

###############################################################################################
@router_anketa.message(Wait.answer_change_2, F.text == 'Выйти')
async def choose_change_exit(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    await client_kb.kb_client_welcom(user_id=user_id)

@router_anketa.message(Wait.answer_change_2, F.text == 'Удалить анкету')
async def choose_change_exit(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    db.cursor.execute('SELECT COUNT(*) FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    db.conn.commit()
    if user_count == 1:
        db.cursor.execute('DELETE FROM anketa WHERE id = ?', (user_id, ))
        db.conn.commit()
        await bot.send_message(chat_id=user_id, text='Успешное удаление')
    elif user_count == 0:
        await bot.send_message(chat_id=user_id, text='Увы, но такой анкеты нет')
    await state.clear()
    await client_kb.kb_client_welcom(user_id=user_id)


###############################################################################################
"""
Завершешния обработки изминений
"""
###############################################################################################