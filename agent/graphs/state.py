from typing import List

from langchain_core.pydantic_v1 import BaseModel
from langchain_core.messages import BaseMessage


class State(BaseModel):
    catalog_name: str = None
    hallucination: List[float] = []
    history: List[BaseMessage]
