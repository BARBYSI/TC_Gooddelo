

async def add_record(session, text):
    async with session.post("http://api:8080/record/new", json={"text": text}):
        pass

