from pathlib import Path
from tqdm import tqdm
import json

from sklearn.metrics import classification_report
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import pandas as pd
from dotenv import dotenv_values

from agent.graphs import ConsultantGraph


config = dotenv_values(r"D:\ITMO\hack\ai-assistant\.env")

catalogs_to_id = {
    "здоровье": 0,
    "финансы": 1,
    "аккаунт": 2,
    "работа": 3,
    "документы": 4,
    "оператор": 5,
}
id_to_catalogs = {v: k for k, v in catalogs_to_id.items()}


prompt = """
Ты помощник в оценивании результатов работы другой нейросети.
Тебе на вход приходит правильный ответ GROUND_TRUTH и ответ нейросети ANSWER.
Твоя задача сравнить два этих вопроса и поставить оценку тому, насколько
ответ нейросети ANSWER совпадает с ответом GROUND_TRUTH.

### Требования
1. Поставь оценку 1 - если ответ нейросети совсем не совпадает с правильным.
2. Поставь оценку 2 - если ответ нейросети частично совпадает с правильным, но были упомянуты неправдивые факты или
ответ нейросети не содержит всей информации.
3. Поставь оценку 3 - если ответ нейросети по смыслу совпадает с правильным и упомянуты все факты.
4. ВАЖНО! В качестве ответа выведи только одно число от 1 до 3 в виде строки без скобок.
5. ВАЖНО! Не добавляй свои комментарии, ответом должно быть только число.

GROUND_TRUTH:
{gt}
ANSWER:
{answer}
Твой ответ:
"""


def get_answers(data: pd.DataFrame, graph: ConsultantGraph):
    answers = []
    catalogs = []
    for question in tqdm(data["question_changed"]):
        result = graph.invoke(question).content
        catalogs.append(graph.catalog_name)
        answers.append(result)
        graph.clear_history()

    return answers, catalogs


def offline_classification_metrics(catalogs, catalogs_predicted):
    catalogs_encoded = list(map(catalogs_to_id.get, catalogs))
    catalogs_predicted_encoded = list(map(catalogs_to_id.get, catalogs_predicted))
    print(set(catalogs_encoded))
    print(set(catalogs_predicted_encoded))

    report = classification_report(
        catalogs_encoded, catalogs_predicted_encoded,
        target_names=list(catalogs_to_id.keys()),
        output_dict=True,
    )

    return report


def offline_answer_metrics(llm, gt, predicted, base_path):
    assert len(gt) == len(predicted)

    result = {
        "true": [],
        "pred": [],
        "score": []
    }
    for answer_gt, answer_pred in tqdm(zip(gt, predicted)):
        answer = llm.invoke({
            "gt": answer_gt,
            "answer": answer_pred
        })
        result["true"].append(answer_gt)
        result["pred"].append(answer_pred)
        result["score"].append(answer.content)

    with open(base_path / "scores_llama3.1_deepvk.json", "w+", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    # with open(base_path / "scores_llama3.1.json", "r", encoding="utf-8") as file:
    #     result = json.load(file)

    data_pd = pd.DataFrame(result)
    data_pd["score"] = data_pd["score"].astype("int")
    counts = data_pd["score"].value_counts()

    metrics = {
        "correct": int(counts[3]),
        "semi-correct": int(counts[2]),
        "incorrect": int(counts[1]),
        "percent_correct": float(counts[3] / len(gt)),
        "percent_semi-correct": float(counts[2] / len(gt)),
        "percent_incorrect": float(counts[1] / len(gt)),
    }

    return metrics


if __name__ == "__main__":
    base_path = Path(__file__).parent.resolve()

    llm = ChatOpenAI(
        api_key=config["OPENAI_API_KEY"],
        model="gpt-4o-mini",
        temperature=0
    )
    template = PromptTemplate.from_template(prompt)
    model = template | llm

    # graph = ConsultantGraph(show_logs=False)

    # data = pd.read_csv(base_path / "benchmark_questions.csv")
    # answers, catalogs = get_answers(data, graph)
    # answers_table = data.copy()
    # answers_table["predicted"] = answers
    # answers_table["predicted_catalogs"] = catalogs
    # answers_table.to_csv(base_path / "llama3.1_deepvk_results.csv", index=False)

    answers_table = pd.read_csv(base_path / "llama3.1_deepvk_results.csv")

    cls_metrics = offline_classification_metrics(
        answers_table["catalog"],
        catalogs_predicted=answers_table["predicted_catalogs"]
    )
    with open(base_path / "metrics_llama3.1_deepvk.json", "w+") as file:
        json.dump(cls_metrics, file, ensure_ascii=False, indent=4)

    llm_metrics = offline_answer_metrics(
        model,
        answers_table["content_changed"],
        answers_table["predicted"],
        base_path
    )

    with open(base_path / "llm_metrics_llama3.1_deepvk.json", "w+", encoding="utf-8") as file:
        json.dump(llm_metrics, file, ensure_ascii=False, indent=4)
