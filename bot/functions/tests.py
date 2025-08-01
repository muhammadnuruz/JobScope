from bot.functions.get_advert_function import AIProductManager
from dotenv import load_dotenv

load_dotenv()

import asyncio


async def main():
    manager = AIProductManager()
    await manager.login()
    items = await manager.get_items()
    for item in items:
        print(item['packQuantity'])


if __name__ == "__main__":
    asyncio.run(main())
