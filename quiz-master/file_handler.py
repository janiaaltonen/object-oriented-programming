from question import Question
from answer import Answer


class FileHandler:
    def __init__(self):
        self.db_path = "db/"
        self.questions = '_questions.dat'
        self.answers = '_answers.dat'

    def read_questions(self, category):
        filename = category + self.questions
        path = self.db_path + filename
        questions = []
        with open(path, 'r', encoding="utf-8") as file:
            number = 0
            for row in file:
                question = row.strip()
                if len(question) > 0:
                    q = Question(category, question, number)
                    questions.append(q)
                    number += 1
        file.close()
        return tuple(questions)

    def read_answers(self, category, number):
        filename = category + self.answers
        path = self.db_path + filename
        answers = []
        with open(path, 'r', encoding="utf-8") as file:
            for i, row in enumerate(file):
                if i == number:
                    options = row.strip().split(";")
                    for option in options:
                        if "=T" in option:
                            answer = option.split("=T")[0]
                            a = Answer(answer, True, number)
                            answers.append(a)
                        else:
                            a = Answer(option, False, number)
                            answers.append(a)
        file.close()
        return tuple(answers)


if __name__ == '__main__':
    f = FileHandler()
    i = f.read_answers('geo',1)[0].text
    print(i)