import os
import torch
from utils import conn_to_
from text_generator import TextGenerator
from transformers import (
    AutoModelForCausalLM,
    AutoConfig,
    AutoTokenizer,
    BitsAndBytesConfig,
)

from transformers import (AutoTokenizer, T5ForConditionalGeneration)

class Pipeline:
    """
    Pipeline for text generation
    """

    def __init__(self):
        config = conn_to_(cnf='model')
        
        self.model_name = config['name']['t5-base']
        
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        self.text_generator = TextGenerator(model=self.model,
                                            tokenizer=self.tokenizer,
                                            device='cuda:0')
        
        
    def generate(self, text):
        text = self.text_generator.generate_text(text)
        return text

    

# class ModelLoader:
#     def __init__(self, model_path: str):
#         self.model_path = model_path
#         self.config = AutoConfig.from_pretrained(
#             self.model_path,
#             trust_remote_code=True,
#             use_auth_token=os.getenv("HUGGINGFACE_TOKEN"),
#         )
#         self.model = self._load_model()
#         self.tokenizer = AutoTokenizer.from_pretrained(
#             self.model_path, use_auth_token=os.getenv("HUGGINGFACE_TOKEN")
#         )

#     def _load_model(self):
#         nf4_config = BitsAndBytesConfig(
#             load_in_4bit=True,
#             bnb_4bit_quant_type="nf4",
#             bnb_4bit_use_double_quant=True,
#             bnb_4bit_compute_dtype=torch.bfloat16,
#         )
#         model = AutoModelForCausalLM.from_pretrained(
#             self.model_path,
#             quantization_config=nf4_config,
#             trust_remote_code=True,
#             device_map="auto",
#             use_auth_token=os.getenv("HUGGINGFACE_TOKEN"),
#         )
#         return model
