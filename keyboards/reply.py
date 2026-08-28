"""Oddiy reply (asosiy menyu) tugmalari."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Botning asosiy menyusi — vakansiya joylashni boshlash tugmasi."""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📝 Vakansiya joylash"))
    builder.add(KeyboardButton(text="ℹ️ Yordam"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def confirm_keyboard() -> ReplyKeyboardMarkup:
    """Kiritilgan ma'lumotlarni tasdiqlash uchun reply tugmalar."""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="✅ Tasdiqlash"))
    builder.add(KeyboardButton(text="❌ Bekor qilish"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard() -> ReplyKeyboardMarkup:
    """FSM davomida istalgan vaqtda bekor qilish uchun."""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="❌ Bekor qilish"))
    return builder.as_markup(resize_keyboard=True)
