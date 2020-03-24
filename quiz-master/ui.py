import tkinter as tk
from tkinter import ttk
from quiz import Quiz


class AnswerBlock(ttk.Frame):
    def __init__(self, parent, answers, columns):
        super().__init__(parent)
        self.parent = parent
        self.buttons = []
        self.answers = answers
        for i, answer in enumerate(answers):
            self.buttons.append(ttk.Button(self, text=answer.get_text(), command=lambda i=i: self.check(i), width=15))
            self.buttons[i].grid(row=i // columns, column=i % columns, sticky=tk.W + tk.E + tk.S + tk.N, pady=10, padx=10)

    def check(self, num):
        self.parent.check_answer(self.answers[num].isCorrect)


class UI(tk.Tk):
    def __init__(self, title="QuizMaster"):
        super().__init__()
        self.title(title)
        self.geometry("720x300")
        self.__quiz = Quiz()
        self.question = tk.StringVar()
        self.info = tk.StringVar()
        self.question.set(self.__quiz.ask_question())

        self.questionFrame = tk.Frame(self).grid(row=1, sticky=tk.W + tk.E + tk.S + tk.N)
        tk.Label(self.questionFrame, textvariable=self.question).grid(padx=75, pady=20,
                                                                      sticky=tk.W + tk.E + tk.S + tk.N, columnspan=5)
        self.Buttons = AnswerBlock(self, self.__quiz.ansForQuestion, 2)
        self.Buttons.grid(row=4, column=0, columnspan=3, padx=200, pady=5)

        self.infoFrame = tk.Frame(self).grid(row=6)
        tk.Label(self.infoFrame, textvariable=self.info).grid(padx=75, pady=20,
                                                                        sticky=tk.W + tk.E + tk.S + tk.N, columnspan=5)
        self.canvas = tk.Canvas(self, width=500, height=250)
        self.canvas.grid(row=8, columnspan=9, padx=120, sticky=tk.W + tk.E + tk.S + tk.N)
        self.create_circles()

    def create_circles(self, fill=False, correct=False):
        if not fill:
            start = 5
            end = 25
            for i in range(len(self.__quiz.questions)):
                self.canvas.create_oval(start, 5, end, 25, width=2)
                start += 30
                end += 30
        else:
            start = 5 + 30 * self.__quiz.questionToAsk
            end = 25 + (30 * self.__quiz.questionToAsk)
            if not correct:
                self.canvas.create_oval(start, 5, end, 25, width=2, fill='#b50b0b')
            else:
                self.canvas.create_oval(start, 5, end, 25, width=2, fill='#1d5e2b')

    def check_answer(self, is_correct):
        if is_correct:
            self.__quiz.corrects += 1
            self.create_circles(True, True)
        else:
            self.create_circles(True, False)
        if self.__quiz.questionToAsk < len(self.__quiz.questions) - 1:
            self.__quiz.questionToAsk += 1
            self.ask_new_question()
        else:
            self.info.set(f"Peli päättyi! Tiesit oikein {self.__quiz.corrects} / {len(self.__quiz.questions)}")

    def ask_new_question(self):
        self.question.set(self.__quiz.ask_question())
        self.__quiz.get_answers_for_question(self.__quiz.questionToAsk)
        self.Buttons = AnswerBlock(self, self.__quiz.ansForQuestion, 2)
        self.Buttons.grid(row=4, column=0, columnspan=3, padx=200, pady=5)

if __name__ == '__main__':
    UI().mainloop()