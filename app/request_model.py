from pydantic import BaseModel
from typing import Literal, Optional


class NoteModel(BaseModel):
    note_name: str
    note_value: str
    expiration: Optional[Literal[5, 10, 20, 30, 60, 120, 240, 360]] = 5