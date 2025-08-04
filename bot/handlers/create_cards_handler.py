from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from ..buttons.reply_buttons import back_main_menu_button, main_menu_buttons
from ..buttons.text import add_card
from ..config import save_card_to_db
from ..dispatcher import dp


@dp.message_handler(Text(equals=add_card))
async def add_card_function(msg: Message, state: FSMContext):
    await msg.answer("📎 Отправьте фотографию товара:", reply_markup=await back_main_menu_button())
    await state.set_state("card_photo")


@dp.message_handler(content_types=["photo"], state="card_photo")
async def get_card_photo(msg: Message, state: FSMContext):
    photo = msg.photo[-1].file_id
    await state.update_data(photo=photo)
    await msg.answer("📝 Введите название товара:")
    await state.set_state("card_name")


@dp.message_handler(state="card_name")
async def get_card_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("💰 Введите цену товара (только число):")
    await state.set_state("card_price")


@dp.message_handler(state="card_price")
async def get_card_price(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer("❗️ Пожалуйста, введите только число.")
        return

    user_data = await state.get_data()
    price = int(msg.text)

    await save_card_to_db(
        chat_id=msg.from_user.id,
        imageUrl=user_data['photo'],
        name=user_data['name'],
        price=price
    )

    await msg.answer("✅ Карта успешно добавлена.", reply_markup=await main_menu_buttons(chat_id=msg.from_user.id))
    await state.finish()
