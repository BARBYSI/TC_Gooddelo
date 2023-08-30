from utils.records_generator import records_generator
from utils.remover import remover
import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        print("start!")
        task1 = asyncio.create_task(records_generator(session))
        task2 = asyncio.create_task(remover(session))
        await asyncio.gather(task1, task2)


if __name__ == "__main__":
    asyncio.run(main())
