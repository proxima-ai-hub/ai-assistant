from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class RequsetHistory(BaseModel):
    history: List[Message]