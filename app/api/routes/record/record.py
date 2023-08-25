from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse

from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from database.connection import get_session
from .schemas import *
from .model import Record

router = APIRouter(
    tags=['record'],
    prefix='/record'
)

@cache()
async def get_cache():
    return 1

@router.post(path='/new', status_code=status.HTTP_201_CREATED)
async def create_record(record: RecordSchema, session: AsyncSession = Depends(get_session)):
    new_record = Record(text=record.text)
    session.add(new_record)
    await session.flush()
    return JSONResponse(content={"message": "record created", "id": str(new_record.id)})

@router.get(path='/all', response_model=list[RecordSchema], status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_all_records(session: AsyncSession = Depends(get_session)):
    query = select(Record)
    result = await session.execute(query)
    records = result.scalars().all()
    records_data = []
    for record in records:
        records_data_dict = {"id": str(record.id), "text": record.text}
        records_data.append(records_data_dict)
    return JSONResponse(content=records_data, status_code=status.HTTP_200_OK)

@router.get(path='/{uuid}', response_model=RecordSchema, status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_record(uuid: str, session: AsyncSession = Depends(get_session)):
    query = select(Record).where(Record.id == uuid)
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        record_data_dict = {"id": str(record.id), "text": record.text}
        return JSONResponse(content=record_data_dict)
    else:
        return JSONResponse(content="record not found", status_code=status.HTTP_404_NOT_FOUND)
    
@router.get(path='/few/{count}', response_model=RecordSchema, status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_few_records(count: str, session: AsyncSession = Depends(get_session)):
    query = select(Record).limit(count)
    result = await session.execute(query)
    records = result.scalars().all()
    records_data = []
    for record in records:
        records_data_dict = {"id": str(record.id), "text": record.text}
        records_data.append(records_data_dict)
    return JSONResponse(content=records_data)

@router.get(path='/{offset}/{count}', response_model=RecordSchema, status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_offset_records(offset: int, count: int, session: AsyncSession = Depends(get_session)):
    query = select(Record).offset(offset).limit(count)
    result = await session.execute(query)
    records = result.scalars().all()
    records_data = []
    for record in records:
        records_data_dict = {"id": str(record.id), "text": record.text}
        records_data.append(records_data_dict)
    return JSONResponse(content=records_data)

@router.get(path='/sorted/by_creation_date/all', response_model=RecordSchema, status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_records_by_date(session: AsyncSession = Depends(get_session)):
    query = select(Record).order_by(desc(Record.created_at))
    result = await session.execute(query)
    records = result.scalars().all()
    records_data = []
    for record in records:
        records_data_dict = {"id": str(record.id), "text": record.text}
        records_data.append(records_data_dict)
    return JSONResponse(content=records_data)

@router.put(path='/update/{uuid}', status_code=status.HTTP_200_OK)
async def update_record(uuid: str, new_record: RecordOverrideSchema, session: AsyncSession = Depends(get_session)):
    query = select(Record).where(Record.id == uuid)
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        record.text = new_record.text
        session.commit()
        return JSONResponse(content={"message": "record updated", "id": str(record.id), "text": record.text})
    else:
        return JSONResponse(content="record not found", status_code=status.HTTP_404_NOT_FOUND)
    
@router.delete(path='/delete/{uuid}', status_code=status.HTTP_200_OK)
async def delete_record(uuid: str, session: AsyncSession = Depends(get_session)):
    query = select(Record).where(Record.id == uuid)
    result = await session.execute(query)
    record = result.scalars().first()
    if record:
        await session.delete(record)
        await session.commit()
        return JSONResponse(content={"message": "record deleted", "id": str(record.id)})
    else:
        return JSONResponse(content="record not found", status_code=status.HTTP_404_NOT_FOUND)


#добавить удаление/обновление кеша