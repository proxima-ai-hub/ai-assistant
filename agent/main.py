from agent.graphs import ConsultantGraph

if __name__ == "__main__":
    graph = ConsultantGraph(show_logs=False)
    graph.chat()

    print()
    print("------ Message history ------")
    print(graph.history)
