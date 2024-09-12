from agent.graphs import ConsultantGraph

if __name__ == "__main__":
    graph = ConsultantGraph(show_logs=True, save_online_metric=False)
    graph.chat()
