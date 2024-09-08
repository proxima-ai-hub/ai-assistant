from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import FunctionMessage

from agent.database import Retriever, ModelType
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM


class RAGNode(_BaseNode):
    """
    RAG Node to pull relevant information based on user input.
    """
    DATABASE_COLLECTION_NAME = "original_data_collection"
    CATALOG_NAME_TO_CATALOG = {
        "health": "здоровье",
        "account": "аккаунт",
        "finance": "финансы",
        "career": "работа",
        "documents": "документы",
    }

    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM = None,
            prompt: str = None,
            output_parser: BaseOutputParser = None,
            show_logs: bool = False,
        ) -> None:
        self.name = name
        self.description = description
        self.show_logs = show_logs
        self.retriever = Retriever(ModelType.RUBERT_TINY_2)

    def invoke(self, state):
        history = state.history
        catalog_name = history[-1].content
        retrieved_info = self.retriever.search(
            query=history[1].content,
            collection_name=RAGNode.DATABASE_COLLECTION_NAME,
            filter_options={"catalog": RAGNode.CATALOG_NAME_TO_CATALOG[catalog_name]}
        )

        if self.show_logs:
            print(self.name)
            print(f"Going to catalog: {catalog_name}")
            print(f"Retrieved data: {retrieved_info}")

        history.append(FunctionMessage(name="RAGNode", content=retrieved_info))

        return {"history": history}
