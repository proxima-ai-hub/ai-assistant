from pathlib import Path

from agent.database.retriever import Retriever, ModelType


if __name__ == "__main__":
    retriever = Retriever(model_type=ModelType.DEEPVK_USER, device=0)
    retriever.create_database(path_to_data="<your_path_to_data>",
                              collection_name="<your_collection_name>")

    # Test it works
    print(retriever.search(
        "В личном кабинете нет вкладки передать в архив",
        "original_data_deepvk_collection",
        topk=1,
        filter_options={"catalog": "аккаунт"}
    ))    
