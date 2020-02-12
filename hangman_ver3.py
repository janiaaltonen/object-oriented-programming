"""
Hangman game version 3.0
Game works in GUI
User tries to guess right word letter by letter
User has 8 wrong guesses, 9th wrong guess is game over
"""

import tkinter as tk
from random import randrange

hangintree = ('koroke', 'pystypuu', 'tukirauta', 'poikkipuu', 'köysi', 'pää', 'torso', 'kädet', 'jalat')


class Hangman:

    printable = []

    def __init__(self, filename='hangman_words.txt'):
        self.filename = filename
        self.__words = self.readWords()
        self.used_words = []
        self.__word = {str}
        self.__printable = []
        self.generate()
        self.corrects = set()
        self.missed = set()
        self.guesses = 0

    def readWords(self):
        """
        * method reads guessable words from txt. file and returns them in a tuple
        """
        file = None
        words = []
        try:
            file = open(self.filename, 'r', encoding="utf-8")
            for row in file:
                row = row.strip()
                if len(row) > 0:
                    words.append(row)
            file.close()
        except (FileNotFoundError, IOError) as error:
            print(f'Tiedostoa {self.filename} ei voitu lukea: {error}')
        finally:
            if file is not None:
                file.close()
        return tuple(words)

    def generate(self):
        """
        * method takes random word out of (self.__words)
        * used words are placed in used_words[] so they won't pop up again
        """

        while True:
            word = self.__words[randrange(len(self.__words))]
            if word not in self.used_words:
                self.used_words.append(word)
                self.__word = word
                self.__printable = ['_'] * len(word)
                break

    def check(self, letter):
        """
        * method checks if the input_letter is in random word, updates corrects set() and returns True
        * if not in random word updates missed set() and returns False
        * updates guesses (right ones)
        * places input_letter to correct position(s) in printable[]
        """
        index_places = [i for i, e in enumerate(self.__word) if e == letter]
        if len(index_places) > 0:
            self.corrects.add(letter)
            for i in index_places:
                self.__printable[i] = letter.upper()
                self.guesses += 1
            return True
        else:
            self.missed.add(letter)
            return False

    def isWin(self):
        """
        * method checks if game is won
        * if game is won corrects and missed sets() and guesses are reset
        * returns tuple()
        """
        is_won = self.guesses == len(self.__word)
        return is_won

    def reset(self):
        self.generate()
        self.corrects = set()
        self.missed = set()
        self.guesses = 0

    @property
    def getLetters(self):
        return " ".join([str(i) for i in self.__printable])

    @property
    def getWord(self):
        return self.__word


class HP(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__hangman = Hangman()
        self.bind("<Return>", self.updateUI)
        self.title("Hangman")
        self.geometry("480x320")
        self.input = tk.StringVar()
        self.output = tk.StringVar()
        self.output.set(self.__hangman.getLetters)
        self.info = tk.StringVar()


        self.frame1 = tk.Frame(self).pack(fill=tk.X, pady=10)
        tk.Label(self.frame1, text="Guess a letter").pack(fill=tk.X)
        self.entry = tk.Entry(self.frame1, textvariable=self.input, width=2)
        self.entry.pack()

        self.frame2 = tk.Frame(self).pack(fill=tk.X)
        tk.Label(self.frame2, textvariable=self.output).pack(fill=tk.X)

        self.frame3 = tk.Frame(self).pack(fill=tk.X)
        tk.Label(self.frame3, textvariable=self.info).pack(fill=tk.X)

        self.frame4 = tk.Frame(self).pack(fill=tk.X)
        tk.Button(self.frame4, text="Start a new game", command=self.createNewGame).pack(fill=tk.X, padx=15, pady=5)

    def updateUI(self, *args):

        letter = self.input.get()
        if len(letter) == 1:
            if letter not in self.__hangman.corrects and letter not in self.__hangman.missed:
                if self.__hangman.check(letter):
                    self.output.set(self.__hangman.getLetters)
                    if self.__hangman.isWin():
                        self.entry.config(state="disabled")
                        self.info.set("Guessed right, well done!!")
                else:
                    self.info.set("Sorry, wrong guess - that is " + str(len(self.__hangman.missed)) + "/ "
                                  + str(len(hangintree)) + ". part " + hangintree[len(self.__hangman.missed) - 1]
                                  + " in your hangintree")
                    if len(self.__hangman.missed) == len(hangintree):
                        self.info.set("HANGED! You failed to guess " + str(self.__hangman.getWord))
        else:
            self.info.set("Please enter only one letter")
        self.input.set("")

    def createNewGame(self):

        self.__hangman.reset()
        self.output.set(self.__hangman.getLetters)
        self.info.set("")
        self.entry.config(state="normal")


if __name__ == '__main__':
    HP().mainloop()
