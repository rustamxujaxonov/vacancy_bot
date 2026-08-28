# Vakansiya E'lon Bot

Aiogram 3.x + asyncpg (PostgreSQL) + Railway uchun tayyor loyiha.

## Fayl tuzilishi

```
vacancy_bot/
├── bot.py                     # Botni ishga tushiruvchi asosiy fayl
├── config.py                  # Sozlamalar (.env dan o'qiydi)
├── requirements.txt
├── Procfile                   # Railway uchun
├── .env.example
├── database/
│   ├── __init__.py
│   └── db.py                  # asyncpg pool, jadval yaratish, CRUD funksiyalar
├── states/
│   ├── __init__.py
│   └── vacancy_states.py      # FSM holatlari
├── keyboards/
│   ├── __init__.py
│   ├── inline.py               # Inline tugmalar (admin, tasdiqlash va h.k.)
│   └── reply.py                 # Reply tugmalar (asosiy menyu)
├── handlers/
│   ├── __init__.py
│   ├── user_handlers.py         # /start, vakansiya FSM oqimi, chek yuborish
│   └── admin_handlers.py        # Admin guruhidagi Chop etish/Rad etish tugmalari
└── utils/
    ├── __init__.py
    └── texts.py                 # Xabar matnlari va vakansiya kartasi shabloni
```

## Railway'da sozlash

1. Railway'da PostgreSQL plugin qo'shing — u avtomatik `DATABASE_URL` environment
   o'zgaruvchisini beradi.
2. Loyihani deploy qiling (GitHub repo yoki Railway CLI orqali).
3. Railway "Variables" bo'limida quyidagilarni kiriting:
   - `BOT_TOKEN` — BotFather'dan olingan token
   - `ADMIN_GROUP_ID` — chek va e'lonlar tekshiriladigan guruh ID (masalan -1001234567890)
   - `CHANNEL_ID` — e'lonlar chop etiladigan kanal ID (masalan -1009876543210)
   - `CARD_NUMBER` — to'lov qabul qilinadigan karta raqami
   - `CARD_OWNER` — karta egasining F.I.Sh
   - `PAYMENT_AMOUNT` — to'lov summasi (masalan "50 000 so'm")
   - `DATABASE_URL` — Railway Postgres avtomatik beradi (agar bermasa, o'zingiz qo'shing)
4. Bot ishga tushganda `database/db.py` ichidagi `create_tables()` avtomatik
   jadvallarni yaratadi — qo'lda migratsiya kerak emas.
5. Botni guruhga admin qilib qo'shing (xabar yuborishi va tugmalarni tahrirlashi uchun),
   kanalga esa post qilish huquqi bilan admin qilib qo'shing.

## Ishga tushirish (lokal)

```bash
pip install -r requirements.txt
cp .env.example .env   # va qiymatlarni to'ldiring
python bot.py
```
