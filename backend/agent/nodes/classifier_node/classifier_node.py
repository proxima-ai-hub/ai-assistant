from typing import List

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import AIMessage, BaseMessage

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

    def get_similar_questions(self, history: List[BaseMessage]):
        questions = history[-1].content
        result = [f"{data['payload']['question']} - {data['payload']['catalog']}"
                  for data in questions]
        return "\n".join(result)

    def invoke(self, state: State):
        history = state.history
        similar_questions = self.get_similar_questions(history)
        summary = self.get_summary(history)

        answer = self.chain.invoke({"summary": summary, "similar_questions": similar_questions})

        if self.show_logs:
            print(self.name)
            print(f"User query: {summary}")
            print(f"Similar questions: {similar_questions}")
            print(f"Model answer: {answer}")
            print("----------------")

        catalog_name = answer

        return {"history": history, "catalog_name": catalog_name}
