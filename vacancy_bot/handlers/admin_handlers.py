"""
Admin guruhidagi inline tugmalarni (✅ Chop etish / ❌ Rad etish) qayta ishlaydi.
- ✅ bosilsa: vakansiya kartasi kanalga chop etiladi, foydalanuvchiga xabar boradi.
- ❌ bosilsa: vakansiya rad etiladi, foydalanuvchiga xabar boradi.

Ikkala holatda ham admin guruhidagi xabar tugmalarsiz, natija bilan yangilanadi —
shu orqali boshqa adminlar allaqachon ko'rib chiqilganini bilib oladi.
"""
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery

from database import db
from utils import texts
from config import CHANNEL_ID, ADMIN_GROUP_ID

router = Router(name="admin_handlers")

# Faqat ADMIN_GROUP_ID guruhidan kelgan callbacklarni qabul qilamiz (xavfsizlik uchun)
router.callback_query.filter(F.message.chat.id == ADMIN_GROUP_ID)


@router.callback_query(F.data.startswith("approve:"))
async def approve_vacancy(callback: CallbackQuery, bot: Bot) -> None:
    vacancy_id = int(callback.data.split(":")[1])
    vacancy = await db.get_vacancy(vacancy_id)

    if vacancy is None:
        await callback.answer("❗ Vakansiya topilmadi (bazadan o'chirilgan bo'lishi mumkin).", show_alert=True)
        return

    if vacancy["status"] != "pending":
        await callback.answer("Bu vakansiya allaqachon ko'rib chiqilgan.", show_alert=True)
        return

    # Kanalga tayyor vakansiya kartasini chop etamiz
    channel_message = await bot.send_message(
        chat_id=CHANNEL_ID,
        text=texts.vacancy_card_text(vacancy),
        parse_mode="HTML",
    )

    await db.set_status(vacancy_id, "approved")
    await db.set_channel_message_id(vacancy_id, channel_message.message_id)

    # Admin guruhidagi xabarni yangilaymiz — tugmalarni olib tashlab, natijani yozamiz
    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n✅ <b>CHOP ETILDI</b>",
        parse_mode="HTML",
        reply_markup=None,
    )

    # Foydalanuvchiga bildirishnoma yuboramiz
    await bot.send_message(chat_id=vacancy["user_id"], text=texts.APPROVED_USER_TEXT)

    await callback.answer("✅ Kanalga chop etildi!")


@router.callback_query(F.data.startswith("reject:"))
async def reject_vacancy(callback: CallbackQuery, bot: Bot) -> None:
    vacancy_id = int(callback.data.split(":")[1])
    vacancy = await db.get_vacancy(vacancy_id)

    if vacancy is None:
        await callback.answer("❗ Vakansiya topilmadi (bazadan o'chirilgan bo'lishi mumkin).", show_alert=True)
        return

    if vacancy["status"] != "pending":
        await callback.answer("Bu vakansiya allaqachon ko'rib chiqilgan.", show_alert=True)
        return

    await db.set_status(vacancy_id, "rejected")

    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n❌ <b>RAD ETILDI</b>",
        parse_mode="HTML",
        reply_markup=None,
    )

    await bot.send_message(chat_id=vacancy["user_id"], text=texts.REJECTED_USER_TEXT)

    await callback.answer("❌ Vakansiya rad etildi.")
