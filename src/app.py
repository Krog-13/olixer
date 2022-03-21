import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_KEY
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_KEY)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_message(message: types.Message):
    await message.reply("Hi everybody")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
