import nltk


QUESTION_WORDS = [
    "What",
    "When",
    "Where",
    "Which",
    "Who",
    "Whom",
    "Whose",
    "Why",
    "How",
]
QUESTION_MARK = "?"


class TextProcessor:
    def __init__(self) -> None:
        pass

    def is_question(self, text: str):

        if text[len(text) - 1] == QUESTION_MARK:
            return False

        for word in text.lower():
            if word in QUESTION_WORDS:
                return False
        return True
