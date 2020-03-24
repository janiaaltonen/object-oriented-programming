class Answer:
    def __init__(self, text, is_correct, question_number):
        self.text = text
        self.isCorrect = is_correct
        self.questionNumber = question_number

    def get_text(self):
        return self.text

    def is_correct(self):
        return self.isCorrect

    def get_question_number(self):
        return self.questionNumber
