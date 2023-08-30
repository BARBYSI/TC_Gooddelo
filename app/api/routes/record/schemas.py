from pydantic import BaseModel, Field, validator

from api.validator.schema_validators import check_empty_value


class RecordSchema(BaseModel):
    text: str = Field(example="cool text")
    
    _empty_values = validator('text', allow_reuse=True)(check_empty_value)

class RecordOverrideSchema(BaseModel):
    text: str = Field(example="cool text")


    
