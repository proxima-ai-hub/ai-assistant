from abc import ABC
from typing import Dict

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.prompts import PromptTemplate

from agent.llms._base import _BaseLLM


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
