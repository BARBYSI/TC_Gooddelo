from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession

def async_transaction(func):
    @wraps(func)
    async def wrapper(db_session, *args, **kwargs):
        async with db_session as session:
            try: 
                return await func(session, *args, **kwargs)
            except Exception as e:
                raise e
            finally: 
                await db_session.commit()
                await db_session.close()
    return wrapper