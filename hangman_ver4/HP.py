from hangman_ver4.bloks import Block
import tkinter as tk
from tkinter import ttk
from hangman_ver4.hangman import Hangman

hangintree = ('koroke', 'pystypuu', 'tukirauta', 'poikkipuu', 'köysi', 'pää', 'torso', 'kädet', 'jalat')


class ButtonsBlock(Block):
    def __init__(self, parent, alphabets, columns):
        super().__init__(parent)
        self.parent = parent
        self.buttons = []
        self.alphabets = alphabets
        for i, alphabet in enumerate(alphabets):
            self.buttons.append(ttk.Button(self, text=str(alphabet), command=lambda i=i:
                                           self.disable(i), width=4))
            self.buttons[i].grid(row=i // columns, column=i % columns, sticky=tk.W + tk.E + tk.S + tk.N, pady=2, padx=2)

    def disable(self, nro):
        self.buttons[nro].config(state='disabled')
        self.parent.check(self.buttons[nro]['text'])


class HP(tk.Tk):
    def __init__(self, title="Hangman"):
        super().__init__()
        self.title(title)
        self.geometry("720x480")
        self.hangman = Hangman()
        self.output = tk.StringVar()
        self.output.set(self.hangman.getLetters)
        self.info = tk.StringVar()
        alphabets = 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', \
                    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Å', 'Ä', 'Ö', '-'
        self.Buttons = ButtonsBlock(self, alphabets, 15)
        self.Buttons.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        self.frame2 = tk.Frame(self).grid(row=2)
        tk.Label(self.frame2, textvariable=self.output).grid(pady=10, columnspan=5)

        self.frame3 = tk.Frame(self).grid(row=3)
        tk.Label(self.frame3, textvariable=self.info).grid(padx=10, pady=10, columnspan=5, sticky=tk.W + tk.E)

        tk.Button(self, text="Start a new game", command=self.new).grid(row=5, padx=30, pady=5,
                                                                        sticky=tk.E + tk.W, columnspan=5)

    def check(self, c_letter):
        letter = c_letter.lower()
        if letter not in self.hangman.corrects and letter not in self.hangman.missed:
            if self.hangman.check(letter):
                self.output.set(self.hangman.getLetters)
                if self.hangman.isWin():
                    self.Buttons.disableAll()
                    self.info.set("You guessed right, well done!!")
            else:
                self.info.set("Sorry, wrong guess - that is " + str(len(self.hangman.missed)) + ". part " +
                              hangintree[len(self.hangman.missed) - 1] + " in your hangintree")
                if len(self.hangman.missed) == len(hangintree):
                    self.info.set("HANGED! You failed to guess " + str(self.hangman.getWord))

    def new(self):
        self.hangman.reset()
        self.output.set(self.hangman.getLetters)
        self.Buttons.enableAll()
        self.info.set("")


if __name__ == '__main__':
    HP().mainloop()
