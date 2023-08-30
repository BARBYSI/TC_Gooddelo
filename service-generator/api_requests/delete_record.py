
async def delete_record(session, uuid):
    async with session.delete(f'http://api:8080/record/delete/{uuid}'):
        pass