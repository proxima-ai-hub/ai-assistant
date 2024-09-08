from typing import List

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import BaseMessage, AIMessage

from .prompt import ANSWER_NODE_PROMPT
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State


class AnswerNode(_BaseNode):
    """
    Answer Node to generate answer based on data catalog.
    """
    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM,
            prompt: str = ANSWER_NODE_PROMPT,
            output_parser: BaseOutputParser = StrOutputParser(),
            show_logs: bool = False
        ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs

    def get_data(self, history: List[BaseMessage]):
        rag_answer = history[-1].content
        result = {x['payload']['question']: x['payload']['content']
                  for x in rag_answer}
        # result = [f"{x['payload']['question']} - {x['payload']['content']}"
        #           for x in rag_answer]
        # return "\n".join(result)
        return result

    def invoke(self, state: State):
        history = state.history
        summary = self.get_summary(history)
        data = self.get_data(history)

        answer = self.chain.invoke({"summary": summary, "data": data})

        if self.show_logs:
            print(self.name)
            print(f"User query: {summary}")
            print(f"Model answer: {answer}")
            print("----------------")

        history.append(AIMessage(name="HealthNode", content=answer))

        return {"history": history, "catalog_name": state.catalog_name}
