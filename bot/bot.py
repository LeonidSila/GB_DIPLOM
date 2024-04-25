
from client import client_main as c
from anketa_main import anketa as ank
import asyncio
from config import bot, dp
from database import data_base as db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from poisk import poisk_main as poisk
from poisk import poisk_main_form
from shop import shop_main as sh
from aiogram.types import PreCheckoutQuery, ContentType


db.creat_teble()

dp.include_router(c.router_client)
dp.include_router(ank.router_anketa)
dp.include_router(poisk.router_poisk)
dp.include_router(sh.router_shop)

dp.pre_checkout_query(sh.pre_checkout_query)



async def start():
    try:
        scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
        scheduler.add_job(poisk_main_form.poisk_anket_time_like, trigger='interval', seconds = 14800, kwargs={'bot': bot})
        scheduler.add_job(poisk_main_form.help_url_not, trigger='interval', seconds = 5, kwargs={'bot': bot})
        scheduler.add_job(poisk_main_form.reset_click, trigger='cron', hour=2, minute=1, kwargs={'bot': bot})
        scheduler.start()
        await dp.start_polling(bot)
    except Exception as e:
        print(f'Start: {str(e)}')
        await bot.session.close()



if __name__ == "__main__":
    asyncio.run(start())