import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.executor import start_webhook
from aiogram.utils.markdown import link
import config
from sqliter import Database
from olx import Olixer


# initialization
bot = Bot(token=config.API_KEY)
dp = Dispatcher(bot)
db = Database()
crawler = Olixer()
logging.basicConfig(level=logging.INFO)


async def on_startup(dp):
    """Start and create task"""
    await db.conn.connect()
    await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(3600))


async def on_shutdown(dp):
    """Shutdown"""
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
    """Craw new post from user's post query"""
    all_queries = await db.get_all_query()
    new_posts = crawler.get_posts(all_queries)
    return new_posts


async def scheduled(wait_for):
    """Main processing loop
    sending all messages own subscribers bot
    """
    logging.info('START')
    while True:
        # time out
        logging.warning(f'Waiting {wait_for} seconds...')
        await asyncio.sleep(wait_for)
        for posts in await scrapi():
            if not posts['urls']:
                logging.info('NOY POST')
                continue
            new_url = posts['urls'][0]
            id = posts['id']
            await db.update_filters(values= {'last_post': new_url,'user_id': id})
            logging.info(len(posts['urls']))
            user_uid = await db.get_user_id(values={'id': id})
            logging.info(user_uid[0])
            for url in posts['urls']:
                # sending new posts
                one = crawler.get_info_post(url)
                photo = open('static/fon.png', 'rb')
                await bot.send_photo(
                    user_uid[0],
                    photo,
                    caption=one['title'] +'\nЦена:' + one['price'] + '\nОписание:'
                            + one['text'].strip()[:400] + link('\nlink', url), disable_notification=True, parse_mode='markdown')
                photo.close()


if __name__ == '__main__':
    """Create webhook"""
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