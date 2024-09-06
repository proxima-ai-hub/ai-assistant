from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser

from ._base import _BaseLLM


class LlamaLLM(_BaseLLM):
    def __init__(
            self,
            name: str,
            ollama_model_name: str,
            prompt: str,
            output_parser: BaseOutputParser = StrOutputParser()
        ) -> None:
        llm = OllamaLLM(model=ollama_model_name)
        super().__init__(name, llm, prompt, output_parser)
