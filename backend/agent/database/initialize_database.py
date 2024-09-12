from pathlib import Path

from agent.database.retriever import Retriever, ModelType


if __name__ == "__main__":
    retriever = Retriever(model_type=ModelType.DEEPVK_USER, device=0)
    retriever.create_database(
        Path(__file__).parent.resolve() / "case_datasets" / "original_data.csv",
        "original_data_deepvk_collection"
    )

    print(retriever.search(
        "В личном кабинете нет вкладки передать в архив",
        "original_data_deepvk_collection",
        topk=1,
        filter_options={"catalog": "аккаунт"}
    ))    
