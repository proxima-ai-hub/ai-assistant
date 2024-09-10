from typing import Dict, Literal
from langchain_core.messages import FunctionMessage

from agent.nodes._base import _BaseRouter
from agent.graphs.state import State


class RAGRouter(_BaseRouter):
    """
    RAG router to retranslate rag node output.
    """
    def __init__(
            self,
            name: str,
            description: str,
            mapping: Dict,
            show_logs: bool = False
        ):
        super().__init__(name, description, mapping)
        self.show_logs = show_logs

    def invoke(self, state: State) -> Literal["rag", "operator"]:
        last = state.history[-1]
        assert isinstance(last, FunctionMessage) and last.name == "RAGNode"

        if not last.content or len(last.content) < 1:
            return "no_info"
        else:
            return "answer"
