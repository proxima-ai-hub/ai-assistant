from agent.llms import LlamaLLM

prompt = """
Ты помощник перевода текста на английский язык.
Тебе на вход приходит запрос QUERY на русском языке.
Твоя задача перевести QUERY на английский язык.

<Пример>
QUERY:
Привет, я Джон. Как у тебя дела?
Твой ответ:
Hello, my name is John. How are you doing?
<Конец примера>

QUERY:
{query}
Твой ответ:
"""

if __name__ == "__main__":
    llm = LlamaLLM("llama", "llama3.1", prompt)

    question = "Сегодня хорошая погода!"
    answer = llm.invoke({"query": question})
    
    print(f"QUERY (eng): {question}")
    print(f"Model answer (rus): {answer}")
