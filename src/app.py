import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import link
import config
from sqliter import Database
from olx import Olixer
logging.basicConfig(level=logging.INFO)
from loguru import logger as LOGGER
bot = Bot(token=config.API_KEY)
dp = Dispatcher(bot)

# initialization Database
db = Database(config)

# initialization parser
param={}
crawler = Olixer(param)


@dp.message_handler(commands=['start', 'help'])
async def send_message(message: types.Message):
    await message.reply(link('link', 'www.google.com'), parse_mode='markdown')

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
            LOGGER.debug('Not post')
            continue
        new_url = posts['urls'][0]
        id = posts['id']
        db.update_filters(new_url, id)
        LOGGER.debug(len(posts['urls']))
        for url in posts['urls']:
            one = crawler.get_info_post(url)
            photo = open('static/fon.png', 'rb')
            await bot.send_photo(
                838019137,
                photo,
                caption=one['title'] + '\n' + 'Цена:' + one['price'] + 'От:' + '\nОписание:'
                        + one['text'].strip()[:400] + link('clik', url), disable_notification=True, parse_mode='markdown')
            photo.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)

