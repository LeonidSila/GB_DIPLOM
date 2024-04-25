from aiogram import types
from aiogram import F, Router, Bot
from keaboards import client_kb
from database import data_base as db

from config import dp, bot

from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType



router_shop = Router()


@router_shop.message(F.text == '100 нажатий')
async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id = message.from_user.id,
        title= '100 нажатий',
        description='Сбрасывает нажатие до 0',
        payload='Pay_100_click',
        provider_token = '381764678:TEST:83693',
        currency='rub',
        prices=[
                    LabeledPrice(
                        label='Доступ к секретной информации',
                        amount=30000
                    ),
                    LabeledPrice(
                        label='НДС',
                        amount=20000
                    ),
                    LabeledPrice(
                        label='Скидка',
                        amount=-1000
                    ),
                    LabeledPrice(
                        label='Бонус',
                        amount=-40000
                    )
                ],
        max_tip_amount=50000,
        suggested_tip_amounts=[1000,2000,3000,4000],
        start_parameter='bot',
        provider_data=None,
        photo_url='https://play-lh.googleusercontent.com/LHZ34g6xvzFL5RtsJ_o3hCeNSoYq7OJ3Hw2WsRhrM00SJIZDftNpELElEIVWbXyLpQ=w1024-h500',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=None
        )
    

@router_shop.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)

@router_shop.message(F.successful_payment)
async def successful_payment(message: Message):
    user_id = message.from_user.id
    msg = f'Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}.'
    await message.answer(msg)
    await client_kb.kb_client_welcom(user_id=user_id)
    str_opirasion = message.successful_payment.invoice_payload
    if str_opirasion == 'Pay_100_click':
        db.cursor.execute('UPDATE users set call_clik = 0 where id = ?', 
        (user_id, ))
        db.conn.commit()
    elif str_opirasion == 'Vip_click':
        db.cursor.execute('UPDATE users set vip = 1 where id = ?', 
        (user_id, ))
        db.conn.commit()

    



@router_shop.message(F.text == 'VIP')
async def order_2(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id = message.from_user.id,
        title= 'Статус VIP',
        description='Пожизненый VIP',
        payload='Vip_click',
        provider_token = '381764678:TEST:83693',
        currency='rub',
        prices=[
                    LabeledPrice(
                        label='Доступ к секретной информации',
                        amount=99900
                    ),
                    LabeledPrice(
                        label='НДС',
                        amount=20000
                    ),
                    LabeledPrice(
                        label='Скидка',
                        amount=-1000
                    ),
                    LabeledPrice(
                        label='Бонус',
                        amount=-40000
                    )
                ],
        max_tip_amount=100000,
        suggested_tip_amounts=[1000,2000,3000,4000],
        start_parameter='bot',
        provider_data=None,
        photo_url='https://sun6-22.userapi.com/s/v1/if2/rzp2EN7a52WWXVn09g2WB0zpZPH4dlBLBqGNungOn0WzROIUBz2mKtU6Vc-cg-LhlH9tDrdyGxtvriVIpdHqdHBc.jpg?size=971x971&quality=96&crop=0,593,971,971&ava=1',
        photo_size=100,
        photo_width=800,
        photo_height=450,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=None
        )
    