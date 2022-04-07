import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_webhook
import config
from sqliter import Database
from olx import Olixer
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_KEY)
dp = Dispatcher(bot)
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook setting
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{config.API_KEY}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver setting
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=5000)




# initialization Database
db = Database(config)

# initialization parser
param={}
crawler = Olixer(param)

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(dispatcher):
    await bot.delete_webhook()



@dp.message_handler(commands=['start', 'help'])
async def send_message(message: types.Message):
    await message.reply("Hi everybody")

# command subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.message):
    if not db.subscriber_exists(user_uid=message.from_user.id):
        db.add_subscriber(message.from_user.id, True)
        await message.answer('Вы успешно подписались на рассылку! OLX')
    else:
        db.update_subscription(message.from_user.id, True)
        await message.answer('Подписка активирована')


# command unsubscribe
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
        await message.answer('Вы отписаны')
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer('Вы успешно отписаны от рассылки')

@dp.message_handler(commands=['filter'])
async def unsubscribe(message: types.Message):
    await message.answer('Вставте ссылку с olx.kz')

@dp.message_handler(regexp='(https://)')
async def unsubscribe(message: types.Message):
    olx_query = message.text
    if not crawler.correct_address(olx_query):
        await message.answer('URL not correct.\n Try again')
        return
    db.add_filters(olx_query, message.from_user.id)
    await message.answer('Your filters successfully added')

async def scrapi():
    all_queries = db.get_all_query()
    new_posts = crawler.get_posts(all_queries).__next__()
    return new_posts
@dp.message_handler(commands=['go'])
async def go(message: types.Message):
    await message.answer('go')


async def scheduled(wait_for):
    while True:
        # time out
        await asyncio.sleep(wait_for)
        posts = await scrapi()
        if not posts['urls']:
            continue
        new_url = posts['urls'][0]
        id = posts['id']
        db.update_filters(new_url, id)
        logging.info(len(posts['urls']))
        for url in posts['urls']:
            one = crawler.get_info_post(url)
            photo = open('static/fon.png', 'rb')
            await bot.send_photo(
                838019137,
                photo,
                caption=one['title'] + '\n' + 'Цена:' + one['price'] + 'От:' + '\nОписание:'
                        + one['text'].strip()[:400] + url, disable_notification=True)
            photo.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )

    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(20))
    executor.start_polling(dp, skip_updates=True)

