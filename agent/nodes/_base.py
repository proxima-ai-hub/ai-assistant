from typing import Dict, List
from abc import ABC

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import FunctionMessage, BaseMessage
from langchain_core.prompts import PromptTemplate

from agent.llms._base import _BaseLLM
from agent.graphs.state import State


class _BaseNode(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM,
            prompt: str = "",
            output_parser: BaseOutputParser = StrOutputParser(),
        ) -> None:
        self.name = name
        self.description = description
        self.chain = PromptTemplate.from_template(prompt) | llm.llm | output_parser

    def get_summary(self, history: List[BaseMessage]):
        for replic in history[::-1]:
            if isinstance(replic, FunctionMessage) and replic.name == "SummarizationNode":
                return replic.content
        raise Exception("Not found summary")


class _BaseRouter(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            mapping: Dict,
        ) -> None:
        self.name = name
        self.description = description
        self._mapping = mapping

    @property
    def mapping(self):
        return self._mapping

    def invoke(self, state: State):
        pass
