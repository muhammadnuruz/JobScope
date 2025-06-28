from aiogram import types
from aiogram.dispatcher import FSMContext
import requests

from bot.buttons.reply_buttons import back_main_menu_button, main_menu_buttons
from bot.dispatcher import dp, bot
from bot.buttons.text import create_task

TASK_CREATE_API = "http://127.0.0.1:8005/api/tasks/tasks/"


@dp.message_handler(text=create_task)
async def start_task_creation(msg: types.Message, state: FSMContext):
    response = requests.get(f"http://127.0.0.1:8005/api/telegram-users/manager-companies/{msg.from_user.id}/")
    if response.status_code != 200 or not response.json():
        await msg.answer("❌ Вы не являетесь менеджером ни в одной компании.")
        return

    companies = response.json()
    buttons = [[types.InlineKeyboardButton(text=c['name'], callback_data=f"select_company_{c['id']}")] for c in
               companies]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await msg.answer("🏢 Выберите компанию:", reply_markup=markup)
    await state.set_state("selecting_company")


@dp.callback_query_handler(lambda c: c.data.startswith("select_company_"), state="selecting_company")
async def select_company(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(reply_markup=await back_main_menu_button(), text="👤 Выберите сотрудника:")
    company_id = int(call.data.split("_")[-1])
    await state.update_data(company_id=company_id)
    await call.message.delete()
    employees = requests.get(f"http://127.0.0.1:8005/api/telegram-users/employees/{company_id}/").json()
    if not employees:
        await call.message.answer("❌ В этой компании нет обычных сотрудников.")
        return

    buttons = [[types.InlineKeyboardButton(text=e['full_name'], callback_data=f"select_employee_{e['id']}")] for e in
               employees]
    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.answer("👤 Выберите сотрудника:", reply_markup=markup)
    await state.set_state("selecting_employee")
    await call.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("select_employee_"), state="selecting_employee")
async def select_employee(call: types.CallbackQuery, state: FSMContext):
    employee_id = int(call.data.split("_")[-1])
    await call.message.delete()
    await state.update_data(user_id=employee_id)
    await call.message.answer("✏️ Введите название задания:")
    await state.set_state("task_title")
    await call.answer()


@dp.message_handler(state="task_title")
async def get_title(msg: types.Message, state: FSMContext):
    await state.update_data(title=msg.text)
    await msg.answer("📝 Введите описание задания:")
    await state.set_state("task_description")


@dp.message_handler(state="task_description")
async def get_description(msg: types.Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer("🗓 Введите дедлайн (например: 2025-07-01):")
    await state.set_state("task_deadline")


@dp.message_handler(state="task_deadline")
async def get_deadline(msg: types.Message, state: FSMContext):
    await state.update_data(deadline=msg.text)
    await msg.answer("🎁 Введите количество бонусных баллов:")
    await state.set_state("task_reward")


@dp.message_handler(state="task_reward")
async def get_reward(msg: types.Message, state: FSMContext):
    try:
        reward = int(msg.text)
    except ValueError:
        await msg.answer("⚠️ Пожалуйста, введите число.")
        return
    await state.update_data(reward=reward)
    await msg.answer("⚠️ Введите количество штрафных баллов:")
    await state.set_state("task_penalty")


@dp.message_handler(state="task_penalty")
async def get_penalty(msg: types.Message, state: FSMContext):
    try:
        penalty = int(msg.text)
    except ValueError:
        await msg.answer("⚠️ Пожалуйста, введите число.")
        return

    await state.update_data(penalty=penalty)
    data = await state.get_data()

    payload = {
        "user": data["user_id"],
        "company": data["company_id"],
        "title": data["title"],
        "description": data["description"],
        "deadline": data["deadline"],
        "reward": data["reward"],
        "penalty": data["penalty"]
    }
    response = requests.post(TASK_CREATE_API, data=payload)
    res_user = requests.get(f"http://127.0.0.1:8005/api/telegram-users/detail/{data['user_id']}").json()
    res_company = requests.get(f"http://127.0.0.1:8005/api/companies/companies/{data['company_id']}/").json()
    try:
        await bot.send_message(chat_id=res_user["chat_id"], text=f"""
🆕 Вам назначена новая задача!

🏢 Компания: {res_company['name']}
📌 Задача: {data['title']}
📋 Описание: {data['description']}
📆 Дедлайн: {data['deadline']}
🎁 Бонусные баллы: {data['reward']}
⚠️ Штрафные баллы: {data['penalty']}
""")
    except Exception:
        pass
    if response.status_code in [200, 201]:
        await msg.answer("✅ Задание успешно создано!", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer("❗ Произошла ошибка при создании задания.",
                         reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()
