from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langgraph.graph import END, START, StateGraph

from agent.nodes import ClassifierNode
from agent.llms import LlamaLLM
from agent.graphs import State


class ConsultantGraph:
    def __init__(self, show_logs=False) -> None:
        self.llm = LlamaLLM("llama_3.1 from ollama", "llama3.1")
        self.show_logs = show_logs

        self.graph = self._build_graph()
        self.history = [AIMessage(content="Привет, я бот-консультант, чем могу помочь?")]
    
    def _build_graph(self):
        graph = StateGraph(State)
        
        # Initialize nodes
        classifier_node = ClassifierNode(
            name="Classifier Node",
            description=ClassifierNode.__doc__,
            llm=self.llm,
            show_logs=self.show_logs
        )

        # Set up graph relations
        graph.add_node("classifier", classifier_node.invoke)

        graph.add_edge(START, "classifier")
        graph.add_edge("classifier", END)

        return graph.compile()
    
    def invoke(self, query: str):
        self.history.append(HumanMessage(content=query))
        answer = self.graph.invoke({"history": self.history})["history"][-1]
        self.history.append(answer)

        return answer

    def _print_message(self) -> str:
        message = self.history[-1]
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        print(f"{role}: {message.content}")

    def chat(self):
        self._print_message()
        query = input("user: ")
        while query != "q":
            self.invoke(query=query)
            self._print_message()

            query = input("user: ")