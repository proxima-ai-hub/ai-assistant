from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import FunctionMessage

from agent.database import Retriever, ModelType
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs import State


class RetrieverNode(_BaseNode):
    """
    Retriever Node to pull relevant information based on user input.
    """
    DATABASE_COLLECTION_NAME = "original_data_deepvk_collection"

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
        catalog_name = state.catalog_name
        retrieved_info = self.retriever.search(
            query=self.get_summary(history),
            collection_name=RetrieverNode.DATABASE_COLLECTION_NAME,
            filter_options={"catalog": catalog_name},
            topk=5,
            score_threshold=0.5
        )

        if self.show_logs:
            print(self.name)
            print(f"Summary: {self.get_summary(history)}")
            print(f"Going to catalog: {catalog_name}")
            print(f"Retrieved data: {retrieved_info}")
            print("----------------")

        history.append(FunctionMessage(name="RetrieverNode", content=retrieved_info))

        return {"history": history, "catalog_name": catalog_name}
