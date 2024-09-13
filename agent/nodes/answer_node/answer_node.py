from typing import List

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain.evaluation import load_evaluator, EvaluatorType
from langchain_core.messages import BaseMessage, AIMessage
import pandas as pd

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
            show_logs: bool = False,
            save_online_metric: bool = False,
        ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs
        self.save_online_metric = save_online_metric
        if self.save_online_metric:
            self.evaluator = load_evaluator("labeled_score_string", llm=llm.llm, normalize_by=10)

    def get_data(self, history: List[BaseMessage]):
        rag_answer = history[-1].content
        result = {x['payload']['question']: x['payload']['content']
                  for x in rag_answer}
        # result = {"question": [x['payload']['question'] for x in rag_answer],
        #           "correct_answer": [x['payload']['content'] for x in rag_answer]}
        # result = pd.DataFrame(result).to_markdown()

        # result = [f"{x['payload']['question']} - {x['payload']['content']}"
        #           for x in rag_answer]
        # return "\n".join(result)
        return result

    def invoke(self, state: State):
        history = state.history
        summary = self.get_summary(history)
        data = self.get_data(history)

        answer = self.chain.invoke({"summary": summary, "data": data})

        if self.save_online_metric:
            score = self.evaluator.evaluate_strings(
                prediction=answer,
                reference=data[next(iter(data))],
                input=summary,
            )["score"]
            state.hallucination.append(score)

        if self.show_logs:
            print(self.name)
            print(f"User query: {summary}")
            print(f"Model answer: {answer}")
            print("----------------")

        history.append(AIMessage(name="HealthNode", content=answer))

        return {"history": history, "catalog_name": state.catalog_name, "hallucination": state.hallucination}
