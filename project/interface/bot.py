from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
load_dotenv()
import asyncio
import logging
from interface.config import tokenbot
from interface.logging_config import setup_logger
from SQL.db import init_db
import app.handlers

bot = Bot(token=tokenbot)
dp = Dispatcher()
dp.include_router(app.handlers.router)
setup_logger()
init_db()

logger = logging.getLogger(__name__)

async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())




