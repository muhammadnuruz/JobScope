from aiogram import types
import requests

from bot.dispatcher import dp
from bot.buttons.text import active_tasks
from bot.buttons.inline_buttons import complete_task_button

TASK_LIST_API = "http://127.0.0.1:8005/api/tasks/my-tasks/"


@dp.message_handler(text=active_tasks)
async def list_employee_tasks(msg: types.Message):
    res = requests.get(f"{TASK_LIST_API}?chat_id={msg.from_user.id}")
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
    res = requests.get(f"http://127.0.0.1:8005/api/tasks/tasks/{task_id}/complete/")
    if res.status_code in [200, 202]:
        await call.message.edit_reply_markup()
        await call.message.answer("✅ Задача отмечена как выполненная.")
    else:
        await call.message.answer("❗ Произошла ошибка при отметке задачи.")
    await call.answer()
