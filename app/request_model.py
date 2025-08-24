from pydantic import BaseModel
from typing import Literal, Optional


class NoteModel(BaseModel):
    note_name: str
    note_value: str
    expiration: Optional[Literal[300, 600, 1200, 1800, 3600, 5200, 10400, 21600]] = 300