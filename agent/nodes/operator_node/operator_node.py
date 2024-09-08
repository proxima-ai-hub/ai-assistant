from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import AIMessage

from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs import State


class OperatorNode(_BaseNode):
    """
    Operator Node to redirect user requirements to human.
    """

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

    def invoke(self, state: State):
        if self.show_logs:
            print(self.name)
            print("----------------")

        state.history.append(AIMessage(name="OperatorNode", content="Перевожу на оператора..."))

        return {"history": state.history, "catalog_name": state.catalog_name}
