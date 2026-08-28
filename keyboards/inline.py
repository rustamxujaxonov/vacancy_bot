"""
Inline tugmalar. callback_data formatida vacancy_id ham yuboriladi,
shunda admin_handlers.py qaysi vakansiya haqida gap ketayotganini biladi.
"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_decision_keyboard(vacancy_id: int) -> InlineKeyboardMarkup:
    """
    Admin guruhiga yuboriladigan tugmalar:
    ✅ Chop etish  — kanalga post qiladi
    ❌ Rad etish   — foydalanuvchiga rad javobini yuboradi
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Chop etish", callback_data=f"approve:{vacancy_id}")
    builder.button(text="❌ Rad etish", callback_data=f"reject:{vacancy_id}")
    builder.adjust(2)
    return builder.as_markup()
