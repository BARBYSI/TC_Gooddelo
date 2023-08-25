from fastapi import status, HTTPException

def check_empty_value(value):
    if isinstance(value, str) and value.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Value can't be empty",)
    return value