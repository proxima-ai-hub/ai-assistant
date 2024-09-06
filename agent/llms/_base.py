from abc import ABC

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate


class _BaseLLM(ABC):
    """
    Base class for Large Language Models.
    """
    def __init__(self, name: str, llm: BaseChatModel) -> None:
        self.name = name
        self._llm = llm

    @property
    def llm(self):
        return self._llm

    def invoke(
            self,
            state: dict,
            prompt: str = "",
            output_parser: BaseOutputParser = StrOutputParser()
        ):
        chain = PromptTemplate.from_template(prompt) | self.llm | output_parser
        return chain.invoke(state)
