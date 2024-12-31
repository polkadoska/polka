import ssl
from aiogram import Bot, executor, types
from loader import dp, bot, loop
import handlers, middlewares
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands
from utils.apschedule import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web
from utils.yoo import *
from data import config
import asyncio

# from utils.yoomoney import success_pay_yoomoney


WEBHOOK_HOST = config.WEBHOOK_HOST
WEBHOOK_PATH = config.WEBHOOK_PATH
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBHOOK_SSL_CERT = config.WEBHOOK_SSL_CERT
WEBHOOK_SSL_PRIV = config.WEBHOOK_SSL_PRIV
WEBAPP_HOST = config.WEBAPP_HOST
WEBAPP_PORT = config.WEBAPP_PORT

SSL_ON = True


async def on_startup(app):
    await set_default_commands(dp)
    await on_startup_notify(dp)
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(check_balance_and_debits_money, trigger='cron', hour=19, args=(dp,))
    scheduler.start()
    app = web.Application()
    app.router.add_post('/yookassa', yookassaapp)
    runner = web.AppRunner(app)
    await runner.setup()
    if SSL_ON:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
        site = web.TCPSite(runner, '0.0.0.0', 8444, ssl_context=ssl_context)
    else:
        site = web.TCPSite(runner, '0.0.0.0', 8444)
    await site.start()
    

async def on_shutdown(app):
    await on_shutdown_notify(dp)


async def yookassaapp(request):
    try:
        data = await request.json()
        logging.info(f"CHECK PAY: {data}")
        await success_pay(data)
        return web.Response(status=200)
    except Exception as e:
        logging.error(e)
        return web.Response(status=400)
    
async def yoomoneyapp(request):
    try:
        data = await request.text()
        logging.info(f"CHECK PAY: {data}")
        # await success_pay_yoomoney(data)
        return web.Response(status=200)
    except Exception as e:
        logging.error(e)
        return web.Response(status=400)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
