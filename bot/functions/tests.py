from bot.functions.get_advert_function import AIProductManager
from dotenv import load_dotenv

load_dotenv()

import asyncio


async def main():
    manager = AIProductManager()
    await manager.login()
    clients = await manager.get_clients()
    print(len(clients))

if __name__ == "__main__":
    asyncio.run(main())
