"""
Loyihaning barcha sozlamalari shu yerda, .env fayldan o'qiladi.
Railway'da bu qiymatlar "Variables" bo'limidan environment sifatida keladi,
shuning uchun os.getenv ishlatilgan (agar .env fayl bo'lmasa ham xato bermaydi).
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Bot ---
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

# --- Guruh va kanal ---
# int() ga o'tkazamiz, chunki Telegram chat ID lari manfiy butun sonlar
ADMIN_GROUP_ID: int = int(os.getenv("ADMIN_GROUP_ID", "0"))
CHANNEL_ID: int = int(os.getenv("CHANNEL_ID", "0"))

# --- To'lov ma'lumotlari ---
CARD_NUMBER: str = os.getenv("CARD_NUMBER", "0000 0000 0000 0000")
CARD_OWNER: str = os.getenv("CARD_OWNER", "F.I.Sh")
PAYMENT_AMOUNT: str = os.getenv("PAYMENT_AMOUNT", "0 so'm")

# --- Ma'lumotlar bazasi ---
# Railway PostgreSQL plugin qo'shilganda DATABASE_URL avtomatik beriladi
DATABASE_URL: str = os.getenv("DATABASE_URL", "")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment o'zgaruvchisi topilmadi! .env faylni tekshiring.")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment o'zgaruvchisi topilmadi! PostgreSQL ulanmagan.")
