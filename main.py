from dotenv import load_dotenv
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
import asyncio

# routers imports
from app.handlers import router

# get the env variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
# write the main of bot
bot = Bot(token=TOKEN)
dp = Dispatcher()


# main func
async def main():
    # await bot(DeleteWebhook(drop_pending_updates=True))
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')