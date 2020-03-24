
class Question:
    def __init__(self, category, question, number):
        self.category = category
        self.question = question
        self.number = number

    def get_question(self):
        return self.question

    def get_category(self):
        return self.category

    def get_number(self):
        return self.number
