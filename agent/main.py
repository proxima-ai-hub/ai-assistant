from agent.graphs import ConsultantGraph

if __name__ == "__main__":
    graph = ConsultantGraph(show_logs=True)
    from IPython.display import Image, display
    from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

    data = Image(
        graph.graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
    ).data
    import io
    from PIL import Image as IMG

    imageStream = io.BytesIO(data)
    imageFile = IMG.open(imageStream)
    imageFile.save("graph.png")
    # graph.chat()
