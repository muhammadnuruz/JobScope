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
        self.login()

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

    def get_products(self, category_id, page=1, limit=1000):
        data = {
            "method": "getProduct",
            "auth": {"userId": self.user_id, "token": self.token},
            "params": {"page": page, "limit": limit}
        }
        res = requests.get(self.url, json=data).json()
        item_list = []
        prices = self.get_prices()
        for item in res['result']['product']:
            if item['category']['CS_id'] != category_id:
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
