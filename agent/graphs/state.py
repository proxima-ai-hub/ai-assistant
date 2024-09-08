from langchain_core.pydantic_v1 import BaseModel
from typing import Annotated, List
import operator

from langchain_core.messages import BaseMessage


class State(BaseModel):
    catalog_name: str = None
    history: List[BaseMessage]
