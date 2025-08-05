import httpx
from aiogram import types
from bot.config import get_user_by_chat_id, get_user_by_id, get_task_by_id
from bot.dispatcher import dp
from bot.buttons.text import active_tasks
from bot.buttons.inline_buttons import complete_task_button

TASK_LIST_API = "http://127.0.0.1:8005/api/tasks/my-tasks/"


@dp.message_handler(text=active_tasks)
async def list_employee_tasks(msg: types.Message):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{TASK_LIST_API}?chat_id={msg.from_user.id}")
        if res.status_code != 200 or not res.json():
            await msg.answer("❌ У вас нет активных задач.")
            return

        tasks = res.json()
        for task in tasks:
            text = f"""📌 <b>{task['title']}</b>
📝 {task.get('description', '—')}
🏢 Компания: {task['company_name']}
🗓 Дедлайн: {task['deadline']}
🎁 Бонус: {task['reward']}
⚠️ Штраф: {task['penalty']}
📊 Статус: {task['status']}"""
            await msg.answer(text, reply_markup=complete_task_button(task['id']), parse_mode="HTML")


@dp.callback_query_handler(lambda c: c.data.startswith("complete_task_"))
async def mark_task_complete(call: types.CallbackQuery):
    task_id = int(call.data.split("_")[-1])
    task = await get_task_by_id(task_id)
    user = await get_user_by_chat_id(call.from_user.id)

    if not task or not task.company:
        await call.message.answer("❌ Задача или компания не найдены.")
        await call.answer()
        return

    async with httpx.AsyncClient() as client:
        # Kompaniya haqida ma'lumot olish
        comp_resp = await client.get(f"http://127.0.0.1:8005/api/companies/companies/{task.company.id}/")
        if comp_resp.status_code != 200:
            await call.message.answer("❌ Ошибка при получении данных о компании.")
            await call.answer()
            return

        comp = comp_resp.json()

        # Task ni bajarilgan deb belgilash
        complete_resp = await client.get(f"http://127.0.0.1:8005/api/tasks/tasks/{task_id}/complete/")
        if complete_resp.status_code not in [200, 202]:
            await call.message.answer("❗ Произошла ошибка при отметке задачи.")
            await call.answer()
            return

        await call.message.edit_reply_markup()
        await call.message.answer("✅ Задача отмечена как выполненная.")

        for manager_id in comp.get("managers", []):
            manager = await get_user_by_id(manager_id)
            await call.bot.send_message(
                manager.chat_id,
    f"""✅ <b>Сотрудник выполнил задачу</b>

📌 <b>Название:</b> {task.title}
📝 <b>Описание:</b> {task.description or "—"}
🏢 <b>Компания:</b> {comp.get("name", "—")}
🗓 <b>Дедлайн:</b> {task.deadline}
📊 <b>Статус:</b> {task.status}

🎁 <b>Бонус за выполнение:</b> {task.reward}
⚠️ <b>Штраф за невыполнение:</b> {task.penalty}

───────────────

👤 <b>Сотрудник:</b> {user.full_name}
🔗 <b>Юзернейм:</b> @{user.username or "—"}
📞 <b>Телефон:</b> {user.phone_number or "—"}
🧮 <b>Текущие баллы:</b> {user.point}
⚠️ <b>Накопленные штрафы:</b> {user.fine}
🆔 <b>Telegram ID:</b> {user.chat_id}
""",
                parse_mode="HTML"
            )

    await call.answer()
