from pathlib import Path

from agent.database.retriever import Retriever, ModelType


if __name__ == "__main__":
    retriever = Retriever(model_type=ModelType.RUBERT_TINY_2, device=0)
    # retriever.create_database(
    #     Path(__file__).parent.resolve() / "case_datasets" / "original_data.csv",
    #     "original_data_collection"
    # )

    print(retriever.search(
        "Могу ли я заправляться по топливной карте?",
        "original_data_collection",
        topk=1,
    ))    
