from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import FunctionMessage

from agent.database import Retriever, ModelType
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs import State


class SimilarQuestionsNode(_BaseNode):
    """
    RAG Node to pull relevant information based on user input.
    """
    DATABASE_COLLECTION_NAME = "original_data_collection"

    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM = None,
            prompt: str = None,
            output_parser: BaseOutputParser = None,
            show_logs: bool = False,
            retriever: Retriever = None,
        ) -> None:
        self.name = name
        self.description = description
        self.show_logs = show_logs
        self.retriever = Retriever(ModelType.RUBERT_TINY_2) if not retriever else retriever

    def invoke(self, state: State):
        history = state.history
        summary = self.get_summary(history)
        retrieved_info = self.retriever.search(
            query=summary,
            collection_name=SimilarQuestionsNode.DATABASE_COLLECTION_NAME,
            topk=1,
            score_threshold=0.75
        )

        if self.show_logs:
            print(self.name)
            print(f"Retrieved data: {retrieved_info}")
            print("---------------")

        history.append(FunctionMessage(name="SimilarQuestionsNode", content=retrieved_info))

        return {"history": history, "catalog_name": state.catalog_name}
