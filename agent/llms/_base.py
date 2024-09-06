from abc import ABC

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


class _BaseLLM(ABC):
    """
    Base class for Large Language Models.
    """
    def __init__(
            self,
            name: str,
            llm: BaseChatModel,
            prompt: str,
            output_parser: BaseOutputParser = StrOutputParser(),
        ) -> None:
        self.name = name
        self.prompt = PromptTemplate.from_template(prompt)
        self.chain = self.prompt | llm | output_parser

    def invoke(self, state: dict):
        return self.chain.invoke(state)
