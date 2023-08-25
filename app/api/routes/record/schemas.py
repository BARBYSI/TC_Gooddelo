from pydantic import BaseModel, Field, validator

from api.validator.schema_validators import check_empty_value


class RecordSchema(BaseModel):
    id: str = Field(example="0d04e47f-6176-4f0e-8d15-a68d1a45d24a")
    text: str = Field(example="cool text")
    
    _empty_values = validator('id', 'text', allow_reuse=True)(check_empty_value)

class RecordOverrideSchema(BaseModel):
    text: str = Field(example="cool text")


    
