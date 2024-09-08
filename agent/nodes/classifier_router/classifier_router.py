from typing import Dict, Literal
from langchain_core.messages import FunctionMessage

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
        classifier_output = state.history[-1]

        if not isinstance(classifier_output, FunctionMessage):
            raise TypeError("Classifier Router accepts only ClassifierNode output")

        if self.show_logs:
            print(self.name)
            print(f"Classifier output: {classifier_output.content}")
            print(f"Model answer: {self.mapping[classifier_output.content]}")
            print("----------------")

        if classifier_output.content != "operator":
            return "rag"
        else:
            return "operator"
