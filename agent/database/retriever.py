from typing import List, Union
from pathlib import Path
from enum import Enum

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from torch.cuda import is_available
import pandas as pd


class ModelType(Enum):
    RUBERT_TINY_2 = "cointegrated/rubert-tiny2"
    DEEPVK_USER = "deepvk/USER-bge-m3"


class Retriever:
    def __init__(self, model_type: ModelType, device: int = None) -> None:
        self._model_type = model_type
        if not device:
            self._device = 0 if is_available() else -1
        else:
            self._device = device
        self._model = self._setup_model()
        
        self._client = QdrantClient('176.114.66.132', port=6333)
    
    def _setup_model(self):
        if self._model_type == ModelType.RUBERT_TINY_2:
            model = SentenceTransformer(
                ModelType.RUBERT_TINY_2.value,
                device=self._device
            )
        elif self._model_type == ModelType.DEEPVK_USER:
            model = SentenceTransformer(
                ModelType.DEEPVK_USER.value,
                device=self._device
            )
        else:
            raise NotImplementedError()

        return model
    
    def create_database(self, path_to_data: str, collection_name="default_data_db"):
        df = pd.read_csv(path_to_data)

        embeddings = self.encode(df["question"].to_list())
        self._fill_database(embeddings, df, collection_name)

    def encode(self, text: Union[List[str], str]):
        if self._model_type == ModelType.RUBERT_TINY_2:
            embeddings = self._model.encode(text)
        elif self._model_type == ModelType.DEEPVK_USER:
            embeddings = self._model.encode(text, normalize_embeddings=True)
        else:
            raise NotImplementedError()
        
        return embeddings
    
    def search(
            self,
            query: str,
            collection_name: str,
            topk: int = 10,
            filter_options: dict = None,
            score_threshold: float = None
        ):
        embedding = self.encode(query)
        results = self._client.search(
            collection_name,
            embedding,
            limit=topk,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(key=k, match=models.MatchValue(value=v))
                    for k, v in filter_options.items()
                ]
            ) if filter_options else None,
            score_threshold=score_threshold
        )

        return results
    
    def _fill_database(self, embeddings, df, collection_name):
        if len(embeddings) != df.shape[0]:
            raise Exception("embeddings length must be equals dataframe number of rows")
        
        self._client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=len(embeddings[0]),
                distance=models.Distance.COSINE
            ),
        )

        for idx, row in df.iterrows():
            self._client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=idx,
                        vector=embeddings[idx],
                        payload={
                            "question": row["question_changed"],
                            "content": row["content_changed"],
                            "category": row["category"],
                            "catalog": row["catalog"]
                        }
                    )
                ]
            )

