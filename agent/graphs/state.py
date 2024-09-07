from langchain_core.pydantic_v1 import BaseModel
from typing import Annotated, List
import operator

from langchain_core.messages import BaseMessage


class State(BaseModel):
    history: List[BaseMessage]
