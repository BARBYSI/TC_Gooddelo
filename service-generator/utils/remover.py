from api_requests.get_record import get_records
from api_requests.delete_record import delete_record
from utils.logging import logger
import asyncio

async def remover(session):
    counter = 0
    while True:
        records = await get_records(session, 10)

        for record in records:
            await delete_record(session, record['id'])
            counter += 1
        logger.info(f'Я УДАЛИЛ ВОТ СТОКА ЗАПИСЕЙ КАРОЧ: {counter}')
        await asyncio.sleep(10)

