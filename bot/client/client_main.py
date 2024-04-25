from aiogram import F, Router, types
from config import dp, bot
from aiogram.filters import Command
from database import data_base as db
from keaboards import client_kb, voth_anketa_kb
from anketa_main import anketa_form, anketa
from aiogram.fsm.context import FSMContext
from poisk import poisk_main_form
import random
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router_client = Router()
class Count(StatesGroup):
    choze_users = State()
    like = State()
    dizlike = State()

@router_client.message(Command(commands=['help', 'start']))
async def start_help_command(message : types.Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    await message.delete()
    db.cursor.execute('SELECT COUNT(*) FROM users WHERE id = ?', (user_id, ))
    db.conn.commit()
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    if user_count == 0:
        db.cursor.execute('INSERT INTO users (id, Name_m, Last_name_m) VALUES (?, ?, ?)', (user_id, user_first_name, user_last_name, ))
        db.conn.commit()
        await client_kb.kb_client_welcom(user_id=user_id)
    elif user_count == 1:
        await client_kb.kb_client_welcom(user_id=user_id)

@router_client.message(Command(commands=['help', 'start']))

@router_client.message(F.text == '1')
async def main_menu_1(message : types.Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    db.cursor.execute('SELECT COUNT(*) FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    db.conn.commit()
    if user_count == 0:
        await bot.send_message(user_id, text="Вы не можете смотреть анкеты, без своей. Заполните ее и возвращайтесь!", reply_markup=client_kb.kb_vibor_OK)
    else:
        await poisk_main_form.poisk_main(user_id)
        await poisk_main_form.anketa_poisk(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)

@router_client.message(F.text == '2')
async def main_menu_2(message : types.Message, state: FSMContext):
    user_id = message.from_user.id
    db.cursor.execute('SELECT COUNT(*) FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    db.conn.commit()
    if user_count == 0:
        await bot.send_message(user_id, text="<b>Вы не можете изменить анкету, которой не сушествуеб</b>", reply_markup=client_kb.kb_vibor_OK)
    else:
        await state.set_state(anketa.Wait.answer_change_2)
        await anketa_form.chose_change_anketa(user_id=user_id)

@router_client.message(F.text == '3')
async def main_menu_3(message : types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    db.cursor.execute('SELECT COUNT(*) FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    db.conn.commit()
    if user_count == 0:
        await bot.send_message(user_id, text="<b>Вы не зайти в магазин без анкеты\nЗапоните ее</b>", reply_markup=client_kb.kb_vibor_OK)
    else:
        await bot.send_message(chat_id=user_id, text="Что вы хотите купить?\n1) Купить 100 нажатий, хватит еще немного\n2)<b> Vip - У вас появится бесконечные нажатия и статус в профиле</b>", reply_markup=client_kb.kb_vibor_shop)


@router_client.message(F.text == 'roll_db')
async def main_menu_4(message : types.Message, state: FSMContext):
    for i in range(100):
        id = random.randint(1000000, 9999999)
        age = random.randint(1, 100)
        str_name = ('nasita', 'olga', 'ksuha', 'Lexas', 'Alina', 'Vita', 'msx', 'vania', 'nikita', 'ania', 'andey')
        random_name = str_name[random.randint(0, len(str_name)-1)]
        gender_str = ('парень', 'девушка')
        random_gender = gender_str[random.randint(0, len(gender_str)-1)]
        city_str = ('Санкт-Петербург', 'Москва')
        random_city = city_str[random.randint(0, len(city_str)-1)]
        url = 'leonardosion'
        opisanie = 'test_test test test test_test test test test_test test test test_test test test'
        photo = 'AgACAgIAAxkBAAIbTGYnnj1S2cqpc7P7DnY5izG5gZQvAAJG1TEbG2RBSW7AU4Nw1t9vAQADAgADeQADNAQ'
        db.cursor.execute('INSERT INTO anketa (id, name, url_user, age, gender, city, opisanie, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, random_name, url, age, random_gender, random_city, opisanie, photo, ))
        db.conn.commit()



@router_client.message(F.text == 'Более чем')
async def main_menu_yes(message : types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(Count.choze_users)
    db.cursor.execute('SELECT like FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    if user_count is None:
        await state.clear()
        await poisk_main_form.anketa_poisk(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
        return
    user_is_data_base = user_count.split(",")
    if len(user_is_data_base) == 1:
        await anketa_form.anketa_main(user_id=user_id, user_id_anketa_poisk=int(user_is_data_base[0]))
        await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
        db.cursor.execute('UPDATE anketa set like_users = ? where id = ?', 
                    (int(user_is_data_base[0]), user_id, ))
        db.conn.commit()
        db.cursor.execute('UPDATE anketa set like = NULL where id = ?', 
                                                            (user_id, ))
        db.conn.commit()
    else:
        user_list_like_id_del = user_is_data_base.pop(0)
        await anketa_form.anketa_main(user_id=user_id, user_id_anketa_poisk=user_list_like_id_del)
        await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
        db.cursor.execute('UPDATE anketa set like_users = ? where id = ?', 
        (int(user_list_like_id_del), user_id, ))
        db.conn.commit()
        new_user_list = ",".join(user_is_data_base)
        db.cursor.execute('UPDATE anketa set like = ? where id = ?', 
                    (new_user_list, user_id, ))
        db.conn.commit()

@router_client.message(Count.choze_users, F.text == '🧡')
async def choose_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    db.cursor.execute('SELECT like_users FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    await anketa_form.anketa_main(user_id=user_id, user_id_anketa_poisk=user_count, count_1=1)
    
    db.cursor.execute('SELECT like FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    if user_count is None:
        await state.clear()
        await poisk_main_form.anketa_poisk(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
    else:
        user_is_data_base = user_count.split(",")
        if len(user_is_data_base) == 1:
            await anketa_form.anketa_main(user_id=user_id, user_id_anketa_poisk=user_is_data_base[0])
            await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
            db.cursor.execute('UPDATE anketa set like_users = ? where id = ?', 
                        (int(user_is_data_base[0]), user_id, ))
            db.conn.commit()
            db.cursor.execute('UPDATE anketa set like = NULL where id = ?', 
                                                                (user_id, ))
            db.conn.commit()
        else:
            user_list_like_id_del = user_is_data_base.pop(0)
            await anketa_form.anketa_main(user_id=user_id, user_id_anketa_poisk=user_list_like_id_del)
            await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
            db.cursor.execute('UPDATE anketa set like_users = ? where id = ?', 
            (int(user_list_like_id_del), user_id, ))
            db.conn.commit()
            db.cursor.execute('UPDATE anketa set like = ? where id = ?', 
                        (user_is_data_base, user_id, ))
            db.conn.commit()

@router_client.message(Count.choze_users, F.text == '👎🏻')
async def choose_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    db.cursor.execute('SELECT like FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    user_count = user_count[0]
    if user_count is None:
        await state.clear()
        await poisk_main_form.anketa_poisk(user_id=user_id)
        await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
    else:
        user_is_data_base = user_count.split(",")
        if len(user_is_data_base) == 1:
            await anketa_form.anketa_main(user_id=user_id, user_id_anketa_poisk=user_is_data_base[0])
            await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
            db.cursor.execute('UPDATE anketa set like_users = ? where id = ?', 
                        (int(user_is_data_base[0]), user_id, ))
            db.conn.commit()
            db.cursor.execute('UPDATE anketa set like = NULL where id = ?', 
                                                                (user_id, ))
            db.conn.commit()
        else:
            number_index = user_is_data_base[random.randint(0, len(user_is_data_base)-1)]
            user_list_like_id_del = user_is_data_base.pop(number_index)
            await anketa_form.anketa_main(user_id=user_id, user_id_anketa_poisk=user_list_like_id_del)
            await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)
            db.cursor.execute('UPDATE anketa set like_users = ? where id = ?', 
            (int(user_list_like_id_del), user_id, ))
            db.conn.commit()
            db.cursor.execute('UPDATE anketa set like = ? where id = ?', 
                        (user_is_data_base, user_id, ))
            db.conn.commit()

@router_client.message(Count.choze_users, F.text == '💤')
async def choose_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    await client_kb.kb_client_welcom(user_id=user_id)
   
@router_client.message(Count.choze_users, F.text == 'НЕТ')
async def choose_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    await poisk_main_form.anketa_poisk(user_id=user_id)
    await bot.send_message(chat_id=user_id, text=f'{poisk_main_form.random_str()}', reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)