"""
PostgreSQL (asyncpg) bilan ishlash uchun barcha funksiyalar.
Railway PostgreSQL plugin bilan to'g'ridan-to'g'ri ishlaydi (DATABASE_URL orqali).

Bitta global connection pool ishlatiladi — bu Railway kabi muhitlarda
ko'p so'rovlarni samarali va xavfsiz boshqarish imkonini beradi.
"""
import asyncpg
from typing import Optional

from config import DATABASE_URL

# Global pool — bot.py ichida on_startup paytida yaratiladi
pool: Optional[asyncpg.Pool] = None


async def create_pool() -> None:
    """Ilova ishga tushganda chaqiriladi: connection pool yaratadi."""
    global pool
    pool = await asyncpg.create_pool(dsn=DATABASE_URL, min_size=1, max_size=10)


async def close_pool() -> None:
    """Ilova to'xtaganda pool'ni yopadi."""
    global pool
    if pool is not None:
        await pool.close()


async def create_tables() -> None:
    """
    Kerakli jadvallarni yaratadi (agar mavjud bo'lmasa).
    Bot har safar ishga tushganda chaqiriladi — xavfsiz, chunki
    IF NOT EXISTS ishlatilgan.
    """
    query = """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        username TEXT,
        position TEXT NOT NULL,
        company TEXT NOT NULL,
        salary TEXT NOT NULL,
        requirements TEXT NOT NULL,
        contact TEXT NOT NULL,
        receipt_file_id TEXT,
        status TEXT NOT NULL DEFAULT 'pending',  -- pending / approved / rejected
        admin_group_message_id BIGINT,           -- admin guruhidagi xabar ID (tugmalarni tahrirlash uchun)
        channel_message_id BIGINT,               -- kanalga chop etilgan xabar ID
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """
    async with pool.acquire() as conn:
        await conn.execute(query)


# ---------------------------------------------------------------------------
# CRUD funksiyalar
# ---------------------------------------------------------------------------

async def add_vacancy(
    user_id: int,
    username: str | None,
    position: str,
    company: str,
    salary: str,
    requirements: str,
    contact: str,
) -> int:
    """Yangi vakansiya yozuvini yaratadi va uning ID sini qaytaradi."""
    query = """
    INSERT INTO vacancies (user_id, username, position, company, salary, requirements, contact)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    RETURNING id;
    """
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            query, user_id, username, position, company, salary, requirements, contact
        )
        return row["id"]


async def set_receipt(vacancy_id: int, receipt_file_id: str) -> None:
    """Foydalanuvchi yuborgan to'lov cheki file_id sini saqlaydi."""
    query = "UPDATE vacancies SET receipt_file_id = $1 WHERE id = $2;"
    async with pool.acquire() as conn:
        await conn.execute(query, receipt_file_id, vacancy_id)


async def set_admin_group_message_id(vacancy_id: int, message_id: int) -> None:
    """Admin guruhiga yuborilgan xabar ID sini saqlaydi (keyin tahrirlash uchun)."""
    query = "UPDATE vacancies SET admin_group_message_id = $1 WHERE id = $2;"
    async with pool.acquire() as conn:
        await conn.execute(query, message_id, vacancy_id)


async def set_status(vacancy_id: int, status: str) -> None:
    """Vakansiya holatini yangilaydi: pending / approved / rejected."""
    query = "UPDATE vacancies SET status = $1 WHERE id = $2;"
    async with pool.acquire() as conn:
        await conn.execute(query, status, vacancy_id)


async def set_channel_message_id(vacancy_id: int, message_id: int) -> None:
    """Kanalga chop etilgandan keyin xabar ID sini saqlaydi."""
    query = "UPDATE vacancies SET channel_message_id = $1 WHERE id = $2;"
    async with pool.acquire() as conn:
        await conn.execute(query, message_id, vacancy_id)


async def get_vacancy(vacancy_id: int) -> Optional[asyncpg.Record]:
    """Bitta vakansiyani ID bo'yicha oladi."""
    query = "SELECT * FROM vacancies WHERE id = $1;"
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, vacancy_id)


async def get_user_vacancies(user_id: int) -> list[asyncpg.Record]:
    """Foydalanuvchining barcha vakansiyalari tarixini oladi."""
    query = "SELECT * FROM vacancies WHERE user_id = $1 ORDER BY created_at DESC;"
    async with pool.acquire() as conn:
        return await conn.fetch(query, user_id)
