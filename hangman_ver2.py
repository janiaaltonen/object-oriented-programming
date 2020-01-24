"""
Hangman game version 2.0
Game works in console
User tries to guess right word letter by letter
User has 8 wrong guesses, 9th wrong guess is game over
"""
from random import randrange

global hangintree
hangintree = ('koroke', 'pystypuu', 'tukirauta', 'poikkipuu', 'köysi', 'pää', 'torso', 'kädet', 'jalat')


class Hangman:
    """
    """
    printable = []

    def __init__(self, filename='hangman_words.txt'):
        self.filename = filename
        self.__words = self.readWords()
        self.used_words = []
        self.__word = {str}
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
        * @classmethod init_printable is called to initialize printable word like _ _ _
        """

        while True:
            word = self.__words[randrange(len(self.__words))]
            if word not in self.used_words:
                self.used_words.append(word)
                self.__word = word
                self.initPrintable(word)
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
                self.printable[i] = letter.upper()
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
        if is_won:
            self.corrects = set()
            self.missed = set()
            self.guesses = 0
        return is_won, self.__word

    @classmethod
    def initPrintable(cls, word):
        """
        * set value for printable [] before any letters are guessed
        * param. word comes from method generate()
        * @classmethod used to learn about classes and objects
        * not sure if I should prefer instance method instead in this case??!?
        """
        cls.printable = ['_'] * len(word)


def show(hangman_object):
    """
    * function prints printable word's right guessed letters or _ in place of not guessed letters
    """
    print(*hangman_object.printable)


def guess(hangman_object):
    """
    * function asks letter from user
    * verify that user_input is letter or '-' sign
    * checks that letter is not guessed before (correct or missed)
    * returns user_input
    """
    while True:
        user_input = input("Guess a letter: ").lower()
        print(user_input.upper())
        print()
        if len(user_input) >= 1 and user_input.isalpha() or user_input == '-':
            if user_input not in hangman_object.corrects and user_input not in hangman_object.missed:
                return user_input


def isContinue():
    """
    * asks from user if one wants to continue with new word else program closes.
    """
    letter = input('Continue with a new word [y/Y]?:\t')
    if len(letter) > 0 and letter.isalpha() and letter[0].lower() == 'y':
        return True
    else:
        return False


def play():
    """
    - contains the main loop
    - creates a Hangman object
    - calls Hangman's methods generate, check and isWin in the loop
    - calls guess, read and isContinue functions
    """
    print('Hangman - guess word letter by letter. Wrong guesses may hang you.')
    hp = Hangman()
    while True:
        hp.generate()
        while True:
            show(hp)
            if hp.check(guess(hp)):
                win, word = hp.isWin()
                if win:
                    print(f'{word.upper()}', 'is correct! Well done!!', sep='\n')
                    break
            else:
                print(f'Sorry, wrong guess - that is {len(hp.missed)}. part {hangintree[len(hp.missed)-1]} in your hangintree')
                if len(hp.missed) == len(hangintree):
                    print(f'HANGED!!', 'You failed to guess ', f'{word.upper()}', sep='\n')
                    break
        if not isContinue():
            break


if __name__ == '__main__':
    play()
