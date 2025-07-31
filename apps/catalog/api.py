import requests

from bot.dispatcher import Config


class APIClient:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.login_data = {
            "method": "login",
            "auth": {
                "login": Config.LOGIN,
                "password": Config.PASSWORD
            }
        }
        self.url = Config.URL

    def login(self):
        res = requests.get(self.url, json=self.login_data).json()
        if res.get("status"):
            self.token = res["result"]["token"]
            self.user_id = res["result"]["userId"]

    def get_categories(self):
        self.login()
        data = {
            "method": "getProductCategory",
            "auth": {"userId": self.user_id, "token": self.token}
        }
        res = requests.get(self.url, json=data).json()
        result = []
        for category in res['result']['productCategory']:
            if category['active'] == "Y":
                result.append(category)
        return result

    def get_prices(self):
        response = requests.get(
            self.url,
            json={
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
        )
        result = response.json()
        if result['status'] is True:
            lst = result['result']
            prices = {price['product']["CS_id"]: price["price"] for price in lst}
            return prices
        return []

    def get_products(self, category_id, limit=1000):
        self.login()
        items = []
        for i in range(4):
            data = {
                "method": "getProduct",
                "auth": {"userId": self.user_id, "token": self.token},
                "params": {"page": i + 1, "limit": limit}
            }
            res = requests.get(self.url, json=data).json()
            items.append(res['result']['product'])
        item_list = []
        prices = self.get_prices()
        for i in items:
            for item in i:
                if item['category']['CS_id'] != category_id or item['active'] != "Y":
                    continue
                cs_id = item.get("CS_id")
                name = item.get("name", "").strip()
                imageUrl = item.get("imageUrl", "")
                price = prices.get(cs_id, 0)

                if not cs_id or not name:
                    continue
                item_list.append({
                    "id": cs_id,
                    "name": name,
                    "price": price,
                    "imageUrl": imageUrl,
                })
        return item_list

    def get_product(self, item_id, limit=1000):
        self.login()
        items = []
        for i in range(4):
            data = {
                "method": "getProduct",
                "auth": {"userId": self.user_id, "token": self.token},
                "params": {"page": i + 1, "limit": limit}
            }
            res = requests.get(self.url, json=data).json()
            items.append(res['result']['product'])
        item_list = []
        prices = self.get_prices()
        for i in items:
            for item in i:
                if item['CS_id'] != item_id or item['active'] != "Y":
                    continue
                cs_id = item.get("CS_id")
                name = item.get("name", "").strip()
                imageUrl = item.get("imageUrl", "")
                price = prices.get(cs_id, 0)

                if not cs_id or not name:
                    continue
                item_list.append({
                    "id": cs_id,
                    "name": name,
                    "price": price,
                    "imageUrl": imageUrl,
                })
        return item_list
