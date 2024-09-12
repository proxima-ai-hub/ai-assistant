from pathlib import Path
from tqdm import tqdm

import pandas as pd
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import dotenv_values


config = dotenv_values(r"D:\ITMO\hack\ai-assistant\.env")

prompt = """
Ты помощник в составлении датасета для тестирования другой LLM-модели.
Тебе приходит на вход вопрос пользователя.
Твоя задача переформулировать вопрос так чтобы исходный смысл сохранился.

Можно заменять слова на синонимы, менять местами.

Вопрос:
{query}
Твой ответ:
"""

if __name__ == "__main__":
    llm = OpenAI(
        api_key=config["OPENAI_API_KEY"],
        model="gpt-3.5-turbo-instruct"
    )
    path = Path(__file__).parent.parent.resolve() / "database" / "case_datasets" / "original_data.csv"
    questions = pd.read_csv(path, usecols=["question_changed", "content_changed", "catalog"])

    cols = []
    template = PromptTemplate.from_template(prompt)
    model = template | llm

    for question in tqdm(questions["question_changed"]):
        answer = model.invoke({"query": question})
        cols.append(answer)

    questions["new_questions"] = cols
    questions.to_csv("benchmark_questions.csv")
