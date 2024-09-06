import os

from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from dotenv import load_dotenv
import torch

load_dotenv()


print(torch.cuda.is_available())

HUGGING_FACE_LLAMA_TOKEN = os.getenv("HUGGING_FACE_LLAMA_TOKEN")
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"

os.environ["HF_TOKEN"] = HUGGING_FACE_LLAMA_TOKEN
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGING_FACE_LLAMA_TOKEN

pipeline_hf = pipeline(
    "text-generation", model=MODEL_NAME, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto"
)
llm = HuggingFacePipeline(pipeline=pipeline_hf)
response = llm.invoke("The first man on the moon was ...")
print(response)
