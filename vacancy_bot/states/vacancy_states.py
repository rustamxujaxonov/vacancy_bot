"""
Vakansiya joylash jarayonining FSM (Finite State Machine) holatlari.
Foydalanuvchi bosqichma-bosqich shu holatlar bo'ylab yuriladi.
"""
from aiogram.fsm.state import State, StatesGroup


class VacancyForm(StatesGroup):
    # Vakansiya ma'lumotlari
    position = State()        # Lavozim
    company = State()         # Kompaniya nomi
    salary = State()          # Maosh
    requirements = State()    # Talablar
    contact = State()         # Aloqa uchun ma'lumot

    # Tasdiqlash va to'lov bosqichlari
    confirm = State()         # Kiritilgan ma'lumotlarni tasdiqlash
    waiting_receipt = State()  # To'lov chekini kutish (rasm)
