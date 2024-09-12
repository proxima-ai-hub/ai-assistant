import os
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
    
    dir_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(dir_path, 'original_data.csv') 
    collection_name = 'embeddings_db'   
    
    def __init__(self, model_type: ModelType, device: int = None) -> None:
        
        self._model_type = model_type
        if not device:
            self._device = 0 if is_available() else -1
        else:
            self._device = device
        
        self._model = self._setup_model()        
        self._client = QdrantClient('89.169.151.229', port=6333)   
        self.create_database()
    
    def _setup_model(self):
        print('*'*50)
        if self._model_type == ModelType.RUBERT_TINY_2:
            model = SentenceTransformer(
                ModelType.RUBERT_TINY_2.value,
                device='cpu'
            )
        elif self._model_type == ModelType.DEEPVK_USER:
            model = SentenceTransformer(
                ModelType.DEEPVK_USER.value,
                device='cpu'
            )
        else:
            raise NotImplementedError()

        return model
    
    def encode(self, text: Union[List[str], str]):
        if self._model_type == ModelType.RUBERT_TINY_2:
            embeddings = self._model.encode(text)
        elif self._model_type == ModelType.DEEPVK_USER:
            embeddings = self._model.encode(text, normalize_embeddings=True)
        else:
            raise NotImplementedError()
        
        return embeddings    
    
    def create_database(self):
        print('*'*100)
        collections = self._client.get_collections()
        print('На этом этапе мы на')
        if collections.collections:
            print('The collection already exists')    
            return           
        else:
            df = pd.read_csv(self.csv_path) 
            embeddings = self.encode(df['question'].to_list())
            print(f'EMB: {embeddings.shape}')
            self._fill_database(embeddings, df)

    def _fill_database(self, embeddings, df):
                
        self._client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=len(embeddings[1]),
                distance=models.Distance.COSINE
            ),
        )
        
        for idx, row in df.iterrows():
            self._client.upsert(
                collection_name=self.collection_name,
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
    
    def search(
            self,
            query: str,
            topk: int = 10,
            filter_options: dict = None,
            score_threshold: float = None
        ):
        embedding = self.encode(query)
        results = self._client.search(
            self.collection_name,
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