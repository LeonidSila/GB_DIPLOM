
from keaboards import voth_anketa_kb, client_kb
from database import data_base as db
from config import bot
import random
from anketa_main import anketa_form
from aiogram import Bot


str_vois =['Возможно', 'Хмм','Может', 'A что если', 'Интересно', 'Возможно ли','А что, если бы', 
           'Может быть', 'Что если','Неужели', 'А вдруг', 'Что думаешь?','Представь', 'Интересно было бы', 
           'А можешь себе представить?','Возможно ли это?', 'Неужели это правда' 
           'Может быть такой вариант?','Представь себе?', 'Задумайся о этом?']
def random_str():
    str_for_user = str_vois[random.randint(0, len(str_vois)-1)]
    return str_for_user

async def poisk_main(user_id):

    await bot.send_message(chat_id=user_id, text="Давай посмотрим",reply_markup=voth_anketa_kb.kb_vibor_anketa_poisk)



async def poisk_anket_alg(user_id):
    db.cursor.execute('SELECT age, city, gender FROM anketa WHERE id = ?', (user_id, ))
    user_count = db.cursor.fetchone()
    db.conn.commit()
    db.cursor.execute('SELECT id FROM anketa WHERE id <> ? AND gender <> ? AND city = ? AND age >= ? AND age <= ?', 
                      (user_id, user_count[2] ,user_count[1], int(user_count[0])-13, int(user_count[0])+13, ))
    user_count_ank = db.cursor.fetchall()
    db.conn.commit()
    for i in range(len(user_count_ank)):
        user_count_ank[i] = str(user_count_ank[i])[1:-2]
    new_user_list = ",".join(user_count_ank)
    db.cursor.execute('UPDATE anketa set user_cout_poisk = ? where id = ?', 
                    (new_user_list, user_id, ))
    db.conn.commit()

async def call_click_db(user_id):
    db.cursor.execute('SELECT vip FROM users WHERE id = ?', (user_id, ))
    user_vip  = db.cursor.fetchone()
    user_vip = user_vip [0]
    db.conn.commit()
    if user_vip == 0:
        db.cursor.execute('SELECT call_clik FROM users WHERE id = ?', (user_id, ))
        user_count_ank = db.cursor.fetchone()
        user_count_ank = user_count_ank[0]

        if user_count_ank >=100:
            await bot.send_message(chat_id=user_id, text="Вы просмотрели лимит на сегодня\nВы можете купить в магазине либо дополнительное колличесвто, либо купить безлимит", 
                            reply_markup=client_kb.kb_vibor_shop)
            return "Лимит закончен"
        elif user_count_ank == 99:
            user_count_ank = user_count_ank + 1
            await bot.send_message(chat_id=user_id, text='Это последняя анкета на сегодня')
            db.cursor.execute('UPDATE users set call_clik = ? where id = ?', 
                        (user_count_ank, user_id, ))
            db.conn.commit()
            return "Доступ открыт"
        else:
            user_count_ank = user_count_ank + 1
            db.cursor.execute('UPDATE users set call_clik = ? where id = ?', 
                        (user_count_ank, user_id, ))
            db.conn.commit()
            return "Доступ открыт"
    else:
        return "Доступ открыт"

async def anketa_poisk(user_id):
    db.cursor.execute('SELECT user_cout_poisk FROM anketa WHERE id = ?', (user_id, ))
    user_count_ank = db.cursor.fetchone()
    db.conn.commit()
    if user_count_ank[0] is None:
        await poisk_anket_alg(user_id=user_id)
        db.cursor.execute('SELECT user_cout_poisk FROM anketa WHERE id = ?', (user_id, ))
        user_count_ank = db.cursor.fetchone()
        db.conn.commit()
    user_is_data_base = user_count_ank[0].split(",")
    if len(user_is_data_base)<2:
        await poisk_anket_alg(user_id=user_id)
        db.cursor.execute('SELECT user_cout_poisk FROM anketa WHERE id = ?', (user_id, ))
        user_count_ank = db.cursor.fetchone()
        db.conn.commit()
        user_is_data_base = user_count_ank[0].split(",")
    number_index = random.randint(0, len(user_is_data_base)-1)
    user_id_anketa_poisk = user_is_data_base[number_index]
    user_like = user_is_data_base.pop(number_index)
    db.cursor.execute('UPDATE anketa set like_users = ? where id = ?', 
                    (int(user_like), user_id, ))
    db.conn.commit()
    new_user_list = ",".join(user_is_data_base)
    db.cursor.execute('UPDATE anketa set user_cout_poisk = ? where id = ?', 
                    (new_user_list, user_id, ))
    db.conn.commit()
    await anketa_form.anketa_main(user_id=user_id, user_id_anketa_poisk=user_id_anketa_poisk)


###############################################################################################
"""
Временное исполение
"""
###############################################################################################
async def poisk_anket_time_like(bot : Bot):
    db.cursor.execute('SELECT id, like FROM anketa')
    user_count = db.cursor.fetchall()
    for i in range(len(user_count)):
        try:
            if user_count[i][1] is not None:
                await bot.send_message(chat_id=user_count[i][0], text=f'У вас {len(user_count[i][1].split(","))} почитателей, готовы посмотреть?', reply_markup=voth_anketa_kb.kb_vibor_anketa_time)
            elif user_count[i][1] is None:
                await bot.send_message(chat_id=user_count[i][0], text=f'<b>{len(user_count)}</b> Ждут тебя')
        except:
            print('Пропуск')

async def help_url_not(bot : Bot):
    db.cursor.execute('SELECT id FROM anketa')
    user_count = db.cursor.fetchall()
    for i in range(len(user_count)):
        try:
            await bot.send_photo(chat_id=user_count[i][0], photo='AgACAgIAAxkBAAIdxmYpLQbuhdbXdGXen0X39Jh4Y0S8AAI62TEbFmZQSYAe9caiuLwRAQADAgADeQADNAQ')
            await bot.send_message(chat_id=user_count[i][0], text='Учтите, если у вас не работает отображение ссылки на аккаунт, заполените ячейку, как на фото выше')
        except:
            print('Пропуск')

async def reset_click(bot : Bot):
    db.cursor.execute('UPDATE users set call_clik = 0')
    db.conn.commit()
    print('Обнуление')