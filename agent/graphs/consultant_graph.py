from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph

from agent.nodes import (
    ClassifierNode,
    ClassifierRouter,
    RAGNode,
    SummarizationNode,
    SimilarQuestionsNode,
    AnswerNode,
    OperatorNode,
    NoInfoNode,
    RAGRouter
)
from agent.database import Retriever, ModelType
from agent.llms import LlamaLLM
from agent.graphs import State


class ConsultantGraph:
    def __init__(self, show_logs: bool = False) -> None:
        self.llm = LlamaLLM("llama_3.1 from ollama", "temp0:latest")
        self.show_logs = show_logs

        self.graph = self._build_graph()
        self.history = [AIMessage(content="Привет, я бот-консультант, чем могу помочь?")]
        self.catalog_name = None
    
    def _build_graph(self):
        graph = StateGraph(State)
        retriever = Retriever(ModelType.DEEPVK_USER)
        
        # Initialize nodes
        summarization_node = SummarizationNode(
            name="Summarization Node",
            description=SummarizationNode.__doc__,
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
                "rag": "rag",
                "оператор": "operator",
                "no_info": "no_info",
                "end": END,
            },
            show_logs=self.show_logs
        )
        rag_node = RAGNode(
            name="RAGNode",
            description=RAGNode.__doc__,
            retriever=retriever,
            show_logs=self.show_logs,
        )
        answer_node = AnswerNode(
            name="AnswerNode",
            description=AnswerNode.__doc__,
            llm=self.llm,
            show_logs=self.show_logs
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
        rag_router = RAGRouter(
            name="RAGRouter",
            description=RAGRouter.__doc__,
            mapping={
                "answer": "answer",
                "no_info": "no_info"
            },
            show_logs=self.show_logs
        )

        # Add nodes to graph
        graph.add_node("summarization", summarization_node.invoke)
        graph.add_node("classifier", classifier_node.invoke)
        graph.add_node("similar_questions", similar_questions_node.invoke)
        graph.add_node("rag", rag_node.invoke)
        graph.add_node("answer", answer_node.invoke)
        graph.add_node("operator", operator_node.invoke)
        graph.add_node("no_info", no_info_node.invoke)

        # Set up graph relations
        graph.add_edge(START, "summarization")
        graph.add_edge("summarization", "similar_questions")
        graph.add_edge("similar_questions", "classifier")
        graph.add_conditional_edges(
            "classifier",
            classifier_router.invoke,
            classifier_router.mapping,
        )
        graph.add_conditional_edges(
            "rag",
            rag_router.invoke,
            rag_router.mapping,
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
             "catalog_name": self.catalog_name}
        )
        self.history = answer["history"]
        self.catalog_name = answer["catalog_name"]

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
            self.clear_history()
            print()
            print()
