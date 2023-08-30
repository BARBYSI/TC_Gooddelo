from api_requests.add_record import add_record
from utils.string_generator import generate_random_string
from utils.logging import logger
import asyncio
import time
import random

async def records_generator(session):
    while True:
        records_amount = random.randint(10,100)
        for _ in range(records_amount):
            await add_record(session, generate_random_string(16))
        logger.info(f'Я ЩА СДЕЛАЛ СТОЛЬКО ЗАПИСЕЙ КАРОЧ: {records_amount}')
        await asyncio.sleep(30)


