from typing import List

from pydantic import BaseModel


class Messages(BaseModel):
    role: str = "user"
    content: str


class Request(BaseModel):
    history: List[Messages]


class Message(BaseModel):
    text: str