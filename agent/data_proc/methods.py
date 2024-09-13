from agent.data_proc.resources import punctuation, glossary, dict_glossary


def question_converter(question: str) -> str:
    question = question.lower().translate(str.maketrans(punctuation, ' ' * len(punctuation)))
    question_list = question.split()
    for ind, word in enumerate(question_list):
        if word in glossary:
            if word == 'тк':
                if ind < len(question_list) - 1 and question_list[ind + 1] == 'рф':
                    question_list[ind] = dict_glossary['тк рф']
                    continue
            question_list[ind] = dict_glossary[word]
    return " ".join(question_list)
