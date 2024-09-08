from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import FunctionMessage

from .prompt import CLASSIFIER_NODE_PROMPT
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State


class ClassifierNode(_BaseNode):
    """
    Classifier Node to classify input query (user input) in categories.
    """
    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM,
            prompt: str = CLASSIFIER_NODE_PROMPT,
            output_parser: BaseOutputParser = StrOutputParser(),
            show_logs: bool = False
        ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs

    def _history_to_str(self, history: list) -> str:
        roles = ["assistant", "user"]
        result = [f"{roles[ind % 2]}: {message.content}"
                  for ind, message in enumerate(history)]
        return "\n".join(result)

    def invoke(self, state: State):
        history = state.history
        answer = self.chain.invoke({"history": self._history_to_str(history)})

        if self.show_logs:
            print(self.name)
            print(f"User query: {history[-1]}")
            print(f"Model answer: {answer}")
            print("----------------")

        history.append(FunctionMessage(name="ClassifierNode", content=answer))
        return {"history": history}
