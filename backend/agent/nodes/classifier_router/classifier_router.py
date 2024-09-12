from typing import Dict, Literal
from langchain_core.messages import AIMessage

from agent.nodes._base import _BaseRouter
from agent.graphs.state import State


class ClassifierRouter(_BaseRouter):
    """
    Router Node to retranslate classifier node output to RAG or OPERATOR nodes.
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
        catalog_name = state.catalog_name

        if self.show_logs:
            print(self.name)
            print(f"Catalog name: {catalog_name}")
            print("----------------")

        if catalog_name:
            if catalog_name == "оператор":
                return "оператор"
            elif catalog_name not in (
                "здоровье",
                "финансы",
                "аккаунт",
                "работа",
                "оператор",
                "документы",
            ):
                return "no_info"
            else:
                return "rag"
        else:
            return "end"
