from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from sqlalchemy.ext.asyncio import AsyncSession

from .service import *
from database.connection import get_session
from .schemas import *
from database.models.record import Record

router = APIRouter(
    tags=['record'],
    prefix='/record'
)

@router.post(path='/new', status_code=status.HTTP_201_CREATED)
async def create_record(record: RecordSchema, session: AsyncSession = Depends(get_session)):
    record_data = await db_create_new_record(session, record)
    await FastAPICache.clear()
    return JSONResponse(content={"message": "record created", "id": record_data["id"], "text": record_data["text"]})

@router.get(path='/all', response_model=list[RecordSchema], status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_all_records(session: AsyncSession = Depends(get_session)):
    records_data = await db_get_records(session)
    return JSONResponse(content=records_data, status_code=status.HTTP_200_OK)

@router.get(path='/{uuid}', response_model=RecordSchema, status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_record(uuid: str, session: AsyncSession = Depends(get_session)):
    record_data = await db_get_single_record(session, uuid)
    if record_data != None:
        return JSONResponse(content=record_data)
    else:
        return JSONResponse(content="record not found", status_code=status.HTTP_404_NOT_FOUND)

@router.get(path='/few/{count}', response_model=RecordSchema, status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_records(count: str, session: AsyncSession = Depends(get_session)):
    records_data = await db_get_few_records(session, count)
    print(records_data)
    return JSONResponse(content=records_data)

@router.get(path='/{offset}/{count}', response_model=RecordSchema, status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_records(offset: int, count: int, session: AsyncSession = Depends(get_session)):
    records_data = await db_get_offset_records(session, offset, count)
    return JSONResponse(content=records_data)

@router.get(path='/sorted/by_creation_date/all', response_model=RecordSchema, status_code=status.HTTP_200_OK)
@cache(expire=600, coder=JsonCoder)
async def get_records_by_date(session: AsyncSession = Depends(get_session)):
    records_data = await db_get_records_by_date(session)
    return JSONResponse(content=records_data)

@router.put(path='/update/{uuid}', status_code=status.HTTP_200_OK)
async def update_record(uuid: str, new_record: RecordOverrideSchema, session: AsyncSession = Depends(get_session)):
    record_data = await db_update_record(session, uuid, new_record.text)
    FastAPICache.clear()
    if record_data != None:
        return JSONResponse(content={"message": "record updated", "id": record_data['id'], "text": record_data['text']})
    else:
        return JSONResponse(content="record not found", status_code=status.HTTP_404_NOT_FOUND)
    
@router.delete(path='/delete/{uuid}', status_code=status.HTTP_200_OK)
async def delete_record(uuid: str, session: AsyncSession = Depends(get_session)):
    result = await db_delete_record(session, uuid)
    FastAPICache.clear()

    return JSONResponse(content=result)

#добавить удаление/обновление кеша