from hangman_ver4.bloks import Block
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from hangman_ver5.hangman import Hangman
from hangman_ver5.classifier import Classifier

hangintree = ('koroke', 'pystypuu', 'tukirauta', 'poikkipuu', 'köysi', 'pää', 'torso', 'kädet', 'jalat')

levels = {0: 'demonstration', 1: 'easy', 2: 'intermediate', 3: 'difficult', 4: 'expert'}


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
    """
    * In requirements analysis there was method called configure(). I used method called config(),
    * because tk has method configure and don't know if it's meant to override that method and don't know how to get
    * around this without overriding tk method..
    * Currently there might not be enough words in expert level to play the game through..
    """

    class THangman(Hangman):
        def __init__(self, parent):
            self.level = parent.config()
            self.points = 0
            self._Hangman__words = self.readWords()
            super().__init__()

        def readWords(self):
            """
            * Overrides Hangman class method to use Classifier class method 
            """
            c = Classifier()
            return c.readWords(self.level)

        def newLevel(self):
            """
            * game has levels 0-4. Method updates level to next one. If player is in level 4, next one is 0.
            * After the level is updated, corresponding words are read to attribute _Hangman__words
            """
            if self.level < 4:
                self.level += 1
                message = "Congratulations! You have reached new level. You are now at " + levels[self.level] + " level"
                messagebox.showinfo("New level reached", message)
            else:
                self.level = 0
                message = "Congratulations! You are now master of Hangman game, a Yoda of words!. Game will now start" \
                          " again in the demonstration level"
                messagebox.showinfo("New level reached", message)
            self._Hangman__words = self.readWords()

    def __init__(self, title="Hangman"):
        super().__init__()
        self.title(title)
        self.geometry("720x480")
        self.configurationFile = "level.conf"
        self.__hp = HP.THangman(self)
        self.output = tk.StringVar()
        self.output.set(self.__hp.getLetters)
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
        message = "You are currently playing in " + levels[self.__hp.level] + " level"
        messagebox.showinfo("Level of difficulty", message)

    def config(self, write=False):
        file = None
        level = None
        if not write:
            try:
                file = open(self.configurationFile, 'r', encoding="utf-8")
                for row in file:
                    row = row.strip()
                    if len(row) > 0:
                        level = int(row.split(":", 1)[1])
                file.close()
            except (FileNotFoundError, IOError):
                c = Classifier()
                c.read()
                c.classify()
                level = 0
                try:
                    file = open(self.configurationFile, 'w', encoding="utf-8")
                    file.write("level:" + str(level) + "\n")
                    file.close()
                except IOError as e:
                    print(f'Tiedostoa {self.configurationFile} ei voitu luoda: {e}')
            finally:
                if file is not None:
                    file.close()
                return level
        else:
            try:
                file = open(self.configurationFile, 'w', encoding="utf-8")
                file.write("level:" + str(self.__hp.level) + '\n')
                file.close()
            except IOError as e:
                print(f'Tiedostoon {self.configurationFile} ei voitu kirjoittaa: {e}')
            finally:
                if file is not None:
                    file.close()

    def check(self, c_letter):
        """
        * every (wrong) or right guessed letter is worth (-)100 points.
        * e.g. guessable word includes three times letter 'A' -> only worth 100 points
        * if word is guessed right then 100*[length_of_word] is added to points
        * player can reach next level only then when word is guessed right and one has 10 000 or more points
        """
        letter = c_letter.lower()
        if letter not in self.__hp.corrects and letter not in self.__hp.missed:
            if self.__hp.check(letter):
                self.__hp.points += 100
                self.output.set(self.__hp.getLetters)
                if self.__hp.isWin():
                    self.__hp.points = 100 * len(self.__hp.getWord) + self.__hp.points
                    self.Buttons.disableAll()
                    self.info.set("You guessed right, well done!!")
                    if self.__hp.points >= 10000:
                        self.__hp.newLevel()
                        self.config(True)
            else:
                self.__hp.points -= 100
                self.info.set("Sorry, wrong guess - that is " + str(len(self.__hp.missed)) + ". part " +
                              hangintree[len(self.__hp.missed) - 1] + " in your hangintree")
                if len(self.__hp.missed) == len(hangintree):
                    self.info.set("HANGED! You failed to guess " + str(self.__hp.getWord))

    def new(self):
        self.__hp.reset()
        self.output.set(self.__hp.getLetters)
        self.Buttons.enableAll()
        self.info.set("")


if __name__ == '__main__':
    HP().mainloop()
