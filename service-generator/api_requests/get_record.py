

async def get_records(session, count):
    async with session.get(f'http://api:8080/record/few/{count}') as response:
        return await response.json()