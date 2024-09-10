from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import AIMessage

from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs import State


class NoInfoNode(_BaseNode):
    """
    NoInfoNode if there is no information.
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
        history = state.history

        if self.show_logs:
            print(self.name)
            print("Not Found information")
            print("----------------")

        history.append(AIMessage(
            name="NoInfoNode",
            content="Извините, у меня нет информации по Вашему запросу. Пожалуйста, переформулируйте вопрос или попросите перевести Вас на оператора."
        ))

        return {"history": history, "catalog_name": state.catalog_name}
