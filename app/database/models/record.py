from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import DateTime
from database.connection import Base
from uuid import uuid4 as uuid
from datetime import datetime

class Record(Base):
    __tablename__ = 'records'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid)
    text= Column(String, default='')
    created_at = Column(DateTime, default=datetime.now())
