import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.buttons.text import all_active_tasks
from bot.dispatcher import dp


@dp.message_handler(text=all_active_tasks)
async def show_manager_companies(msg: types.Message, state: FSMContext):
    response = requests.get(f"http://127.0.0.1:8005/api/telegram-users/manager-companies/{msg.from_user.id}/")
    companies = response.json()
    if not companies:
        await msg.answer("❌ Вы не являетесь менеджером ни в одной компании.")
        return

    buttons = [[types.InlineKeyboardButton(text=comp['name'], callback_data=f"manager_company_{comp['id']}")] for comp
               in companies]
    await msg.answer("🏢 Выберите компанию:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))


@dp.callback_query_handler(lambda c: c.data.startswith("manager_company_"))
async def show_company_tasks(call: types.CallbackQuery):
    company_id = int(call.data.split("_")[-1])
    await call.message.delete()
    response = requests.get(f"http://127.0.0.1:8005/api/tasks/tasks/by-company/{company_id}/")
    tasks = response.json()

    if not tasks:
        await call.message.answer("✅ В этой компании пока нет задач.")
        return

    for task in tasks:
        text = f"""📝 <b>{task['title']}</b>
📅 Deadline: {task['deadline']}
🎁 Reward: {task['reward']}
⚠️ Penalty: {task['penalty']}
👤 Сотрудник: {task['user_name']}
📌 Статус: {task['status']}"""
        await call.message.answer(
            text=text,
            parse_mode="HTML",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_task_{task['id']}")
            )
        )
    await call.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("delete_task_"))
async def delete_task(call: types.CallbackQuery):
    task_id = int(call.data.split("_")[-1])
    response = requests.delete(f"http://127.0.0.1:8005/api/tasks/tasks/{task_id}/delete/")
    await call.message.delete()
    if response.status_code in [200, 204]:
        await call.message.answer("✅ Задача успешно удалена.")
    else:
        await call.message.answer("❗ Ошибка при удалении задачи.")
    await call.answer()
