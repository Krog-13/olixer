import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_webhook
from aiogram.utils.markdown import link
import config
from sqliter import Database
from olx import Olixer
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_KEY)
dp = Dispatcher(bot)

# initialization Database
db = Database()

# initialization parser
param={}
crawler = Olixer(param)

async def on_startup(dp):
    await db.conn.connect()
    await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(500))

async def on_shutdown(dp):
    await db.conn.disconnect()
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bay!')

@dp.message_handler(commands='help')
async def send_message(message: types.Message):
    await message.reply("Hi everybody")

# command subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.message):
    if not await db.subscriber_exists(values={'uid': message.from_user.id}):
        await db.add_subscriber(values= {'uid': message.from_user.id,'status': True})
        await message.answer('Вы успешно подписались на рассылку! OLX')
    else:
        await db.update_subscription(values= {'uid': message.from_user.id,'status': True})
        await message.answer('Подписка активирована')

# command unsubscribe
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not await db.subscriber_exists(values={'uid': message.from_user.id}):
        await db.add_subscriber(values= {'uid': message.from_user.id,'status': False})
        await message.answer('Вы отписаны')
    else:
        await db.update_subscription(values= {'uid': message.from_user.id,'status': False})
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
    await db.add_filters(values= {'uid': message.from_user.id, 'query_post': olx_query})
    await message.answer('Your filters successfully added')

async def scrapi():
    all_queries = await db.get_all_query()
    new_posts = crawler.get_posts(all_queries).__next__()
    return new_posts

async def scheduled(wait_for):
    logging.info('START')
    while True:
        # time out
        await asyncio.sleep(wait_for)
        posts = await scrapi()
        if not posts['urls']:
            logging.info('NOY POST')
            continue
        new_url = posts['urls'][0]
        id = posts['id']
        await db.update_filters(values= {'last_post': new_url,'user_id': id})
        logging.info(len(posts['urls']))
        for url in posts['urls']:
            one = crawler.get_info_post(url)
            photo = open('static/fon.png', 'rb')
            await bot.send_photo(
                838019137,
                photo,
                caption=one['title'] + '\n' + 'Цена:' + one['price'] + 'От:' + '\nОписание:'
                        + one['text'].strip()[:400] + link('\nclick', url), disable_notification=True, parse_mode='markdown')
            photo.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT
    )

