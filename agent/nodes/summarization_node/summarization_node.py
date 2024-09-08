import json

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import HumanMessage, AIMessage, FunctionMessage

from .prompt import SUMMARIZATION_NODE_PROMPT
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State


class SummarizationNode(_BaseNode):
    """
    Summarization Node to summarize user requirements.
    """
    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM,
            prompt: str = SUMMARIZATION_NODE_PROMPT,
            output_parser: BaseOutputParser = StrOutputParser(),
            show_logs: bool = False
        ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs

    def _history_to_str(self, history: list) -> str:
        roles = ["assistant", "user"]
        result = [f"{roles[ind % 2]}: {message.content}"
                  for ind, message in enumerate(history)
                  if isinstance(message, (HumanMessage, AIMessage))]
        return "\n".join(result)

    def invoke(self, state: State):
        history = state.history
        answer = self.chain.invoke({"history": self._history_to_str(history)})

        if self.show_logs:
            print(self.name)
            print(f"User query: {history[-1]}")
            print(f"Model answer: {answer}")
            print("----------------")

        history.append(FunctionMessage(name="SummarizationNode", content=answer))

        return {"history": history, "catalog_name": state.catalog_name}
