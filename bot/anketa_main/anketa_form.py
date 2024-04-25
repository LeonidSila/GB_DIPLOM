from database import data_base as db
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile, InputMediaPhoto
from config import dp, bot
from keaboards import voth_anketa_kb, client_kb
from aiogram import F, Router
# from geo_map import geo_map_client as geo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

#Основа для отображения входного меню в поиске анкеты

async def chose_change_anketa(user_id):
    await bot.send_message(chat_id=user_id, text="1: Изменить фото\n2: Изменить описание\n3: Изменить Имя\n4: Изменить пол\n5: Изменить Возраст\n6: Изменить Город",
                           reply_markup=client_kb.answer_change_menu)

async def db_anketa_user_main(user_id, gender, name, age, text, city, photo=None, photo_2=None, photo_3=None):
    
    if photo is None:
        db.cursor.execute('UPDATE anketa set gender = ?, name = ?, age = ?, city = ?, opisanie = ? where id = ?', 
                            (gender, name, age, city, text, user_id, ))
        db.conn.commit()
    elif photo_2 is None and photo_3 is None:
        db.cursor.execute('UPDATE anketa set gender = ?, name = ?, age = ?, city = ?, opisanie = ?, photo = ? where id = ?', 
                            (gender, name, age, city, text, photo, user_id, ))
        db.conn.commit()
    elif photo_3 is None:
        db.cursor.execute('UPDATE anketa set gender = ?, name = ?, age = ?, city = ?, opisanie = ?, photo = ?, photo_2 = ? where id = ?', 
                            (gender, name, age, city, text, photo, photo_2, user_id, ))
        db.conn.commit()
    else:
        db.cursor.execute('UPDATE anketa set gender = ?, name = ?, age = ?, city = ?, opisanie = ?, photo = ?, photo_2 = ?, photo_3 = ? where id = ?', 
                            (gender, name, age, city, text, photo, photo_2, photo_3, user_id, ))
        db.conn.commit()

async def db_anketa_user_main_change (user_id, gender = None, name = None, age = None, text = None, city = None, photo=None, photo_2=None, photo_3=None):
    if photo is not None and photo_2 is not None and photo_3 is not None:
        db.cursor.execute('UPDATE anketa set photo = ?, photo_2 = ?, photo_3 = ? where id = ?', 
                            (photo, photo_2, photo_3, user_id, ))
        db.conn.commit()
    elif photo is not None and photo_2 is not None:
        db.cursor.execute('UPDATE anketa set photo = ?, photo_2 = ?, photo_3 = Null where id = ?', 
                            (photo, photo_2, user_id, ))
        db.conn.commit()
    elif photo is not None:
        db.cursor.execute('UPDATE anketa set photo = ?, photo_2 = Null, photo_3 = Null where id = ?', 
                            (photo, user_id, ))
        db.conn.commit()
    elif gender is not None:
        db.cursor.execute('UPDATE anketa set gender = ? where id = ?', 
                            (gender, user_id, ))
        db.conn.commit()
    elif name is not None:
        db.cursor.execute('UPDATE anketa set name = ? where id = ?', 
                            (name, user_id, ))
        db.conn.commit()
    elif age is not None:
        db.cursor.execute('UPDATE anketa set age = ? where id = ?', 
                            (age, user_id, ))
        db.conn.commit()
    elif text is not None:
        db.cursor.execute('UPDATE anketa set opisanie = ? where id = ?', 
                            (text, user_id, ))
        db.conn.commit()
    elif city is not None:
        db.cursor.execute('UPDATE anketa set city = ? where id = ?', 
                            (city, user_id, ))
        db.conn.commit()


async def anketa_main(user_id, user_id_anketa_poisk = None, count_1 = None):
    if count_1 is not None:
        db.cursor.execute('SELECT name, age, opisanie, photo, photo_2, photo_3, city, url_user FROM anketa WHERE id = ?', (user_id_anketa_poisk, ))
        user_count = db.cursor.fetchone()
        db.conn.commit()
        user_name = user_count[0].capitalize()
        user_age = user_count[1]
        user_opisanie = user_count[2]
        photo_1 = user_count[3]
        photo_2 = user_count[4]
        photo_3 = user_count[5]
        city = user_count[6]
        url_user = user_count[7]
        if photo_2 is not None and photo_3 is None:
            photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city}) (@{url_user})\n{user_opisanie}</b>'))
            photo_2 = InputMediaPhoto(media=photo_2)
            media_user = [photo_1, photo_2]
            await bot.send_media_group(chat_id = user_id, media = media_user)
        elif photo_2 is None:
            photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city}) (@{url_user})\n{user_opisanie}</b>'))
            media_user = [photo_1]
            await bot.send_media_group(chat_id = user_id, media = media_user)
        else:
            photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city}) (@{url_user})\n{user_opisanie}</b>'))
            photo_2 = InputMediaPhoto(media=photo_2)
            photo_3 = InputMediaPhoto(media=photo_3)
            media_user = [photo_1, photo_2, photo_3]
            await bot.send_media_group(chat_id = user_id, media = media_user)
    
    elif user_id_anketa_poisk is None:
        db.cursor.execute('SELECT name, age, opisanie, photo, photo_2, photo_3, city FROM anketa WHERE id = ?', (user_id, ))
        user_count = db.cursor.fetchone()
        db.conn.commit()
        user_name = user_count[0].capitalize()
        user_age = user_count[1]
        user_opisanie = user_count[2]
        photo_1 = user_count[3]
        photo_2 = user_count[4]
        photo_3 = user_count[5]
        city = user_count[6]
        if photo_2 is not None and photo_3 is None:
            photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city})\n{user_opisanie}</b>'))
            photo_2 = InputMediaPhoto(media=photo_2)
            media_user = [photo_1, photo_2]
            await bot.send_media_group(chat_id = user_id, media = media_user)
        elif photo_2 is None:
            photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city})\n{user_opisanie}</b>'))
            media_user = [photo_1]
            await bot.send_media_group(chat_id = user_id, media = media_user)
        else:
            photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city})\n{user_opisanie}</b>'))
            photo_2 = InputMediaPhoto(media=photo_2)
            photo_3 = InputMediaPhoto(media=photo_3)
            media_user = [photo_1, photo_2, photo_3]
            await bot.send_media_group(chat_id = user_id, media = media_user)
        await bot.send_message(chat_id=user_id, text="Ваша анкета выгядит так")
    else:
        db.cursor.execute('SELECT name, age, opisanie, photo, photo_2, photo_3, city FROM anketa WHERE id = ?', (user_id_anketa_poisk, ))
        user_count = db.cursor.fetchone()
        db.conn.commit()
        user_name = user_count[0].capitalize()
        user_age = user_count[1]
        user_opisanie = user_count[2]
        photo_1 = user_count[3]
        photo_2 = user_count[4]
        photo_3 = user_count[5]
        city = user_count[6]
        if photo_2 is not None and photo_3 is None:
            photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city})\n{user_opisanie}</b>'))
            photo_2 = InputMediaPhoto(media=photo_2)
            media_user = [photo_1, photo_2]
            await bot.send_media_group(chat_id = user_id, media = media_user)
        elif photo_2 is None:
            photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city})\n{user_opisanie}</b>'))
            media_user = [photo_1]
            await bot.send_media_group(chat_id = user_id, media = media_user)
        else:
            photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city})\n{user_opisanie}</b>'))
            photo_2 = InputMediaPhoto(media=photo_2)
            photo_3 = InputMediaPhoto(media=photo_3)
            media_user = [photo_1, photo_2, photo_3]
            await bot.send_media_group(chat_id = user_id, media = media_user)



    # if photo_3 is not None or photo_2 is not None or photo_1 is not None:
    #     photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city})\n{user_opisanie}</b>'))
    #     photo_2 = InputMediaPhoto(media=photo_2)
    #     photo_3 = InputMediaPhoto(media=photo_3)
    #     media_user = [photo_1, photo_2, photo_3]
    #     await bot.send_media_group(chat_id = user_id, media = media_user)
    # elif photo_3 is None or photo_2 is None:
    #     photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city})\n{user_opisanie}</b>'))
    #     media_user = [photo_1]
    #     await bot.send_media_group(chat_id = user_id, media = media_user)
    # elif photo_3 is None:
    #     photo_1 = InputMediaPhoto(media=photo_1, caption=(f'<b>{user_name} - {user_age} ({city})\n{user_opisanie}</b>'))
    #     photo_2 = InputMediaPhoto(media=photo_2)
    #     media_user = [photo_1, photo_2]
    #     await bot.send_media_group(chat_id = user_id, media = media_user)
    # await bot.send_message(chat_id=user_id, text="Ваша анкета выгядит так")

async def chablon_db_anketa_user_all(user_id, name, age, opisanie, gender, interes, city=None, poisk_po_city = None, latitude=None, longitude=None, photo_1 = None, photo_2 = None, photo_3 = None):
        db.cursor.execute('UPDATE anketa set name = ?, age = ?, gender = ?, interes = ?, city = ?, poisk_po_city = ?, latitude = ?, longitude = ?, opisanie = ?, photo = ?, photo_2 = ?, photo_3 = ? where id = ?', 
                          (name, age, gender, interes, city, poisk_po_city, latitude, longitude, opisanie, photo_1, photo_2, photo_3, user_id, ))
        db.conn.commit()