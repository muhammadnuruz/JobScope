from datetime import datetime

import requests

USER_LIST_API = "http://127.0.0.1:8005/api/telegram-users/"
DEBT_LIST_API = "http://127.0.0.1:8005/api/debts/"
DEBT_DELETE_API = "http://127.0.0.1:8005/api/debts/delete/"


async def delete_expired_debts():
    try:
        users_resp = requests.get(USER_LIST_API)
        if users_resp.status_code != 200:
            print("❌ Foydalanuvchilarni olishda xatolik.")
            return

        users = users_resp.json()

        for user in users['results']:
            chat_id = user["chat_id"]

            debts_resp = requests.get(DEBT_LIST_API, params={"chat_id": chat_id})
            if debts_resp.status_code != 200:
                continue

            debts = debts_resp.json().get("results", [])
            for debt in debts:
                deadline = debt.get("deadline")
                try:
                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
                    if deadline_date < datetime.today().date():
                        requests.delete(f"{DEBT_DELETE_API}{debt['id']}/")
                        print(f"🗑 Qarz o'chirildi: {debt['borrower_name']}")
                except Exception as e:
                    print("🛑 Sana xatosi:", e)

    except Exception as e:
        print("Xatolik:", e)
