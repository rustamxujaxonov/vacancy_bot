"""
Barcha statik matnlar va shablonlar shu yerda — handler fayllarini
toza saqlash va matnlarni bitta joydan boshqarish uchun.
"""
from config import CARD_NUMBER, CARD_OWNER, PAYMENT_AMOUNT


WELCOME_TEXT = (
    "👋 Assalomu alaykum!\n\n"
    "Bu bot orqali siz vakansiya (ish o'rni) e'lonini bizning kanalimizda "
    "chop etishingiz mumkin.\n\n"
    "Boshlash uchun pastdagi \"📝 Vakansiya joylash\" tugmasini bosing."
)

HELP_TEXT = (
    "ℹ️ <b>Bot qanday ishlaydi:</b>\n\n"
    "1️⃣ Vakansiya ma'lumotlarini kiritasiz (lavozim, kompaniya, maosh, talablar, aloqa)\n"
    "2️⃣ Ma'lumotlarni tasdiqlaysiz\n"
    "3️⃣ Ko'rsatilgan karta raqamiga to'lov qilib, chek rasmini yuborasiz\n"
    "4️⃣ Admin chekni tekshiradi va vakansiyangizni tasdiqlaydi yoki rad etadi\n"
    "5️⃣ Tasdiqlansa, e'lon avtomatik kanalga chop etiladi ✅"
)

ASK_POSITION = "1️⃣ Lavozim nomini kiriting (masalan: Python dasturchi):"
ASK_COMPANY = "2️⃣ Kompaniya nomini va manzilni kiriting (viloyat yoki shaxar) kiriting:"
ASK_SALARY = "3️⃣ Maoshni kiriting (masalan: 5 000 000 - 8 000 000 so'm):"
ASK_REQUIREMENTS = "4️⃣ Talablarni kiriting (tajriba, ko'nikmalar, yosh chegarasi va h.k.):"
ASK_CONTACT = "5️⃣ Aloqa uchun ma'lumot kiriting (telefon raqam yoki username):"

CANCELLED_TEXT = "❌ Jarayon bekor qilindi. Qaytadan boshlash uchun /start bosing."


def preview_text(data: dict) -> str:
    """Foydalanuvchi kiritgan ma'lumotlarni tasdiqlash oldidan ko'rsatish uchun."""
    return (
        "📋 <b>Kiritilgan ma'lumotlar:</b>\n\n"
        f"💼 <b>Lavozim:</b> {data['position']}\n"
        f"🏢 <b>Kompaniya:</b> {data['company']}\n"
        f"💰 <b>Maosh:</b> {data['salary']}\n"
        f"📌 <b>Talablar:</b> {data['requirements']}\n"
        f"📞 <b>Aloqa:</b> {data['contact']}\n\n"
        "Ma'lumotlar to'g'rimi?"
    )


def payment_instructions_text() -> str:
    """To'lov qilish bo'yicha yo'riqnoma va karta ma'lumotlari."""
    return (
        "💳 <b>To'lovni amalga oshiring</b>\n\n"
        f"Summasi: <b>{PAYMENT_AMOUNT}</b>\n"
        f"Karta raqami: <code>{CARD_NUMBER}</code>\n"
        f"Karta egasi: <b>{CARD_OWNER}</b>\n\n"
        f"Eslatma to'lovni qilib bo'lgach arizangiz tekshiriladi agar muammo bo'lsa to'lov qaytariladi aloqa uchun admin @dontrustamf\n"
        "To'lovni amalga oshirgach, chek (skrinshot) rasmini shu yerga yuboring 👇"
    )


def vacancy_card_text(data: dict, with_status: bool = False) -> str:
    """
    Admin guruhiga va kanalga yuboriladigan tayyor vakansiya e'lon kartasi.
    `data` — asyncpg.Record yoki dict bo'lishi mumkin (ikkalasida ham kalit orqali murojaat qilinadi).
    """
    text = (
        "📢 <b>YANGI VAKANSIYA</b>\n\n"
        f"💼 <b>Lavozim:</b> {data['position']}\n"
        f"🏢 <b>Kompaniya:</b> {data['company']}\n"
        f"💰 <b>Maosh:</b> {data['salary']}\n"
        f"📌 <b>Talablar:</b> {data['requirements']}\n"
        f"📞 <b>Aloqa:</b> {data['contact']}\n"
    )
    return text


def admin_caption_text(data: dict, user_id: int, username: str | None) -> str:
    """Admin guruhiga chek bilan birga yuboriladigan caption (foydalanuvchi ma'lumoti bilan)."""
    user_line = f"@{username}" if username else f"ID: {user_id}"
    return (
        f"🆕 <b>Yangi vakansiya so'rovi</b> (yuboruvchi: {user_line})\n\n"
        + vacancy_card_text(data)
        + "\n💳 Yuqoridagi chekni tekshirib, qarorni tugma orqali tanlang."
    )


APPROVED_USER_TEXT = "✅ Tabriklaymiz! Sizning vakansiyangiz tasdiqlandi va kanalga chop etildi."
REJECTED_USER_TEXT = (
    "❌ Afsuski, sizning to'lovingiz yoki vakansiyangiz admin tomonidan rad etildi.\n"
    "Savollar bo'lsa, to'lovni qaytarmoqchi bo'lsangiz administrator bilan bog'laning. @dontrustamf"
)
