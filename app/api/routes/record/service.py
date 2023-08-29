from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import select, desc


from database.models.record import Record
from api.decorators.async_transaction import async_transaction

@async_transaction
async def db_create_new_record(session: AsyncSession, record:BaseModel):
    new_record = Record(text=record.text)
    session.add(new_record)
    await session.flush()
    record_data = {
        "id": str(new_record.id),
        "text": new_record.text
    }
    return record_data

@async_transaction
async def db_get_records(session: AsyncSession):
    query = select(Record)
    result = await session.execute(query)
    records = result.scalars().all()
    print(records)
    records_data = []
    for record in records:
        records_data_dict = {"id": str(record.id), "text": record.text}
        records_data.append(records_data_dict)
    return records_data

@async_transaction
async def db_get_single_record(session: AsyncSession, uuid: str):
    query = select(Record).where(Record.id == uuid)
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        record_data_dict = {"id": str(record.id), "text": record.text}
        return record_data_dict
    else:
        return None
    
@async_transaction
async def db_get_few_records(session: AsyncSession, count: int):
    query = select(Record).limit(count)
    result = await session.execute(query)
    records = result.scalars().all()
    records_data = []
    for record in records:
        records_data_dict = {"id": str(record.id), "text": record.text}
        records_data.append(records_data_dict)
    return records_data

@async_transaction
async def db_get_offset_records(session: AsyncSession, offset: int, count: int):
    query = select(Record).offset(offset).limit(count)
    result = await session.execute(query)
    records = result.scalars().all()
    records_data = []
    for record in records:
        records_data_dict = {"id": str(record.id), "text": record.text}
        records_data.append(records_data_dict)
    return records_data

@async_transaction
async def db_get_records_by_date(session: AsyncSession):
    query = select(Record).order_by(desc(Record.created_at))
    result = await session.execute(query)
    records = result.scalars().all()
    records_data = []
    for record in records:
        records_data_dict = {"id": str(record.id), "text": record.text}
        records_data.append(records_data_dict)
    return records_data

@async_transaction
async def db_update_record(session: AsyncSession, uuid: str, text: str):
    query = select(Record).where(Record.id == uuid)
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        record.text = text
        session.commit()
        record_data = {
            "id": str(record.id),
            "text": record.text
        }
        return record_data
    else:
        return None
@async_transaction
async def db_delete_record(session: AsyncSession, uuid: str):
    query = select(Record).where(Record.id == uuid)
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        await session.delete(record)
        await session.commit()
        return {"message": "record deleted", "id": str(record.id)}
    else:
        return {"message": "record not found", "id": str(record.id)}