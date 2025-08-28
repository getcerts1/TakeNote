from pydantic import BaseModel, field_validator
from typing import Literal, Optional


class NoteModel(BaseModel):
    note_name: str
    note_value: str
    expiration: Optional[Literal[300, 600, 1200, 1800, 3600, 5200, 10400, 21600]] = 300


class SignIn(BaseModel):
    username: str
    password: str

    @field_validator('password')
    def length_check(cls, value):
        if len(value) < 8:
            raise ValueError("Password length too short")
        return value
