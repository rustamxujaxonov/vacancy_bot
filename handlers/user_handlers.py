"""
Oddiy foydalanuvchi bilan bo'ladigan barcha muloqot shu yerda:
/start, vakansiya ma'lumotlarini FSM orqali yig'ish, tasdiqlash,
to'lov cheki rasmi so'rash va admin guruhiga yuborish.
"""
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.vacancy_states import VacancyForm
from keyboards.reply import main_menu_keyboard, confirm_keyboard, cancel_keyboard
from keyboards.inline import admin_decision_keyboard
from database import db
from utils import texts
from config import ADMIN_GROUP_ID

router = Router(name="user_handlers")


# ---------------------------------------------------------------------------
# /start va asosiy menyu
# ---------------------------------------------------------------------------

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(texts.WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(F.text == "ℹ️ Yordam")
async def show_help(message: Message) -> None:
    await message.answer(texts.HELP_TEXT, parse_mode="HTML")


# Har qanday holatda "❌ Bekor qilish" bosilsa — jarayonni to'xtatamiz
@router.message(F.text == "❌ Bekor qilish", StateFilter("*"))
async def cancel_process(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(texts.CANCELLED_TEXT, reply_markup=main_menu_keyboard())


# ---------------------------------------------------------------------------
# FSM: vakansiya ma'lumotlarini bosqichma-bosqich yig'ish
# ---------------------------------------------------------------------------

@router.message(F.text == "📝 Vakansiya joylash")
async def start_vacancy_form(message: Message, state: FSMContext) -> None:
    await state.set_state(VacancyForm.position)
    await message.answer(texts.ASK_POSITION, reply_markup=cancel_keyboard())


@router.message(VacancyForm.position, F.text)
async def process_position(message: Message, state: FSMContext) -> None:
    await state.update_data(position=message.text)
    await state.set_state(VacancyForm.company)
    await message.answer(texts.ASK_COMPANY)


@router.message(VacancyForm.company, F.text)
async def process_company(message: Message, state: FSMContext) -> None:
    await state.update_data(company=message.text)
    await state.set_state(VacancyForm.salary)
    await message.answer(texts.ASK_SALARY)


@router.message(VacancyForm.salary, F.text)
async def process_salary(message: Message, state: FSMContext) -> None:
    await state.update_data(salary=message.text)
    await state.set_state(VacancyForm.requirements)
    await message.answer(texts.ASK_REQUIREMENTS)


@router.message(VacancyForm.requirements, F.text)
async def process_requirements(message: Message, state: FSMContext) -> None:
    await state.update_data(requirements=message.text)
    await state.set_state(VacancyForm.contact)
    await message.answer(texts.ASK_CONTACT)


@router.message(VacancyForm.contact, F.text)
async def process_contact(message: Message, state: FSMContext) -> None:
    await state.update_data(contact=message.text)
    data = await state.get_data()
    await state.set_state(VacancyForm.confirm)
    await message.answer(
        texts.preview_text(data), parse_mode="HTML", reply_markup=confirm_keyboard()
    )


# ---------------------------------------------------------------------------
# Tasdiqlash bosqichi -> to'lov ma'lumotlarini ko'rsatish
# ---------------------------------------------------------------------------

@router.message(VacancyForm.confirm, F.text == "✅ Tasdiqlash")
async def confirm_vacancy(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    # Vakansiyani bazaga "pending" holatida saqlaymiz
    vacancy_id = await db.add_vacancy(
        user_id=message.from_user.id,
        username=message.from_user.username,
        position=data["position"],
        company=data["company"],
        salary=data["salary"],
        requirements=data["requirements"],
        contact=data["contact"],
    )
    await state.update_data(vacancy_id=vacancy_id)
    await state.set_state(VacancyForm.waiting_receipt)

    await message.answer(
        texts.payment_instructions_text(),
        parse_mode="HTML",
        reply_markup=cancel_keyboard(),
    )


@router.message(VacancyForm.confirm, F.text == "❌ Bekor qilish")
async def reject_own_preview(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(texts.CANCELLED_TEXT, reply_markup=main_menu_keyboard())


# Agar tasdiqlash bosqichida boshqa matn yuborsa
@router.message(VacancyForm.confirm)
async def confirm_invalid(message: Message) -> None:
    await message.answer(
        "Iltimos, pastdagi tugmalardan birini tanlang: ✅ Tasdiqlash yoki ❌ Bekor qilish."
    )


# ---------------------------------------------------------------------------
# To'lov chekini qabul qilish -> admin guruhiga yuborish
# ---------------------------------------------------------------------------

@router.message(VacancyForm.waiting_receipt, F.photo)
async def process_receipt(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    vacancy_id: int = data["vacancy_id"]

    # Eng katta o'lchamdagi rasm file_id sini olamiz
    receipt_file_id = message.photo[-1].file_id
    await db.set_receipt(vacancy_id, receipt_file_id)

    caption = texts.admin_caption_text(
        data=data, user_id=message.from_user.id, username=message.from_user.username
    )

    sent_message = await bot.send_photo(
        chat_id=ADMIN_GROUP_ID,
        photo=receipt_file_id,
        caption=caption,
        parse_mode="HTML",
        reply_markup=admin_decision_keyboard(vacancy_id),
    )

    # Keyinchalik tugmalarni tahrirlash uchun xabar ID sini saqlab qo'yamiz
    await db.set_admin_group_message_id(vacancy_id, sent_message.message_id)

    await message.answer(
        "✅ Chekingiz qabul qilindi va admin ko'rib chiqishga yuborildi.\n"
        "Natija haqida sizga xabar beramiz.",
        reply_markup=main_menu_keyboard(),
    )
    await state.clear()


# Agar chek o'rniga rasm bo'lmagan narsa yuborsa
@router.message(VacancyForm.waiting_receipt)
async def process_receipt_invalid(message: Message) -> None:
    await message.answer("Iltimos, to'lov chekining rasmini (skrinshot) yuboring 📷")
