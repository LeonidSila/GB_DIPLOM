from config import bot
from aiogram import F, Router
from aiogram import types
from poisk import poisk_main_form
from keaboards import voth_anketa_kb, client_kb
from database import data_base as db

router_poisk = Router()

@router_poisk.message(F.text == 'kek')
async def poisk_ank_1(message : types.Message):
    user_id = message.from_user.id
    await poisk_main_form.poisk_anket_alg(user_id=user_id)

@router_poisk.message(F.text == '🧡')
async def ank_in_poisk_like(message : types.Message):
    user_id = message.from_user.id
    if await poisk_main_form.call_click_db(user_id=user_id) == "Доступ открыт":
        db.cursor.execute('SELECT like_users FROM anketa WHERE id = ?', (user_id, ))
        liks_user_point  = db.cursor.fetchone()
        liks_user_point =  liks_user_point[0]
        db.conn.commit()
        if liks_user_point is not None:
            db.cursor.execute('SELECT like FROM anketa WHERE id = ?', (liks_user_point, ))
            user_liks  = db.cursor.fetchone()
            user_liks = user_liks[0]
            db.conn.commit()
            if user_liks is None:
                db.cursor.execute('UPDATE anketa set like = ? where id = ?', 
                        (user_id, liks_user_point, ))
                db.conn.commit()
                await poisk_main_form.anketa_poisk(user_id=user_id)
                await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
            else:
                if str(user_id) in user_liks:
                    await poisk_main_form.anketa_poisk(user_id=user_id)
                    await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
                else:
                    user_liks = user_liks.split(",")
                    user_liks.append(str(user_id))
                    new_user_list = ",".join(user_liks)
                    db.cursor.execute('UPDATE anketa set like = ? where id = ?', 
                        (new_user_list, liks_user_point, ))
                    db.conn.commit()
                    await poisk_main_form.anketa_poisk(user_id=user_id)
                    await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
        else:
            await poisk_main_form.anketa_poisk(user_id=user_id)
            await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
    else:
        return

@router_poisk.message(F.text == '👎🏻')
async def ank_in_poisk_diz_like(message : types.Message):
    user_id = message.from_user.id
    if await poisk_main_form.call_click_db(user_id=user_id) == "Доступ открыт":
        await poisk_main_form.anketa_poisk(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
    else:
        return

@router_poisk.message(F.text == '💤')
async def ank_in_poisk_diz_like(message : types.Message):
    user_id = message.from_user.id
    await client_kb.kb_client_welcom(user_id=user_id)