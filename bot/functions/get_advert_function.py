import os
import re
import shutil
from datetime import datetime
from typing import List, Dict
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from dateutil.relativedelta import relativedelta
from UzTransliterator import UzTransliterator

import requests

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

admin_chat_id = -4044486187
from bot.dispatcher import Config, bot


class AIProductManager:
    def __init__(self):
        self.api_url = Config.URL
        self.bot = bot
        self.admin = 1974800905
        self.user_id = None
        self.token = None
        self.login_data = {
            "method": "login",
            "auth": {
                "login": Config.LOGIN,
                "password": Config.PASSWORD
            }
        }
        self.items = None
        self.orders = None
        self.users = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.persistent_directory = os.path.join(self.current_dir, "db", "chroma_db")
        self.transliterator = UzTransliterator.UzTransliterator()

    def _get_item_data(self):
        return {
            "auth": {
                "userId": self.user_id,
                "token": self.token
            },
            "method": "getProduct",
        }

    def _get_price_data(self):
        return {
            "auth": {
                "userId": self.user_id,
                "token": self.token
            },
            "method": "getPrice",
            "params": {
                "priceType": {
                    "SD_id": "d0_3",
                    "code_1C": "code_1c"
                }
            }
        }

    def _get_clients_data(self):
        return {
            "auth": {
                "userId": self.user_id,
                "token": self.token
            },
            "method": "getClient",

        }

    def _get_orders_data(self):
        return {
            "auth": {
                "userId": self.user_id,
                "token": self.token
            },
            "method": "getOrder",
        }

    async def login(self):
        response = requests.post(
            url=self.api_url,
            json=self.login_data,
        )
        result = response.json()
        response_users = requests.get("http://127.0.0.1:8005/api/telegram-users/")
        users = response_users.json().get("results", [])
        self.users = users
        if result['status'] is True:
            self.user_id = result['result']['userId']
            self.token = result['result']["token"]
        else:
            await self.bot.send_message(chat_id=self.admin, text="❌ Login muvaffaqiyatsiz!: {}".format(response.text))

    async def get_category(self):
        data = {
            "auth": {
                "userId": self.user_id,
                "token": self.token
            },
            "method": "getProductCategory",
            "params": {
                "page": 1,
                "limit": 1000
            }
        }
        response = requests.get(
            self.api_url,
            json=data
        )
        result = response.json()
        all_categories = []
        if result['status'] is True:
            for category in result['result']['productCategory']:
                all_categories.append({"CS_id": category["CS_id"], "name": category['name']})
            return all_categories
        else:
            return None

    async def get_prices(self):
        data = self._get_price_data()
        response = requests.get(
            self.api_url,
            json=data
        )
        result = response.json()
        if result['status'] is True:
            lst = result['result']
            prices = {price['product']["CS_id"]: price["price"] for price in lst}
            return prices
        else:
            await self.bot.send_message(chat_id=self.admin,
                                        text="❌ Narxlarni olish muvaffaqiyatsiz!: {}".format(response.text))
            return None

    async def get_items(self):
        page = 1
        all_items = []
        while True:
            data = self._get_item_data()
            data["params"] = {
                "page": page,
                "limit": 1000
            }

            try:
                response = requests.get(
                    url=self.api_url,
                    json=data
                )
                result = response.json()
            except Exception as e:
                await self.bot.send_message(
                    chat_id=self.admin,
                    text=f"❌ API xatolik yuz berdi: {e}"
                )
                return None

            if result.get("status") is True:
                items = result['result'].get('product', [])

                if not items:
                    break

                all_items.extend(items)
                page += 1
            else:
                await self.bot.send_message(
                    chat_id=self.admin,
                    text=f"❌ Tovarlarni olish muvaffaqiyatsiz!: {response.text}"
                )
                return None

        prices = await self.get_prices()
        if prices is None:
            return None

        item_list = []
        for item in all_items:
            if item.get("active") == "N":
                continue
            cs_id = item.get("CS_id")
            name = item.get("name")
            imageUrl = item.get("imageUrl")
            price = prices.get(cs_id)
            item_list.append({
                "id": cs_id,
                "name": name,
                "price": price,
                "imageUrl": imageUrl,

            })
        self.items = item_list
        return item_list

    def get_items_by_cs_id(self, top_items: list):
        return [item for item in self.items if item.get("id") in top_items]

    def normalize_phone(self, phone):
        if not phone:
            return None
        digits = re.sub(r'\D', '', phone)

        if digits.startswith("998") and len(digits) == 12:
            return digits
        elif len(digits) == 9:
            return "998" + digits
        elif digits.startswith("00998") and len(digits) == 14:
            return digits[2:]
        else:
            return None

    async def get_clients(self):
        page = 1
        all_clients = []

        while True:
            data = self._get_clients_data()
            data["params"] = {
                "page": page,
                "limit": 1000
            }

            try:
                response = requests.get(
                    url=self.api_url,
                    json=data
                )
                result = response.json()
            except Exception as e:
                await self.bot.send_message(
                    chat_id=self.admin,
                    text=f"❌ API xatolik yuz berdi (client): {e}"
                )
                return None

            if result.get('status') is True:
                clients = result['result'].get('client', [])

                if not clients:
                    break

                all_clients.extend(clients)
                page += 1
            else:
                await self.bot.send_message(
                    chat_id=self.admin,
                    text="❌ Mijoznlarni olish muvaffaqiyatsiz!: {}".format(response.text)
                )
                return None

        return [
            client for client in all_clients
            if client.get("active") == "Y"
        ]

    async def get_orders(self):
        page = 1
        all_orders = []
        now = datetime.now()

        three_months_ago_start = (
                now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - relativedelta(months=3))

        date_from = three_months_ago_start.strftime("%Y-%m-%d %H:%M:%S")
        date_to = now.strftime("%Y-%m-%d %H:%M:%S")
        while True:
            data = self._get_orders_data()
            data["params"] = {
                "page": page,
                "limit": 1000,
                "filter": {
                    "include": "all",
                    "status": [1, 2, 3],
                    "period": {
                        "dateCreate": {
                            "from": date_from,
                            "to": date_to
                        }
                    }
                }
            }

            try:
                response = requests.get(
                    url=self.api_url,
                    json=data
                )
                result = response.json()
            except Exception as e:
                await self.bot.send_message(
                    chat_id=self.admin,
                    text=f"❌ Buyurtmalarni olishda xatolik!: {e}"
                )
                return None

            if not result.get("status"):
                await self.bot.send_message(
                    chat_id=self.admin,
                    text="❌ Buyurtmalarni olish muvaffaqiyatsiz!: {}".format(response.text)
                )
                return None

            orders = result["result"].get("order", [])
            if not orders:
                break

            all_orders.extend(orders)
            page += 1

        self.orders = all_orders
        return None

    async def get_3_months_purchases(self, client_id: str):
        all_products = []
        for order in self.orders:
            if client_id == order['client']['CS_id']:
                products = order.get("orderProducts", [])
                for product in products:
                    prod_info = product.get("product", {})
                    product_data = {
                        "CS_id": prod_info.get('CS_id'),
                        "name": prod_info.get('name'),
                        "price": product.get('price'),
                        "quantity": product.get('quantity'),
                        "summa": product.get("summa")
                    }
                    all_products.append(product_data)

        return all_products

    async def embedding_function(self):
        if os.path.exists(self.persistent_directory):
            shutil.rmtree(self.persistent_directory)

        await self.login()
        await self.get_items()

        docs = []
        for item in self.items:
            name = (item.get("name") or "").strip()
            cs_id = item.get("id")
            price = item.get("price")
            if not name or not cs_id:
                continue

            metadata = {
                "id": cs_id,
                "name": name,
                "price": price
            }

            doc = Document(page_content=name, metadata=metadata)
            docs.append(doc)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=self.persistent_directory
        )

    def search_query(self, query: str,
                     k: int = 5,
                     score_threshold: float = 0.3) -> List[Dict]:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        db = Chroma(persist_directory=self.persistent_directory,
                    embedding_function=embeddings)

        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": k, "score_threshold": score_threshold}
        )

        results = retriever.invoke(query)

        response = []
        for doc in results:
            metadata = doc.metadata
            response.append({
                "name": metadata.get("name", "NOMA'LUM"),
                "id": metadata.get("id", "NOMA'LUM"),
                "price": metadata.get("price", "NOMA'LUM"),
            })

        return response

    def embedding_search(self, item_name: str) -> str:
        item_name_cyr = self.transliterator.transliterate(item_name, from_="lat", to="cyr")
        results = self.search_query(item_name_cyr, k=5, score_threshold=0.5)

        context = ""
        for i, match in enumerate(results, 1):
            name = match.get("name", "NOMA‘LUM")
            cs_id = match.get("id", "NOMA‘LUM")
            price = match.get("price", "NOMA‘LUM")

            context += f"{i}) 📦 Nomi: {name}\n   🆔 ID: {cs_id}\n   💰 Narxi: {price} so‘m\n\n"

        return context.strip()

    async def get_advert(self):
        await self.login()
        model = ChatOpenAI(model="gpt-4.1-mini")
        await self.get_items()
        clients = await self.get_clients()
        await self.get_orders()
        sum = 0
        for client in clients:
            if sum > 1500:
                await self.bot.send_message(self.admin, "1500 dan oshib ketdi")
                return
            text = ""
            text_2 = f"Mijoz: {client.get('name')} (ID: {client.get('CS_id')} Phone number: {client.get('tel')})"
            text_3 = ""
            orders = await self.get_3_months_purchases(client_id=client['CS_id'])
            if not orders:
                continue
            sum += 1
            for order in orders:
                text += f"""
Name: {order['name']}
Quantity: {order['quantity']}"""
                results = self.search_query(order['name'])
                for item in results:
                    text_3 += f"""
Id: {item['id']}
Name: {item['name']}
Price: {item['price']}
"""
            if text != "":
                messages = [
                    SystemMessage(content="c"),
                    HumanMessage(content=f"""
Quyida foydalanuvchi so‘nggi 3 oyda xarid qilgan mahsulotlar ro‘yxati va barcha mavjud mahsulotlar ro‘yxati berilgan. Xarid tendensiyalarini hisobga olgan holda, foydalanuvchi keyingi xaridlarda ehtimoliy sotib olishi mumkin bo‘lgan eng yuqori 10 ta mahsulotni aniqlang.

Faqat mahsulot ID’larini chiqarib bering — hech qanday matn, izoh yoki izohsiz. Faqat `id1 id2 id3 ...` ko‘rinishida bo‘lsin.

👤 Mijoz:
{text_2}

🛒 Foydalanuvchi xarid qilgan mahsulotlar:
{text}

📦 Embedding angling mahsulotlar(har bir mahsulot uchun threshold=0.3, k = 5):
{text_3}"""),
                ]
                result = model.invoke(messages)
                recommend_items = self.get_items_by_cs_id(result.content.strip().split())
                client_phone = self.normalize_phone(client.get("tel"))
                user_id = None
                for user in self.users:
                    user_phone = self.normalize_phone(user.get("phone_number"))
                    if client_phone and user_phone and client_phone == user_phone:
                        user_id = user.get("chat_id")
                        break

                for item in recommend_items:
                    name = item.get('name') or 'None'
                    price = item.get('price')
                    price_str = f"{price:,}" if isinstance(price, (int, float)) else 'None'

                    user_caption = f"""
🎯 <b>{name}</b>

💸 <b>Цена:</b> {price_str} so‘m

🛍 <i>Возможно, вам это как раз нужно!</i>
    """
                    if user_id:
                        try:
                            if item.get('imageUrl'):
                                await self.bot.send_photo(
                                    chat_id=user_id,
                                    photo=Config.URL[:28] + item['imageUrl'],
                                    caption=user_caption.strip(),
                                    parse_mode="HTML"
                                )
                            else:
                                await self.bot.send_message(
                                    chat_id=user_id,
                                    text=user_caption.strip(),
                                    parse_mode="HTML")
                        except:
                            pass
                user_info = f"""
👤 <b>Информация для клиентов</b>
🆔 ID: <code>{client.get('CS_id')}</code>
📛 Имя: <b>{client.get('name')}</b>
📞 Проволока: <code>{client.get('tel')}</code>
            """

                admin_items = ""
                for item in recommend_items:
                    admin_items += f"""
<a href="{Config.URL[:28]}{item['imageUrl']}">📦 <b>{item['name']}</b></a>
<pre>💰 Narxi: {item['price']:,} so‘m</pre>
    """

                admin_message = user_info + "\n" + "<b>🧠 Рекомендуемые продукты:</b>" + admin_items
                try:
                    await self.bot.send_message(
                        chat_id=admin_chat_id,
                        text=admin_message.strip(),
                        parse_mode="HTML"
                    )
                except:
                    pass
