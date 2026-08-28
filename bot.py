"""
Botni ishga tushiruvchi asosiy fayl.
Railway'da `python bot.py` (Procfile: worker) sifatida ishlaydi.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import db
from handlers import user_handlers, admin_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def on_startup() -> None:
    """Bot ishga tushishidan oldin: DB pool va jadvallarni tayyorlaymiz."""
    await db.create_pool()
    await db.create_tables()
    logger.info("Ma'lumotlar bazasi ulanishi va jadvallar tayyor.")


async def on_shutdown() -> None:
    """Bot to'xtaganda: DB pool'ni yopamiz."""
    await db.close_pool()
    logger.info("Ma'lumotlar bazasi ulanishi yopildi.")


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # FSM holatlari uchun xotirada saqlash (Railway'da bitta instance uchun yetarli).
    # Agar bir nechta instance/replica kerak bo'lsa, RedisStorage ishlatish tavsiya etiladi.
    dp = Dispatcher(storage=MemoryStorage())

    # Routerlarni ro'yxatdan o'tkazamiz
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)

    # Startup/shutdown hook'lari
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Eski (webhook orqali qolgan) update'larni tashlab, pollingni boshlaymiz
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")
