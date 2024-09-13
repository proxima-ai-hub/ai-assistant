from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph

from agent.nodes import (
    SimilarQuestionsNode,
    ClassifierRouter,
    RetrieverRouter,
    ParaphraseNode,
    ClassifierNode,
    RetrieverNode,
    OperatorNode,
    AnswerNode,
    NoInfoNode,
)
from agent.database import Retriever, ModelType
from agent.llms import LlamaLLM
from agent.graphs import State


class ConsultantGraph:
    def __init__(self, show_logs: bool = False, save_online_metric: bool = False) -> None:
        self.llm = LlamaLLM("llama_3.1 from ollama", "temp0:latest")
        self.show_logs = show_logs
        self.save_online_metric = save_online_metric

        self.graph = self._build_graph()
        self.history = [AIMessage(content="Привет, я бот-консультант, чем могу помочь?")]
        self.catalog_name = None
        self.hallucination = []
    
    def _build_graph(self):
        graph = StateGraph(State)
        retriever = Retriever(ModelType.DEEPVK_USER)
        
        # Initialize nodes
        paraphrase_node = ParaphraseNode(
            name="ParaphraseNode",
            description=ParaphraseNode.__doc__,
            llm=self.llm,
            show_logs=self.show_logs
        )
        similar_questions_node = SimilarQuestionsNode(
            name="SimilarQuestionsNode",
            description=SimilarQuestionsNode.__doc__,
            retriever=retriever,
            show_logs=self.show_logs,
        )
        classifier_node = ClassifierNode(
            name="Classifier Node",
            description=ClassifierNode.__doc__,
            llm=self.llm,
            show_logs=self.show_logs
        )
        classifier_router = ClassifierRouter(
            name="Classifier Router",
            description=ClassifierRouter.__doc__,
            mapping={
                "retriever": "retriever",
                "operator": "operator",
                "no_info": "no_info",
                "end": END,
            },
            show_logs=self.show_logs
        )
        retriever_node = RetrieverNode(
            name="RetrieverNode",
            description=RetrieverNode.__doc__,
            retriever=retriever,
            show_logs=self.show_logs,
        )
        answer_node = AnswerNode(
            name="AnswerNode",
            description=AnswerNode.__doc__,
            llm=self.llm,
            show_logs=self.show_logs,
            save_online_metric = self.save_online_metric
        )
        operator_node = OperatorNode(
            name="OperatorNode",
            description=OperatorNode.__doc__,
            show_logs=self.show_logs,
        )
        no_info_node = NoInfoNode(
            name="NoInfoNode",
            description=NoInfoNode.__doc__,
        )
        retriever_router = RetrieverRouter(
            name="RetrieverRouter",
            description=RetrieverRouter.__doc__,
            mapping={
                "answer": "answer",
                "no_info": "no_info"
            },
            show_logs=self.show_logs
        )

        # Add nodes to graph
        graph.add_node("paraphrase", paraphrase_node.invoke)
        graph.add_node("classifier", classifier_node.invoke)
        graph.add_node("similar_questions", similar_questions_node.invoke)
        graph.add_node("retriever", retriever_node.invoke)
        graph.add_node("answer", answer_node.invoke)
        graph.add_node("operator", operator_node.invoke)
        graph.add_node("no_info", no_info_node.invoke)

        # Set up graph relations
        graph.add_edge(START, "paraphrase")
        graph.add_edge("paraphrase", "similar_questions")
        graph.add_edge("similar_questions", "classifier")
        graph.add_conditional_edges(
            "classifier",
            classifier_router.invoke,
            classifier_router.mapping,
        )
        graph.add_conditional_edges(
            "retriever",
            retriever_router.invoke,
            retriever_router.mapping,
        )
        graph.add_edge("answer", END)
        graph.add_edge("operator", END)
        graph.add_edge("no_info", END)

        return graph.compile()
    
    def clear_history(self):
        self.history = [self.history[0]]
        self.catalog_name = None

    def invoke(self, query: str):
        self.history.append(HumanMessage(content=query))
        answer = self.graph.invoke(
            {"history": self.history,
             "catalog_name": self.catalog_name,
             "hallucination": self.hallucination}
        )
        self.history = answer["history"]
        self.catalog_name = answer["catalog_name"]
        self.hallucination = answer["hallucination"]

        return answer["history"][-1]

    def _print_message(self) -> str:
        message = self.history[-1]
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        print(f"{role}: {message.content}")

    def chat(self):
        while True:
            self._print_message()
            query = input("user: ")
            if query == "q":
                break
            
            self.invoke(query)
            self._print_message()
            print("HISTORY OF MESSAGES")
            print(self.history)
            print("Scores")
            print(self.hallucination)
            self.clear_history()
            print()
            print()
